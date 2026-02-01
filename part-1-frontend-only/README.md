# Part 1: Frontend Only

## Overview
Build complete UI for the Movie Review Platform using only HTML, CSS, and JavaScript. No backend required.

## Features
- Responsive movie listing with Bootstrap 5
- Movie detail page with reviews
- Star rating system (1-5 stars)
- Search movies by title
- Filter movies by category
- Reviews stored in localStorage
- Dummy movie data in JavaScript

## Files
```
part-1-frontend-only/
├── index.html      # Home page with featured movies
├── movies.html     # All movies with filters
├── movie.html      # Movie detail + reviews
├── about.html      # About page
├── data.js         # Dummy data + localStorage functions
└── README.md
```

## How to Run
1. Open `index.html` in your browser
2. Or use Live Server extension in VS Code

## Pages

### Home (index.html)
- Hero section with search box
- Featured movies grid
- Category filter dropdown

### All Movies (movies.html)
- Complete movie listing
- Category filter buttons
- Search by title
- Movie count display

### Movie Detail (movie.html)
- Movie poster and info
- Average rating display
- Review form (name, rating, review)
- List of all reviews

### About (about.html)
- Platform features
- Current stats (movies, reviews)

## Key Learnings
- HTML structure for movie cards
- Bootstrap 5 grid system
- CSS custom properties for theming
- localStorage for data persistence
- JavaScript DOM manipulation
- URL parameters for page navigation
- Star rating with CSS

## Exercises

### Exercise 1: Add Movie Year Filter
Add a year filter dropdown to filter movies by release year.

### Exercise 2: Sort Reviews
Add buttons to sort reviews by date or rating.

### Exercise 3: Edit/Delete Reviews
Add edit and delete buttons to each review card.
