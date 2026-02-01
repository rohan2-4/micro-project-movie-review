# Part 4: Homework Assignment

## Overview
Apply everything you've learned by implementing new features to the Movie Review Platform.

## Your Tasks

### Task 1: Top Rated Movies Section
**Goal:** Display top 10 movies by average rating on the home page.

**Requirements:**
- Create `/api/movies/top-rated` endpoint
- Calculate average rating for each movie
- Sort by average rating (highest first)
- Limit to top 10 movies
- Add "Top Rated" section on home page

**Hints:**
```python
# In app.py - Calculate average rating in query
from sqlalchemy import func

@app.route('/api/movies/top-rated', methods=['GET'])
def get_top_rated():
    # TODO: Query movies with their average rating
    # TODO: Sort by average rating DESC
    # TODO: Limit to 10
    pass
```

**In index.html:**
```html
<!-- Add before Featured Movies -->
<div class="container py-4">
    <h2>Top Rated Movies</h2>
    <div class="row" id="topRatedContainer"></div>
</div>
```

---

### Task 2: Content Type (Movie vs Series)
**Goal:** Add ability to distinguish between Movies and TV Series.

**Requirements:**
- Add `content_type` column to Movie model (`movie` or `series`)
- Update add/submit forms to include content type selector
- Add filter buttons for Movie/Series on movies page
- Display badge showing type (Movie/Series)

**Database Update (models.py):**
```python
class Movie(db.Model):
    # ... existing columns ...
    content_type = db.Column(db.String(10), default='movie')  # 'movie' or 'series'
```

**Note:** Delete `moviehub.db` after changing model, then restart app.

---

### Task 3: Filter by Content Type
**Goal:** Allow users to filter movies page by content type.

**Requirements:**
- Update `/api/movies` to accept `type` query parameter
- Add "Movies" and "Series" filter buttons on movies page
- Update category filter to work with type filter

**API Update:**
```python
@app.route('/api/movies', methods=['GET'])
def get_movies():
    category = request.args.get('category', '')
    search = request.args.get('search', '')
    content_type = request.args.get('type', '')  # TODO: Add this

    query = Movie.query.filter_by(is_verified=True)
    # TODO: Filter by content_type if provided
```

---

### Bonus Task: Trending Movies
**Goal:** Show movies with most reviews in last 7 days.

**Requirements:**
- Create `/api/movies/trending` endpoint
- Count reviews from last 7 days per movie
- Sort by review count
- Display on home page

**Hint:**
```python
from datetime import datetime, timedelta

seven_days_ago = datetime.utcnow() - timedelta(days=7)
# Query reviews created after seven_days_ago
```

---

## Getting Started

1. Navigate to `starter-code` folder
2. Set up virtual environment
3. Install dependencies
4. Run the app
5. Implement each task one by one
6. Test thoroughly

```bash
cd part-4-homework/starter-code
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

## Submission Checklist

- [ ] Task 1: Top Rated endpoint works
- [ ] Task 1: Top Rated section displays on home page
- [ ] Task 2: content_type column added to Movie model
- [ ] Task 2: Forms include content type selector
- [ ] Task 2: Badge shows Movie/Series
- [ ] Task 3: Filter by type works on movies page
- [ ] Bonus: Trending movies section (optional)

## Tips

- Test each feature after implementing
- Use browser DevTools to debug API calls
- Check console for JavaScript errors
- Delete database file if model changes don't reflect

## Expected Result

After completing all tasks:
- Home page shows "Top Rated" section with best movies
- Users can choose Movie/Series when submitting
- Movies page has Movie/Series filter buttons
- Each movie card shows type badge
