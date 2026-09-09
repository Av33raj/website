# Building an SSH Brute-Force Log Detector in Python

## The problem

One of the most common tasks in a SOC (Security Operations Centre) is log triage — going through authentication logs to spot signs of an attack before it succeeds. A classic pattern to look for is brute-forcing: an attacker hammering an SSH login with repeated failed attempts in a short window of time.

I wanted to build a small tool that automates the first step of that process: given a log file, flag any IP address showing a burst of failed login attempts close together in time.

## Approach

The tool works in a few stages:

1. **Parse the log.** Each line of an SSH auth log looks something like:
   ```
   Mon Jan 5 03:14:22 host sshd[1234]: Failed password for invalid user admin from 192.0.2.5 port 51422 ssh2
   ```
   I used regular expressions to pull out the IP address and timestamp from each line, and checked whether the attempt was a `Failed` or `Accepted` login.

2. **Group failures by IP.** Using a `defaultdict(list)`, every failed attempt gets appended to a list keyed by source IP — so by the end of the file, I have a clean mapping of "this IP failed at these times."

3. **Convert timestamps and check the gaps.** Raw timestamps are just strings, so I parsed them into proper `datetime` objects with `strptime`. One thing I hadn't expected: syslog-style timestamps pad single-digit days with an extra space (`Jan  5` instead of `Jan 05`) — `strptime` handled it fine once I got the format string right, but it caught me out at first.

   For each IP, I sorted its list of timestamps and compared every consecutive pair, converting the difference into seconds with `.total_seconds()`. If any pair fell under a threshold (120 seconds by default), that IP got flagged as suspicious.

4. **Report the results.** Flagged IPs are printed to the console and written out to a CSV file, so the output can be opened in Excel or Sheets rather than just scrolling past it in a terminal.

5. **Make it usable.** Rather than hardcoding the log file path and the time threshold, I used `argparse` so the tool can be run like:
   ```
   python access_data.py sample_logs.txt --threshold 60
   ```

## A snippet

The core detection logic — comparing consecutive failures per IP — ended up looking like this:

```python
for ip, timestamps in failures.items():
    timestamps.sort()
    for start, end in zip(timestamps, timestamps[1:]):
        gap = (end - start).total_seconds()
        if gap < args.threshold:
            flagged_ips[ip] = gap
```

Simple once it clicked, but getting there took a few wrong turns — mostly around regex syntax (forgetting square brackets around character ranges) and mixing up `strptime` (parsing a string into a date) with `strftime` (formatting a date into a string).

## What's next

A few natural extensions if I revisit this:
- Counting *how many* failures were in a burst, not just flagging the IP
- Pulling in a geoIP lookup to show where flagged IPs are coming from
- Adapting it to tail a live log file in real time, rather than reading a static file

## Code

The full project, including sample log data, is on GitHub: [SSH_Log_brute_force_detection](https://github.com/Av33raj/SSH_Log_brute_force_detection)
