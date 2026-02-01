# app.py - Movie Review Platform with User Submissions

from flask import Flask, render_template, request, jsonify
from models import db, init_db, User, Movie, Review
from auth import hash_password, verify_password, create_token, token_required, admin_required

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///moviehub.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'movie-hub-secret-key-change-in-production'

init_db(app)


# Page Routes
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/movies')
def movies_page():
    return render_template('movies.html')

@app.route('/movie/<int:movie_id>')
def movie_detail(movie_id):
    return render_template('movie.html', movie_id=movie_id)

@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/register')
def register_page():
    return render_template('register.html')

@app.route('/dashboard')
def dashboard_page():
    return render_template('dashboard.html')

@app.route('/submit-movie')
def submit_movie_page():
    return render_template('submit_movie.html')

@app.route('/admin')
def admin_page():
    return render_template('admin.html')


# Auth API
@app.route('/api/register', methods=['POST'])
def api_register():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    username, email, password = data.get('username'), data.get('email'), data.get('password')
    if not username or not email or not password:
        return jsonify({'error': 'All fields required'}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'Email already registered'}), 400
    if User.query.filter_by(username=username).first():
        return jsonify({'error': 'Username already taken'}), 400

    user = User(username=username, email=email, password_hash=hash_password(password), is_admin=False)
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully'}), 201


@app.route('/api/login', methods=['POST'])
def api_login():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    email, password = data.get('email'), data.get('password')
    if not email or not password:
        return jsonify({'error': 'Email and password required'}), 400

    user = User.query.filter_by(email=email).first()
    if not user or not verify_password(user.password_hash, password):
        return jsonify({'error': 'Invalid credentials'}), 401

    token = create_token(user.id, user.is_admin)
    return jsonify({'token': token, 'user': user.to_dict()}), 200


@app.route('/api/create-admin', methods=['POST'])
def create_admin():
    if User.query.filter_by(email='admin@moviehub.com').first():
        return jsonify({'message': 'Admin exists', 'email': 'admin@moviehub.com', 'password': 'admin123'}), 200

    admin = User(username='admin', email='admin@moviehub.com', password_hash=hash_password('admin123'), is_admin=True)
    db.session.add(admin)
    db.session.commit()
    return jsonify({'message': 'Admin created', 'email': 'admin@moviehub.com', 'password': 'admin123'}), 201


# Movies API (only verified movies shown to users)
@app.route('/api/movies', methods=['GET'])
def get_movies():
    category = request.args.get('category', '')
    search = request.args.get('search', '')

    query = Movie.query.filter_by(is_verified=True)  # Only verified movies
    if category:
        query = query.filter_by(category=category)
    if search:
        query = query.filter(Movie.title.ilike(f'%{search}%'))

    movies = query.all()
    return jsonify({'movies': [m.to_dict_with_rating() for m in movies]}), 200


@app.route('/api/movies/<int:movie_id>', methods=['GET'])
def get_movie(movie_id):
    movie = Movie.query.get(movie_id)
    if not movie:
        return jsonify({'error': 'Movie not found'}), 404
    if not movie.is_verified:
        return jsonify({'error': 'Movie not available'}), 404
    return jsonify({'movie': movie.to_dict_with_rating()}), 200


@app.route('/api/movies', methods=['POST'])
@admin_required
def add_movie(current_user):  # Admin: Add verified movie
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    title, category, poster_url, year = data.get('title'), data.get('category'), data.get('poster_url'), data.get('year')
    if not title or not category or not poster_url or not year:
        return jsonify({'error': 'All fields required'}), 400

    movie = Movie(title=title, category=category, poster_url=poster_url, year=year, description=data.get('description', ''), is_verified=True)
    db.session.add(movie)
    db.session.commit()
    return jsonify({'message': 'Movie added', 'movie': movie.to_dict()}), 201


@app.route('/api/movies/<int:movie_id>', methods=['PUT'])
@admin_required
def update_movie(current_user, movie_id):
    movie = Movie.query.get(movie_id)
    if not movie:
        return jsonify({'error': 'Movie not found'}), 404

    data = request.get_json()
    if 'title' in data:
        movie.title = data['title']
    if 'category' in data:
        movie.category = data['category']
    if 'poster_url' in data:
        movie.poster_url = data['poster_url']
    if 'year' in data:
        movie.year = data['year']
    if 'description' in data:
        movie.description = data['description']

    db.session.commit()
    return jsonify({'message': 'Movie updated', 'movie': movie.to_dict()}), 200


@app.route('/api/movies/<int:movie_id>', methods=['DELETE'])
@admin_required
def delete_movie(current_user, movie_id):
    movie = Movie.query.get(movie_id)
    if not movie:
        return jsonify({'error': 'Movie not found'}), 404

    Review.query.filter_by(movie_id=movie_id).delete()
    db.session.delete(movie)
    db.session.commit()
    return jsonify({'message': 'Movie deleted'}), 200


@app.route('/api/categories', methods=['GET'])
def get_categories():
    categories = db.session.query(Movie.category).filter_by(is_verified=True).distinct().all()
    return jsonify({'categories': [c[0] for c in categories]}), 200


# User Movie Submission
@app.route('/api/movies/check', methods=['POST'])
@token_required
def check_movie_exists(current_user):  # Check if movie already exists
    data = request.get_json()
    title = data.get('title', '').strip()
    if not title:
        return jsonify({'error': 'Title required'}), 400

    existing = Movie.query.filter(Movie.title.ilike(title)).first()
    if existing:
        return jsonify({'exists': True, 'message': f'Movie "{existing.title}" already exists!', 'is_verified': existing.is_verified}), 200
    return jsonify({'exists': False}), 200


