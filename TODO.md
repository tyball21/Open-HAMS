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

### Animal Management ✅ P1
- **Animal Creation 422 Error Fix:** Resolve "Unprocessable Entity" errors when creating animals. ✅ P0
  - *Issue:* Frontend sending FormData but axios forcing `Content-Type: application/json`, causing validation failures.
  - *Root Causes Fixed:*
    - FormData/JSON content-type mismatch in axios configuration
    - Permission function signature errors (`has_permission` parameters)
    - Audit logging parameter mismatch (`user_id` vs `changed_by`)
    - Greenlet async context issues in audit logging
  - *Note:* Fixed in axios.ts, animals.py routes. All animals now create successfully. Completed 2024-12-16.
- **Animal Image Display Fix:** Images not showing in frontend UI. ✅ P1
  - *Issue:* Frontend using relative URLs (`/static/`) pointing to frontend server instead of backend.
  - *Fix:* Updated all image references to use `${API_URL}/static/animal_images/` for environment-agnostic URLs.
  - *Components Updated:* animals-table/cols.tsx, animal details page, event models, animals-select.tsx
  - *Note:* Works with both local development and production S3 deployments. Completed 2024-12-16.
- **Photo Upload:** Allow direct upload from computer. ✅ P1
  - *Issue:* Currently only online photos can be uploaded.
  - *Note:* Backend routes updated to handle file uploads. Frontend workaround `(object as any)["image_filename"] || (object as any)["image"]` still in place due to potential schema drift. ⚠️ Tech debt: Update OpenAPI types when schema stabilizes.
- **Max Checkout Hours:** Make field optional in database and model. ✅ P1
  - *Issue:* Previously mandatory, not needed for multi-day checkouts.
  - *Note:* Made nullable via migration `8484acd9b492`. Backend model `AnimalIn` updated. Frontend form schema (`animalSchema`) updated to optional.
- **Rest Time Requirement:** Remove mandatory field from animal creation. ✅ P1
  - *Issue:* Determined by offsite status and handling frequency.
  - *Note:* Made optional in backend model (`AnimalIn`) and frontend schema (`animalSchema`).
- **Zoo Naming Consistency:** Update all "Hogle Zoo" instances to "Utah's Hogle Zoo." ✅ P1
  - *Issue:* Inconsistent naming.
  - *Note:* Updated in config, frontend layouts, and README copyright notice.
- **Animal Creation Form Improvements:** ✅ P1
  - Make non-critical fields optional. ✅ P1
    - *Issue:* Some fields were required.
    - *Note:* `description`, `image`, `rest_time`, `max_daily_checkout_hours` made optional in frontend schema (`animalSchema`). Corresponding backend models also updated.
  - Remove/modify auto-generated sequential ID display. ✅ P1
    - *Issue:* Potential user confusion with zoo's specific IDs.
    - *Note:* Renamed column header in animals table to "System ID" for clarity.

### Event Management ✅ P1
- **Event Creation Adjustments:** ✅ P1
  - Make event description optional. ✅ P1
    - *Issue:* Description currently mandatory.
    - *Note:* Made description field optional in `EventIn` model, created database migration (`702fbe8a9c35`), and updated frontend Zod schema.
  - Allow future reservations for currently checked-out animals. 🆕 P1
    - *Issue:* Cannot reserve if animal is currently checked out.
- **Dashboard and Event Functionality:** ✅ P1
  - Clarify "live events" definition on dashboard. ✅ P1
    - *Issue:* Unclear definition.
    - *Note:* Added tooltip to "Live Events" heading explaining these are "Events currently in progress".
  - Redirect to dashboard after event deletion. ✅ P1
    - *Issue:* No redirection currently.
    - *Note:* Added navigation to dashboard (`navigate("/dashboard")`) after successful event deletion.
  - Enable editing of event start times post-creation. 🆕 P1
    - *Issue:* Cannot change start time after creation.
  - Fix 12PM reverting to 12AM time entry issue. ✅ P1
    - *Issue:* Incorrect time handling.
    - *Note:* Fixed the `convert12HourTo24Hour` function logic and updated period handling in the `TimePeriodSelect` component.
  - Auto-check-in animals when their event is deleted. ✅ P1
    - *Issue:* Animals remain checked out if event is deleted.
    - *Note:* Modified the `delete_event` endpoint to automatically check in any animals that are currently checked out before deleting the event.

### Event Date Handling Improvements ✅ P0
- **Allow Same-Day Event Creation:** ✅ P0
  - *Issue:* System rejects events with start times that appear to have already passed, preventing same-day event creation.
  - *Implementation:*
    - Modified date validation in `eventSchema` to allow same-day events with future start times
    - Added smarter validation that specifically checks combined date+time for today's events
    - Added `superRefine` validation to ensure start time is in the future for same-day events
  
- **Simplify One-Day Events:** ✅ P0
  - *Issue:* Setting identical start and end dates (e.g., March 7-7) behaves strangely.
  - *Implementation:*
    - Enhanced `DatePickerWithRange` component with "One-day event" checkbox option
    - When checked, the component auto-sets the end date to match the start date
    - Added validation for one-day events to ensure end time is after start time
    - Improved display to show only one date when start and end dates are the same