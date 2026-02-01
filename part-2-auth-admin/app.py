# app.py - Movie Review Platform with Auth

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


# Movies API
@app.route('/api/movies', methods=['GET'])
def get_movies():
    category = request.args.get('category', '')
    search = request.args.get('search', '')

    query = Movie.query
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
    return jsonify({'movie': movie.to_dict_with_rating()}), 200


@app.route('/api/movies', methods=['POST'])
@admin_required
def add_movie(current_user):  # Admin only: Add new movie
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    title, category, poster_url, year = data.get('title'), data.get('category'), data.get('poster_url'), data.get('year')
    if not title or not category or not poster_url or not year:
        return jsonify({'error': 'All fields required'}), 400

    movie = Movie(title=title, category=category, poster_url=poster_url, year=year, description=data.get('description', ''))
    db.session.add(movie)
    db.session.commit()
    return jsonify({'message': 'Movie added', 'movie': movie.to_dict()}), 201


@app.route('/api/movies/<int:movie_id>', methods=['PUT'])
@admin_required
def update_movie(current_user, movie_id):  # Admin only: Update movie
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
def delete_movie(current_user, movie_id):  # Admin only: Delete movie
    movie = Movie.query.get(movie_id)
    if not movie:
        return jsonify({'error': 'Movie not found'}), 404

    Review.query.filter_by(movie_id=movie_id).delete()  # Delete related reviews
    db.session.delete(movie)
    db.session.commit()
    return jsonify({'message': 'Movie deleted'}), 200


@app.route('/api/categories', methods=['GET'])
def get_categories():
    categories = db.session.query(Movie.category).distinct().all()
    return jsonify({'categories': [c[0] for c in categories]}), 200


# Reviews API
@app.route('/api/movies/<int:movie_id>/reviews', methods=['GET'])
def get_reviews(movie_id):
    reviews = Review.query.filter_by(movie_id=movie_id).order_by(Review.created_at.desc()).all()
    return jsonify({'reviews': [r.to_dict() for r in reviews]}), 200


@app.route('/api/movies/<int:movie_id>/reviews', methods=['POST'])
@token_required
def add_review(current_user, movie_id):  # User only: Add review
    movie = Movie.query.get(movie_id)
    if not movie:
        return jsonify({'error': 'Movie not found'}), 404

    data = request.get_json()
    if not data or not data.get('content') or not data.get('rating'):
        return jsonify({'error': 'Content and rating required'}), 400

    rating = int(data['rating'])
    if rating < 1 or rating > 5:
        return jsonify({'error': 'Rating must be between 1 and 5'}), 400

    # Check if user already reviewed this movie
    existing = Review.query.filter_by(movie_id=movie_id, user_id=current_user.id).first()
    if existing:
        return jsonify({'error': 'You have already reviewed this movie'}), 400

    review = Review(content=data['content'], rating=rating, movie_id=movie_id, user_id=current_user.id)
    db.session.add(review)
    db.session.commit()
    return jsonify({'message': 'Review added', 'review': review.to_dict()}), 201


@app.route('/api/reviews/<int:review_id>', methods=['DELETE'])
@token_required
def delete_review(current_user, review_id):  # User can delete own review
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
def get_my_reviews(current_user):  # Get current user's reviews
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
        'total_movies': Movie.query.count(),
        'total_reviews': Review.query.count()
    }), 200


if __name__ == '__main__':
    print("\nMovieHub - Part 2: Auth & Admin")
    print("http://127.0.0.1:5000")
    print("Admin: admin@moviehub.com / admin123\n")
    app.run(debug=True)
