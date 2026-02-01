// data.js - Dummy Movies and Reviews Data

// Dummy Movies Data
const movies = [
    {
        id: 1,
        title: "The Dark Knight",
        category: "Action",
        poster: "https://m.media-amazon.com/images/M/MV5BMTMxNTMwODM0NF5BMl5BanBnXkFtZTcwODAyMTk2Mw@@._V1_.jpg",
        year: 2008,
        description: "When the menace known as the Joker wreaks havoc and chaos on the people of Gotham, Batman must accept one of the greatest psychological and physical tests of his ability to fight injustice."
    },
    {
        id: 2,
        title: "Inception",
        category: "Sci-Fi",
        poster: "https://m.media-amazon.com/images/M/MV5BMjAxMzY3NjcxNF5BMl5BanBnXkFtZTcwNTI5OTM0Mw@@._V1_.jpg",
        year: 2010,
        description: "A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea into the mind of a C.E.O."
    },
    {
        id: 3,
        title: "The Hangover",
        category: "Comedy",
        poster: "https://m.media-amazon.com/images/M/MV5BNGQwZjg5YmYtY2VkNC00NzliLTljYTctNzI5NmU3MjE2ODQzXkEyXkFqcGdeQXVyNzkwMjQ5NzM@._V1_.jpg",
        year: 2009,
        description: "Three buddies wake up from a bachelor party in Las Vegas, with no memory of the previous night and the bachelor missing."
    },
    {
        id: 4,
        title: "The Conjuring",
        category: "Horror",
        poster: "https://m.media-amazon.com/images/M/MV5BMTM3NjA1NDMyMV5BMl5BanBnXkFtZTcwMDQzNDMzOQ@@._V1_.jpg",
        year: 2013,
        description: "Paranormal investigators Ed and Lorraine Warren work to help a family terrorized by a dark presence in their farmhouse."
    },
    {
        id: 5,
        title: "The Shawshank Redemption",
        category: "Drama",
        poster: "https://m.media-amazon.com/images/M/MV5BNDE3ODcxYzMtY2YzZC00NmNlLWJiNDMtZDViZWM2MzIxZDYwXkEyXkFqcGdeQXVyNjAwNDUxODI@._V1_.jpg",
        year: 1994,
        description: "Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency."
    },
    {
        id: 6,
        title: "Avengers: Endgame",
        category: "Action",
        poster: "https://m.media-amazon.com/images/M/MV5BMTc5MDE2ODcwNV5BMl5BanBnXkFtZTgwMzI2NzQ2NzM@._V1_.jpg",
        year: 2019,
        description: "After the devastating events of Infinity War, the universe is in ruins. With the help of remaining allies, the Avengers assemble once more."
    },
    {
        id: 7,
        title: "Interstellar",
        category: "Sci-Fi",
        poster: "https://m.media-amazon.com/images/M/MV5BZjdkOTU3MDktN2IxOS00OGEyLWFmMjktY2FiMmZkNWIyODZiXkEyXkFqcGdeQXVyMTMxODk2OTU@._V1_.jpg",
        year: 2014,
        description: "A team of explorers travel through a wormhole in space in an attempt to ensure humanity's survival."
    },
    {
        id: 8,
        title: "Superbad",
        category: "Comedy",
        poster: "https://m.media-amazon.com/images/M/MV5BY2VkMDg4ZTYtN2M3Yy00NWZhLWE0NTAtMDQxZjhlMTI5NTc4XkEyXkFqcGdeQXVyODY5Njk4Njc@._V1_.jpg",
        year: 2007,
        description: "Two co-dependent high school seniors are forced to deal with separation anxiety after their plan to score alcohol for a party goes awry."
    }
];

// Dummy Reviews Data (initial)
const initialReviews = [
    { id: 1, movieId: 1, reviewerName: "John", rating: 5, content: "Best superhero movie ever! Heath Ledger was amazing.", date: "2024-01-15" },
    { id: 2, movieId: 1, reviewerName: "Sarah", rating: 5, content: "A masterpiece of cinema. The Joker steals every scene.", date: "2024-01-10" },
    { id: 3, movieId: 2, reviewerName: "Mike", rating: 4, content: "Mind-bending plot that keeps you thinking.", date: "2024-01-12" },
    { id: 4, movieId: 3, reviewerName: "Emma", rating: 4, content: "Hilarious from start to finish!", date: "2024-01-08" },
    { id: 5, movieId: 4, reviewerName: "Alex", rating: 5, content: "Genuinely scary! Couldn't sleep for days.", date: "2024-01-05" },
    { id: 6, movieId: 5, reviewerName: "Chris", rating: 5, content: "A beautiful story of hope and friendship.", date: "2024-01-03" },
    { id: 7, movieId: 6, reviewerName: "Lisa", rating: 4, content: "Epic conclusion to the saga!", date: "2024-01-01" },
    { id: 8, movieId: 7, reviewerName: "David", rating: 5, content: "Visually stunning and emotionally powerful.", date: "2023-12-28" }
];

// Initialize reviews in localStorage if not exists
function initReviews() {
    if (!localStorage.getItem('movieReviews')) {
        localStorage.setItem('movieReviews', JSON.stringify(initialReviews));
    }
}

// Get all reviews from localStorage
function getReviews() {
    initReviews();
    return JSON.parse(localStorage.getItem('movieReviews'));
}

// Add a new review
function addReview(movieId, reviewerName, rating, content) {
    const reviews = getReviews();
    const newReview = {
        id: Date.now(),
        movieId: parseInt(movieId),
        reviewerName: reviewerName,
        rating: parseInt(rating),
        content: content,
        date: new Date().toISOString().split('T')[0]
    };
    reviews.push(newReview);
    localStorage.setItem('movieReviews', JSON.stringify(reviews));
    return newReview;
}

// Get reviews for a specific movie
function getMovieReviews(movieId) {
    return getReviews().filter(r => r.movieId === parseInt(movieId));
}

// Get movie by ID
function getMovieById(id) {
    return movies.find(m => m.id === parseInt(id));
}

// Delete a review
function deleteReview(reviewId) {
    let reviews = getReviews();
    reviews = reviews.filter(r => r.id !== reviewId);
    localStorage.setItem('movieReviews', JSON.stringify(reviews));
}

// Clear all reviews (reset to initial)
function resetReviews() {
    localStorage.setItem('movieReviews', JSON.stringify(initialReviews));
}
