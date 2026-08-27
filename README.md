# SkillX Backend

Student Skill Exchange Platform: skill listings, peer-to-peer session
booking, two-way ratings, milestone e-certificates, in-app notifications
and an admin analytics dashboard.

Stack: FastAPI + SQLAlchemy + MySQL. The frontend (HTML/CSS/JS) is served
by the same server from the `frontend/` folder.

## Request lifecycle

routes -> middleware -> controller -> service -> database

## Setup

Requirements: Python 3.11+, MySQL 8 (or XAMPP), a modern browser.

1. Extract the project and open a terminal inside the `skillx-backend`
   folder (the one containing `app/` and `requirements.txt`).

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```
   macOS/Linux: `source venv/bin/activate`

   If PowerShell blocks the script, run once:
   `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Start MySQL and create the database:
   ```sql
   CREATE DATABASE skillx_db;
   ```

5. Create your environment file and set your MySQL user and password:
   ```
   copy .env.example .env
   ```
   The password must match what MySQL Workbench uses to connect.
   No quotes, no spaces around `=`.

6. Create tables and load demo data. There are two ways to do this — either is
   fine, pick one:

   a. Restore `skillx_db.sql`, included in this folder. It holds the schema and
      the demo data exactly as the screenshots in the report show them, and
      creates the database itself, so step 4 can be skipped. Run it from inside
      this folder:
      ```
      mysql -u root -p < skillx_db.sql
      ```

   b. Or build it from the scripts instead:
      ```
      python database\migrations\create_tables.py
      python database\seeders\seed_data.py
      ```

7. Start the server:
   ```
   uvicorn app.main:app --reload
   ```

8. Open http://127.0.0.1:8000/ for the app and
   http://127.0.0.1:8000/docs for the API reference.

## Default accounts

| Role    | Email                   | Password   |
|---------|-------------------------|------------|
| Admin   | admin@skillx-demo.com   | admin123   |
| Student | aungkyaw@skillx-demo.com | student123 |
| Student | thirisan@skillx-demo.com | student123 |
| Student | hsumyat@skillx-demo.com  | student123 |

## Notifications

The project doesn't call any external service, so notifications stay inside
the app instead of being emailed: booking events (request, accept, decline,
complete, cancel, reschedule), certificate awards, and skill approval/
rejection all write to the `notifications` table and show up under Alerts in
the sidebar, with the unread count as a badge next to it.

## Password reset

There's no email service, so a student can't reset their own password purely
by themselves — but an admin never sets or sees it either. The student
requests a reset (`forgot-password.html`, email only) after verifying who
they are with an admin out-of-band (in person, chat, etc.). The admin
approves the request from `admin.html`'s Password reset requests panel — that
just unlocks the next step, it doesn't touch the password. The student then
comes back to `forgot-password.html` and sets their own new password, which
only they ever see. The approval window is 10 minutes
(`PASSWORD_RESET_WINDOW_MINUTES` in `.env`); after that the request shows as
expired and they need a fresh one.

## Complaints

A student can report a problem (tutor, learner or listing) from the "Report
a problem" panel on `profile.html`. It goes to the admin's Complaints view
in `admin.html`, where an admin writes a response and marks it resolved —
the student gets notified in-app either way.

## Screens

Every signed-in page shares one shell: a fixed sidebar (brand, the links for
that role, the unread alert badge, the account block and Log out) built by
`js/nav.js`, and a content area of white cards. Under 900px wide the sidebar
becomes a scrolling strip across the top. Login, registration and password
reset use a split layout instead, with the gradient artwork panel on the left
and the form on the right. `admin.html` is one page holding seven
`<section data-view="...">` blocks — Dashboard, Skill listings, Categories,
Students, Certificates, Complaints and Reports — and the sidebar switches
between them with `showView()`, so `admin.html#users` opens straight on the
Students view. All of the styling lives in `css/style.css`.

## Troubleshooting

- `Can't connect to MySQL server`: MySQL is not running, or DB_HOST/DB_PORT
  in `.env` is wrong.
- `Access denied for user`: DB_USER/DB_PASSWORD in `.env` does not match
  your MySQL account.
- `Address already in use`: another server is on port 8000. Run
  `uvicorn app.main:app --port 8001`.
- `ModuleNotFoundError`: the virtual environment is not activated.
- `uvicorn is not recognized`: dependencies not installed in the active
  environment. Activate the venv, then `pip install -r requirements.txt`.

## Project structure

```
skillx-backend/
├── app/
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── controllers/
│   ├── middleware/
│   ├── models/
│   ├── routes/
│   │   ├── api.py
│   │   └── public.py
│   ├── schemas/
│   ├── services/
│   └── utils/
├── frontend/
├── database/
│   ├── migrations/create_tables.py
│   └── seeders/seed_data.py
├── storage/materials/    (uploaded learning materials, not web-accessible)
├── tests/
└── README.md
```

## Features

Student: register, login, profile with picture and bio, browse and search
skills, skill detail with tutor ratings, offer/edit/delete skills with
availability slots, book sessions, accept/decline/reschedule/cancel/complete
bookings, two-way 5-star feedback, automatic PDF certificates every 5
completed sessions, upload/download learning materials for booked skills,
report a problem to an admin, in-app notifications.

Admin: approve/reject skills, manage students (suspend/reactivate, reset
password), manage categories, view and resolve student complaints, view
all session feedback, verify a certificate by code, analytics dashboard
(summary, total/completed bookings, top skills, top rated students, weekly
exchanges, average rating per category).

## Learning materials

A tutor can attach files (notes, slides, etc.) to a skill they teach from
`my_skills.html`. A learner can see and download them from a skill's page
once they have an active booking for it (declined/cancelled bookings don't
count). Files are stored under `storage/materials/`, outside `frontend/`,
so they're only reachable through the authenticated download endpoint
(`GET /api/materials/{id}/download`) — never served as a plain static file.

## Testing

Import `tests/postman_collection.json` into Postman and run the collection
against a freshly seeded database. Requests are grouped into one folder per
resource (auth, skills, materials, bookings, feedback, complaints,
certificates, admin, dashboard), each request named after the action it
performs; a variant that checks an error case is named the same way with a
short qualifier, e.g. `Register` / `Register (duplicate email)`. It can also
be run headlessly with [Newman](https://github.com/postmanlabs/newman):

```
npx newman run tests/postman_collection.json --env-var "base_url=http://127.0.0.1:8000"
```


## Team

Group 7, capstone module AAPP011-4-2.

| Name | Role |
|------|------|
| Lu Min Han | Project Leader, Integration and Final Documentation, Testing and QA, API |
| Zayar Naing | Skill Listing |
| Zaw | Database and Booking |
| Sean | Frontend and Certificate |
| Han Htut Naing | Feedback |
| Pathmarajah | Dashboard |