@app.route('/api/movies/submit', methods=['POST'])
@token_required
def submit_movie(current_user):  # User submits movie for verification
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    title, category, poster_url, year = data.get('title'), data.get('category'), data.get('poster_url'), data.get('year')
    if not title or not category or not poster_url or not year:
        return jsonify({'error': 'All fields required'}), 400

    # Check if movie exists
    existing = Movie.query.filter(Movie.title.ilike(title.strip())).first()
    if existing:
        return jsonify({'error': f'Movie "{existing.title}" already exists!'}), 400

    movie = Movie(
        title=title.strip(),
        category=category,
        poster_url=poster_url,
        year=year,
        description=data.get('description', ''),
        is_verified=False,  # Pending verification
        submitted_by=current_user.id
    )
    db.session.add(movie)
    db.session.commit()
    return jsonify({'message': 'Movie submitted for verification', 'movie': movie.to_dict()}), 201


@app.route('/api/my-submissions', methods=['GET'])
@token_required
def get_my_submissions(current_user):  # Get user's submitted movies
    movies = Movie.query.filter_by(submitted_by=current_user.id).all()
    return jsonify({'movies': [m.to_dict() for m in movies]}), 200


# Admin: Pending Movies
@app.route('/api/admin/pending', methods=['GET'])
@admin_required
def get_pending_movies(current_user):  # Get unverified movies
    movies = Movie.query.filter_by(is_verified=False).all()
    return jsonify({'movies': [m.to_dict() for m in movies]}), 200


@app.route('/api/admin/verify/<int:movie_id>', methods=['POST'])
@admin_required
def verify_movie(current_user, movie_id):  # Approve movie
    movie = Movie.query.get(movie_id)
    if not movie:
        return jsonify({'error': 'Movie not found'}), 404

    movie.is_verified = True
    db.session.commit()
    return jsonify({'message': 'Movie verified', 'movie': movie.to_dict()}), 200


@app.route('/api/admin/reject/<int:movie_id>', methods=['DELETE'])
@admin_required
def reject_movie(current_user, movie_id):  # Reject and delete movie
    movie = Movie.query.get(movie_id)
    if not movie:
        return jsonify({'error': 'Movie not found'}), 404

    db.session.delete(movie)
    db.session.commit()
    return jsonify({'message': 'Movie rejected'}), 200


@app.route('/api/admin/all-movies', methods=['GET'])
@admin_required
def get_all_movies_admin(current_user):  # Admin sees all movies
    movies = Movie.query.all()
    return jsonify({'movies': [m.to_dict_with_rating() for m in movies]}), 200


# Reviews API
@app.route('/api/movies/<int:movie_id>/reviews', methods=['GET'])
def get_reviews(movie_id):
    reviews = Review.query.filter_by(movie_id=movie_id).order_by(Review.created_at.desc()).all()
    return jsonify({'reviews': [r.to_dict() for r in reviews]}), 200


@app.route('/api/movies/<int:movie_id>/reviews', methods=['POST'])
@token_required
def add_review(current_user, movie_id):
    movie = Movie.query.get(movie_id)
    if not movie or not movie.is_verified:
        return jsonify({'error': 'Movie not found'}), 404

    data = request.get_json()
    if not data or not data.get('content') or not data.get('rating'):
        return jsonify({'error': 'Content and rating required'}), 400

    rating = int(data['rating'])
    if rating < 1 or rating > 5:
        return jsonify({'error': 'Rating must be between 1 and 5'}), 400

    existing = Review.query.filter_by(movie_id=movie_id, user_id=current_user.id).first()
    if existing:
        return jsonify({'error': 'You have already reviewed this movie'}), 400

    review = Review(content=data['content'], rating=rating, movie_id=movie_id, user_id=current_user.id)
    db.session.add(review)
    db.session.commit()
    return jsonify({'message': 'Review added', 'review': review.to_dict()}), 201


@app.route('/api/reviews/<int:review_id>', methods=['DELETE'])
@token_required
def delete_review(current_user, review_id):
    review = Review.query.get(review_id)
    if not review:
        return jsonify({'error': 'Review not found'}), 404

    if review.user_id != current_user.id and not current_user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403

    db.session.delete(review)
    db.session.commit()
    return jsonify({'message': 'Review deleted'}), 200


@app.route('/api/my-reviews', methods=['GET'])
@token_required
def get_my_reviews(current_user):
    reviews = Review.query.filter_by(user_id=current_user.id).all()
    result = []
    for r in reviews:
        data = r.to_dict()
        data['movie_title'] = r.movie.title
        result.append(data)
    return jsonify({'reviews': result}), 200


# Admin Stats
@app.route('/api/admin/stats', methods=['GET'])
@admin_required
def get_admin_stats(current_user):
    return jsonify({
        'total_users': User.query.count(),
        'total_movies': Movie.query.filter_by(is_verified=True).count(),
        'pending_movies': Movie.query.filter_by(is_verified=False).count(),
        'total_reviews': Review.query.count()
    }), 200


if __name__ == '__main__':
    print("\nMovieHub - Part 4: Homework")
    print("http://127.0.0.1:5000")
    print("Admin: admin@moviehub.com / admin123\n")
    app.run(debug=True)
