# Part 2: Authentication & Admin Panel

## Overview
Add Flask backend with user authentication and admin functionality to manage movies.

## Features
- User registration and login with JWT
- Protected routes with @token_required
- Admin-only routes with @admin_required
- Admin can add/edit/delete movies
- Users can write reviews (one per movie)
- Search and filter movies by category
- User dashboard to view own reviews

## Files
```
part-2-auth-admin/
├── app.py              # Flask app with all routes
├── models.py           # User, Movie, Review models
├── auth.py             # JWT helpers and decorators
├── requirements.txt
├── templates/
│   ├── index.html      # Home page
│   ├── movies.html     # All movies
│   ├── movie.html      # Movie detail + reviews
│   ├── login.html      # Login form
│   ├── register.html   # Registration form
│   ├── dashboard.html  # User's reviews
│   └── admin.html      # Admin panel
└── README.md
```

## How to Run
```bash
cd part-2-auth-admin
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
python app.py
```

Open http://127.0.0.1:5000

## Default Admin
- Email: admin@moviehub.com
- Password: admin123
- Click "Create Admin" button or POST to /api/create-admin

## API Endpoints

### Auth
| Route | Method | Description |
|-------|--------|-------------|
| /api/register | POST | Register user |
| /api/login | POST | Login, get token |
| /api/create-admin | POST | Create admin account |

### Movies
| Route | Method | Auth | Description |
|-------|--------|------|-------------|
| /api/movies | GET | No | List movies |
| /api/movies/:id | GET | No | Get movie details |
| /api/movies | POST | Admin | Add movie |
| /api/movies/:id | PUT | Admin | Update movie |
| /api/movies/:id | DELETE | Admin | Delete movie |
| /api/categories | GET | No | List categories |

### Reviews
| Route | Method | Auth | Description |
|-------|--------|------|-------------|
| /api/movies/:id/reviews | GET | No | Get reviews |
| /api/movies/:id/reviews | POST | User | Add review |
| /api/reviews/:id | DELETE | User/Admin | Delete review |
| /api/my-reviews | GET | User | Get own reviews |

## Key Learnings
- Flask backend with SQLAlchemy ORM
- JWT token authentication
- Password hashing with Werkzeug
- Role-based access control
- Protected API routes with decorators
- One-to-Many relationships (User -> Reviews, Movie -> Reviews)

## Exercises

### Exercise 1: Edit Review
Add PUT /api/reviews/:id route to edit review content and rating.

### Exercise 2: User Profile
Add /api/profile route to get/update user profile (username, email).

### Exercise 3: Movie Stats
Add /api/movies/:id/stats route returning total reviews, avg rating, rating distribution.
