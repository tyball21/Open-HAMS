# [Project Name] TODO

> **Life‑Cycle Rules**
> • Keep this file for *active* work only.
> • When an item is done, mark ✅ and migrate the full block to **COMPLETED.md** (with a date).
> • Tag every open task with **Status** and **Priority** so sorting and filters work.

## Legend
| Status | Meaning |
| ------ | ------- |
| 🆕 NEW | just landed |
| 🚧 IN PROGRESS | currently being worked |
| ⏸ BLOCKED | awaiting input/dependency |
| 💤 PENDING | scheduled but idle |

| Priority | Meaning |
| -------- | ------- |
| P0 | must ship / blocker |
| P1 | important |
| P2 | nice‑to‑have |
| P3 | backlog / someday |

---

## Table of Contents
1. [Overview](#overview)
2. [Components](#components)

## Overview ✅
Brief one‑liner on purpose, vision, and success criteria.

---

## Components 🆕
Break the product into logical chunks. Nest features → tasks.

### Animal Management 🆕 P1
- **Photo Upload:** Allow direct upload from computer. 🆕 P1
  - *Issue:* Currently only online photos can be uploaded.
- **Max Checkout Hours:** Remove field unless needed for defined auto-check-in. 🆕 P1
  - *Issue:* Not needed for multi-day checkouts.
- **Rest Time Requirement:** Remove mandatory field from animal creation. 🆕 P1
  - *Issue:* Determined by offsite status and handling frequency.
- **Zoo Naming Consistency:** Update all "Hogle Zoo" instances to "Utah's Hogle Zoo." 🆕 P1
  - *Issue:* Inconsistent naming.
- **Animal Creation Form Improvements:** 🆕 P1
  - Make non-critical fields optional. 🆕 P1
    - *Issue:* All fields currently required.
  - Remove/modify auto-generated sequential ID display. 🆕 P1
    - *Issue:* Potential user confusion with zoo's specific IDs.

### Event Management 🆕 P1
- **Event Creation Adjustments:** 🆕 P1
  - Make event description optional. 🆕 P1
    - *Issue:* Description currently mandatory.
  - Allow future reservations for currently checked-out animals. 🆕 P1
    - *Issue:* Cannot reserve if animal is currently checked out.
- **Dashboard and Event Functionality:** 🆕 P1
  - Clarify "live events" definition on dashboard. 🆕 P1
    - *Issue:* Unclear definition.
  - Redirect to dashboard after event deletion. 🆕 P1
    - *Issue:* No redirection currently.
  - Enable editing of event start times post-creation. 🆕 P1
    - *Issue:* Cannot change start time after creation.
  - Fix 12PM reverting to 12AM time entry issue. 🆕 P1
    - *Issue:* Incorrect time handling.
  - Auto-check-in animals when their event is deleted. 🆕 P1
    - *Issue:* Animals remain checked out if event is deleted.