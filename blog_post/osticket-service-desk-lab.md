# Building a Self-Hosted Service Desk in My Home Lab (osTicket + Active Directory)

## Why

While working through gap analyses against multiple job descriptions — Ramsdens, Barnsley College, a POS support role, an MSP 2nd line role, and a Brighouse IT support role — one requirement came up again and again: experience with a ticketing or service desk system. Nearly every IT support posting names logging, categorising, prioritising, and resolving tickets within SLA as a core expectation.

I already had a home lab running Active Directory (a Windows Server 2022 domain controller with Group Policy, and a domain-joined Windows 10 client), so rather than just reading about service desk workflows, I decided to deploy a real ticketing system alongside it and use it the way an actual first-line support role would — logging tickets against real infrastructure, triaging them, and working them through to resolution.

## The stack

- **VirtualBox** — a third VM added to my existing lab (domain controller + Windows 10 client)
- **Ubuntu Server 26.04 LTS** — chosen over a desktop OS since it mirrors how this would actually be hosted in a business environment, and it's lighter weight
- **Apache, MySQL, PHP 8.5** — the LAMP stack osTicket runs on
- **osTicket** (self-hosted, open source, latest release via `git clone` and osTicket's own `manage.php deploy` process) — chosen over a SaaS option like Freshservice specifically because deploying and network-integrating the platform myself is part of the skill being demonstrated, not just clicking through a hosted UI

## Deployment

The full deployment covered:

- Provisioning a new Ubuntu Server VM on the same internal network as the domain controller and Windows 10 client, so all three could communicate
- Installing and configuring Apache, MySQL, and PHP with the extensions osTicket requires (mysqli, gd, intl, apcu, xml, mbstring, curl)
- Creating a dedicated, least-privilege MySQL database and user for osTicket rather than using the MySQL root account
- Cloning osTicket from its official GitHub repository and deploying it into the Apache web root using osTicket's own `manage.php deploy` tooling
- Setting correct file ownership (`www-data`) and permissions for the web server, then locking the config file back down (`chmod 0644`) and removing the `/setup/` installer directory after installation — standard post-install hardening
- Running the web-based installer, connecting it to the database, and creating the admin agent account

One genuinely useful troubleshooting moment: my host machine couldn't reach the ticketing VM directly, because VirtualBox's NAT Network isolates guest VMs from the host by design. The fix — and the more realistic approach — was to browse to the service desk from the domain-joined Windows 10 client instead, exactly as an employee would access an internal tool from their work PC rather than from outside the network.

## Configuring it like a real service desk

A bare install isn't the point — the value is in the workflow. I configured:

**Departments**
- IT Support (general first-line queue)
- Security (kept separate from general IT support, reflecting how a security incident typically needs different handling and escalation than a routine access request)

**Help Topics**, each mapped to a department and a default priority:
- Account & Access — Normal priority
- Group Policy & Configuration — Normal priority
- Hardware & Peripherals — Low priority
- Security Incident — High priority

**SLA Plans**, tiered by urgency:
- Critical — 4 hour resolution target
- High Priority — 8 hours
- Standard — 18 hours
- Low Priority — 24 hours

Each SLA plan is linked to the matching help topic, so a ticket's priority automatically drives its resolution deadline — the same mechanism that underpins SLA compliance reporting on real service desks.

## Working a real ticket end to end

Rather than logging every ticket directly as an agent, I used osTicket's public-facing portal to submit the first ticket as a fictional end user would — a more realistic test of the full lifecycle than creating tickets purely from the staff side.

**Ticket #771657 — "can't log into computer"**

> *"I have tried to log into my computer but I have gotten the password wrong too many times and it has logged me out, please could you fix that for me."*

This ticket landed correctly in the IT Support queue under Account & Access, Normal priority, with an 18-hour SLA and a calculated due date. From the staff panel, I:

1. Claimed/assigned the ticket to myself
2. Logged an internal triage note *before* touching anything, documenting my working hypothesis:
   > "User reports repeated log in fails leading to them being locked out. Most likely AD account lockout policy. Will need to review security events for failed logon attempts."

This mirrors how a first-line technician should actually work a ticket — form a hypothesis from the symptoms described, then go verify it against the infrastructure, rather than guessing at a fix.

## What's next

This project is ongoing. The next stage is heading into the Active Directory lab itself to:

- Reproduce the lockout against a real domain account and confirm it against the domain's Account Lockout Policy
- Check the Security event log for the relevant lockout events (Event ID 4740) to evidence root cause, not just assume it
- Unlock the account, close the ticket out with a full resolution note, and confirm it landed within its SLA window

From there, I'm building out a wider set of realistic tickets across the categories configured above — including a Group Policy fault I'll deliberately introduce and diagnose, a couple of low-priority hardware tickets, a security incident (a reported phishing attempt), and at least one ticket I escalate rather than resolve outright, since real service desks don't close everything cleanly. I'll follow up with a second post once that set is complete, along with a look at overall SLA performance across the full ticket log.

---
*
