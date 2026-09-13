# Building a Python Port Scanner with nmap

**GitHub:** [Av33raj/python-nmap-port-scanner](https://github.com/Av33raj/python-nmap-port-scanner)

## Overview

A command-line tool that scans a target IP address across a chosen range of ports and reports whether each one is open, closed, or filtered. It wraps the industry-standard `nmap` engine in a small Python script, validates the user's input before scanning, prints results live as it goes, and saves a timestamped report to a text file at the end.

It's a small project, but it touches a lot of the fundamentals that come up constantly in networking and security work: input validation, iterating over a port range, and structuring scan results for reporting.

## How It Works

The script runs in three stages:

1. **Input validation** — before anything is scanned, the tool checks that the target is actually a valid IPv4 address using a regex (`^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$`), and that the port range is entered in the expected `min-max` format (e.g. `40-45`) using a second regex. Both prompts loop until valid input is given, so a malformed IP or port range can't cause the scan itself to fail partway through.
2. **Scanning** — using the `python-nmap` library, the script loops over every port in the given range and calls `nm.scan()` for each one individually, pulling out the TCP state (`open`, `closed`, `filtered`) from the result and printing it to the terminal as it's found.
3. **Reporting** — every result is collected into a list of dictionaries (`ip`, `port`, `status`) as the scan runs. Once finished, `save_txt()` writes them all out to a timestamped, formatted text file so there's a persistent record of the scan afterwards.

## Tech Stack

- **Python**
- **python-nmap** — a Python wrapper around the `nmap` scanning engine
- **re** (regex) — for validating the IP address and port range input
- **datetime** — for timestamping the saved report

## Key Implementation Details

- **Scanning port-by-port** — rather than passing the whole port range to `nmap` in one call, the script loops and calls `nm.scan()` once per port. This keeps the logic simple and makes it easy to print live progress as each port finishes, at the cost of being slower than a single batched nmap scan over the full range.
- **Defensive input handling** — both the IP address and port range prompts sit in `while True` loops that only break once the regex matches, so the user gets immediate, specific feedback ("please enter the range... in the format: (40-45)") instead of the script crashing on bad input.
- **Try/except around each scan** — each individual port scan is wrapped in a `try/except`, so if a single port scan fails or returns unexpected data, the tool logs it and keeps going rather than stopping the whole scan.
- **Structured results over raw output** — storing each result as a dictionary rather than just printing it means the same data can be reused for the saved report without re-parsing anything.

## What I'd Improve Next

- Batch the scan into a single `nm.scan(ip, f"{port_min}-{port_max}")` call instead of one call per port, which would be significantly faster for larger ranges.
- Add support for scanning multiple IPs or a subnet in one run.
- Let the user choose the output format (e.g. CSV or JSON) instead of only a plain text file, to make the results easier to feed into other tools.
- Add basic error handling for cases where `nmap` isn't installed or isn't on the system PATH, with a clearer message than the current catch-all exception.

## Takeaways

This project was a good exercise in wrapping a proper security tool (`nmap`) in a script that's actually pleasant to use — validating input up front, giving live feedback, and leaving the user with a saved report rather than just terminal output that scrolls away. It's a small building block, but the same pattern (validate → scan → structure results → report) scales up to much bigger reconnaissance tooling.
