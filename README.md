# Module 08: Movie Review Platform

A complete movie review platform built progressively from frontend-only to full-stack with user submissions and admin verification.

## Theme
**Light Sky Blue** color scheme across all parts:
- Background: `#e8f4fc`
- Navbar/Footer: `#5dade2`
- Cards: White with `#aed6f1` border
- Primary buttons: `#3498db`
- Text: `#2c3e50`

## Project Structure

```
module-08-movie-review/
├── part-1-frontend-only/      # HTML/CSS/JS only, no backend
├── part-2-auth-admin/         # Flask + Auth + Admin CRUD
├── part-3-user-submissions/   # User submissions + verification
├── part-4-homework/           # Student exercises
└── README.md
```

## Quick Start

### Part 1 (No Backend)
```bash
cd part-1-frontend-only
# Open index.html in browser
# Enter your name once - it's saved for all future reviews
```

### Parts 2-4 (With Backend)
```bash
cd part-2-auth-admin  # or part-3 or part-4/starter-code
python -m venv venv
venv\Scripts\activate
pip install flask flask-sqlalchemy pyjwt werkzeug
python app.py
```

Open http://127.0.0.1:5000

## Default Admin
- Email: admin@moviehub.com
- Password: admin123

## Part Summary

| Part | Focus | Backend | User Name |
|------|-------|---------|-----------|
| 1 | HTML Templates, localStorage | No | Saved in localStorage |
| 2 | Auth, Admin CRUD, Reviews | Yes | From login |
| 3 | User Submissions, Verification | Yes | From login |
| 4 | Homework: Top Rated, Series | Yes | From login |

## Technologies
- Flask + SQLAlchemy
- JWT Authentication
- Bootstrap 5
- Vanilla JavaScript

## Features
- Movie listing with search/filter
- Star rating system (1-5 stars)
- User reviews (no need to enter name every time)
- Admin movie management (CRUD)
- User movie submissions
- Admin verification workflow
- Responsive design for all devices
- Light sky blue theme throughout
