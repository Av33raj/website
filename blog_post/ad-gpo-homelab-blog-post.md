# Building My First Active Directory Domain (and Everything That Went Wrong Along the Way)

## Why I built this

While applying for IT support and cyber security roles, I kept seeing the same requirements come up: Active Directory, Group Policy, user account administration. I'd studied the theory as part of my Computer Science with Cyber Security degree, but I hadn't actually built a domain from scratch — so I set out to fix that with a home lab.

The goal: stand up a working Windows Server domain controller, structure it with a realistic organisational unit (OU) layout, join a client machine to it, and enforce a security policy across the network using Group Policy.

## What I built

Using VirtualBox, I created two virtual machines:

- **WinServer-DC** — Windows Server 2022, promoted to a domain controller for a new forest, `homelab.local`
- **win10-Client** — a Windows 10 machine that would later join that domain

On the domain controller, I installed the Active Directory Domain Services and DNS roles, then built out an organisational structure with three OUs — **IT**, **Sales**, and **Finance** — each containing test users, and a security group (**Finance-Users**) to practise group-based access control.

Once the structure was in place, I joined the Windows 10 client to the domain and created a Group Policy Object to restrict Control Panel access for users in the IT OU — a simple, visually obvious way to prove that policy enforcement was actually working end to end, not just configured on paper.

## Where it actually got interesting

The AD setup itself went smoothly. The two problems that came up afterwards taught me more than the setup did.

**Problem 1: the domain join kept failing with "AD DC could not be contacted."**

My first instinct was that I'd misspelled the domain name (I had, briefly — `homelabs.local` instead of `homelab.local`). But fixing that didn't solve it. Running `ipconfig` on both VMs showed they were both sitting on the exact same private IP range (`10.0.2.x`) under VirtualBox's default NAT mode — which, it turns out, isolates every VM onto its *own* private network. Each machine thought it was alone.

The fix was switching both VMs from plain **NAT** to a shared **NAT Network**, which puts them on the same virtual subnet and lets them actually route to each other. Once I did that, `ping` between the two machines worked, DNS resolution for `homelab.local` worked, and the domain join succeeded immediately.

**Problem 2: Group Policy wouldn't apply, citing a clock mismatch.**

After joining the domain, running `gpupdate /force` failed with an error about the computer's clock not being synchronised with the domain controller's. Active Directory relies on Kerberos for authentication, and Kerberos has a built-in tolerance for time drift — if the client and DC clocks are too far apart, authentication (and therefore policy application) is refused as a security measure.

Checking both VMs' clocks confirmed it: they were roughly seven hours apart. I forced a clock sync on the client via Settings > Date & Time, confirmed it matched the DC, and reran `gpupdate /force` — this time it completed cleanly.

## Proof it worked

With both issues resolved, I logged in as a domain user placed in the IT OU and tried to open Control Panel. Windows blocked it outright:

> *"This operation has been cancelled due to restrictions in effect on this computer. Please contact your system administrator."*

That confirmed the whole chain was working — domain structure, policy creation, policy linking, and enforcement on a real client machine.

## What I'd take into a real environment

Neither of the problems I hit were AD configuration mistakes — they were infrastructure issues (networking, time sync) that just happen to break AD in specific, sometimes confusing ways. That's arguably the more useful lesson: a lot of real-world "AD isn't working" tickets probably aren't AD problems at all, they're the environment underneath it. Knowing to check connectivity and time sync before assuming the domain configuration itself is wrong is exactly the kind of instinct a service desk role needs.

## What's next

I'm planning to extend this into a hybrid identity setup — syncing this on-prem domain to Microsoft Entra ID using Azure AD Connect, and enabling MFA on a synced account. A lot of organisations run exactly this hybrid architecture, so it felt worth understanding both halves rather than just the on-prem side.
