# Part 3: User Movie Submissions & Admin Verification

## Overview
Allow users to submit movies that are not on the platform. Admin reviews and verifies submissions before they appear publicly.

## Features
- Users can submit movies for verification
- Duplicate check before submission
- Movies have is_verified status
- Only verified movies shown to users
- Admin sees pending verification queue
- Admin can verify or reject submissions
- Track who submitted each movie
- Users can view their submission status

## Files
```
part-3-user-submissions/
├── app.py              # Flask app with submission routes
├── models.py           # Models with is_verified, submitted_by
├── auth.py             # JWT helpers and decorators
├── requirements.txt
├── templates/
│   ├── index.html      # Home with submit movie link
│   ├── movies.html     # All verified movies
│   ├── movie.html      # Movie detail + reviews
│   ├── login.html      # Login form
│   ├── register.html   # Registration form
│   ├── dashboard.html  # User's reviews
│   ├── submit_movie.html  # Submit movie form
│   └── admin.html      # Admin with pending verification
└── README.md
```

## How to Run
```bash
cd part-3-user-submissions
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Open http://127.0.0.1:5000

## New API Endpoints

### User Submission
| Route | Method | Auth | Description |
|-------|--------|------|-------------|
| /api/movies/check | POST | User | Check if movie exists |
| /api/movies/submit | POST | User | Submit movie for verification |
| /api/my-submissions | GET | User | View my submissions |

### Admin Verification
| Route | Method | Auth | Description |
|-------|--------|------|-------------|
| /api/admin/pending | GET | Admin | Get pending movies |
| /api/admin/verify/:id | POST | Admin | Verify movie |
| /api/admin/reject/:id | DELETE | Admin | Reject movie |
| /api/admin/all-movies | GET | Admin | Get all movies (verified + pending) |

## Database Changes
```python
class Movie:
    is_verified = db.Column(db.Boolean, default=False)
    submitted_by = db.Column(db.Integer, db.ForeignKey('users.id'))
```

## User Flow
1. User searches for movie
2. Movie not found -> Click "Submit Movie"
3. Check if movie exists (duplicate check)
4. Fill form: title, category, year, poster URL
5. Submit for verification
6. View submission status in "My Submissions"
7. Admin verifies -> Movie appears on platform

## Admin Flow
1. See pending count in stats
2. Go to "Pending Verification" tab
3. View movie details and submitter
4. Click "Verify" to approve
5. Click "Reject" to delete submission

## Key Learnings
- Content moderation workflow
- Duplicate detection with ilike
- Status-based filtering
- User-generated content management
- Admin verification queue

## Exercises

### Exercise 1: Edit Submission
Allow users to edit their pending submissions (not verified ones).

### Exercise 2: Rejection Reason
Add rejection reason field, notify user why submission was rejected.

### Exercise 3: Auto-Verify Trusted Users
After 5 successful verifications, auto-verify user's future submissions.
