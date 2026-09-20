# Fixing a Second Monitor That Stopped Working: Tracking It Down to a GPU Driver Update

## The problem

After a routine restart, my PC stopped detecting my second monitor. The HDMI signal wasn't being picked up at all, and the screen stayed blank. The first monitor still worked, but something was clearly wrong.

I wanted to work out what was actually going on, so I treated it like any other support ticket: rule out the simple causes first, then follow the evidence.

## Approach

I worked through the problem in a few stages:

1. **Rule out the cables.** I disconnected every cable between the monitor and the PC to check for a loose or faulty connection. This had no effect, and the second monitor still wasn't picking up an HDMI signal.

2. **Do a full power reset.** I shut the PC down and disconnected it from the power supply, removed the HDMI cable from the affected monitor, and unplugged the monitor from its power source so it could reset as well.

3. **Read the symptoms.** When the PC came back on, the first monitor was running at the wrong resolution. This was the key clue. A wrong resolution on a working display, plus a second display that wasn't detected, pointed at the GPU rather than the cables or the monitor.

4. **Reinstall the drivers.** I downloaded the AMD Adrenalin software, which includes the GPU drivers. The installer crashed with **error 207** and couldn't finish.

5. **Check Device Manager.** The error led me to Device Manager, which showed that the GPU was **disabled**. Task Manager showed the same thing. That explained both the resolution problem and the missing display.

6. **Look at the driver release date.** After re-enabling the GPU, I went back to AMD's website and saw that a new driver had been released on the same day the problem started. That made the latest update the most likely cause.

## The fix

I downloaded an **earlier driver version** that I knew hadn't caused problems, and used it to factory reset the GPU, replacing the suspect installation with a clean one.

The second monitor came back and displayed normally. The Brave browser also stopped lagging, which suggests it was affected by the same driver problem.
