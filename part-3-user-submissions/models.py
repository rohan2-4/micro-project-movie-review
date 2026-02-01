# models.py - Database Models with User Submissions

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    reviews = db.relationship('Review', backref='author', lazy=True)
    submitted_movies = db.relationship('Movie', backref='submitter', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'is_admin': self.is_admin
        }


class Movie(db.Model):
    __tablename__ = 'movies'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    poster_url = db.Column(db.String(500), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=True)
    is_verified = db.Column(db.Boolean, default=False)  # Only verified movies shown to users
    submitted_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)  # User who submitted
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    reviews = db.relationship('Review', backref='movie', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'category': self.category,
            'poster_url': self.poster_url,
            'year': self.year,
            'description': self.description,
            'is_verified': self.is_verified,
            'submitted_by': self.submitted_by,
            'submitter_name': self.submitter.username if self.submitter else 'Admin'
        }

    def to_dict_with_rating(self):
        reviews = Review.query.filter_by(movie_id=self.id).all()
        avg_rating = 0
        if reviews:
            avg_rating = round(sum(r.rating for r in reviews) / len(reviews), 1)
        return {
            'id': self.id,
            'title': self.title,
            'category': self.category,
            'poster_url': self.poster_url,
            'year': self.year,
            'description': self.description,
            'is_verified': self.is_verified,
            'submitted_by': self.submitted_by,
            'submitter_name': self.submitter.username if self.submitter else 'Admin',
            'avg_rating': avg_rating,
            'review_count': len(reviews)
        }


class Review(db.Model):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'content': self.content,
            'rating': self.rating,
            'movie_id': self.movie_id,
            'user_id': self.user_id,
            'username': self.author.username,
            'created_at': self.created_at.strftime('%Y-%m-%d')
        }


def init_db(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()
        seed_movies()


def seed_admin():
    """Create default admin user if not exists"""
    from auth import hash_password
    if not User.query.filter_by(email='admin@moviehub.com').first():
        admin = User(
            username='admin',
            email='admin@moviehub.com',
            password_hash=hash_password('admin123'),
            is_admin=True
        )
        db.session.add(admin)
        db.session.commit()


def seed_movies():
    seed_admin()  # Always try to create admin first
    if Movie.query.count() == 0:
        movies = [
            Movie(title="The Dark Knight", category="Action", poster_url="https://m.media-amazon.com/images/M/MV5BMTMxNTMwODM0NF5BMl5BanBnXkFtZTcwODAyMTk2Mw@@._V1_.jpg", year=2008, description="When the menace known as the Joker wreaks havoc on Gotham, Batman must accept one of the greatest psychological and physical tests.", is_verified=True),
            Movie(title="Inception", category="Sci-Fi", poster_url="https://m.media-amazon.com/images/M/MV5BMjAxMzY3NjcxNF5BMl5BanBnXkFtZTcwNTI5OTM0Mw@@._V1_.jpg", year=2010, description="A thief who steals corporate secrets through dream-sharing technology is given the task of planting an idea into a CEO's mind.", is_verified=True),
            Movie(title="The Hangover", category="Comedy", poster_url="https://m.media-amazon.com/images/M/MV5BNGQwZjg5YmYtY2VkNC00NzliLTljYTctNzI5NmU3MjE2ODQzXkEyXkFqcGdeQXVyNzkwMjQ5NzM@._V1_.jpg", year=2009, description="Three buddies wake up from a bachelor party in Las Vegas with no memory of the previous night.", is_verified=True),
            Movie(title="The Conjuring", category="Horror", poster_url="https://m.media-amazon.com/images/M/MV5BMTM3NjA1NDMyMV5BMl5BanBnXkFtZTcwMDQzNDMzOQ@@._V1_.jpg", year=2013, description="Paranormal investigators Ed and Lorraine Warren help a family terrorized by a dark presence.", is_verified=True),
            Movie(title="The Shawshank Redemption", category="Drama", poster_url="https://m.media-amazon.com/images/M/MV5BNDE3ODcxYzMtY2YzZC00NmNlLWJiNDMtZDViZWM2MzIxZDYwXkEyXkFqcGdeQXVyNjAwNDUxODI@._V1_.jpg", year=1994, description="Two imprisoned men bond over years, finding solace and redemption through acts of common decency.", is_verified=True),
            Movie(title="Avengers: Endgame", category="Action", poster_url="https://m.media-amazon.com/images/M/MV5BMTc5MDE2ODcwNV5BMl5BanBnXkFtZTgwMzI2NzQ2NzM@._V1_.jpg", year=2019, description="After Infinity War, the Avengers assemble once more to reverse Thanos's actions and restore the universe.", is_verified=True),
            Movie(title="Interstellar", category="Sci-Fi", poster_url="https://m.media-amazon.com/images/M/MV5BZjdkOTU3MDktN2IxOS00OGEyLWFmMjktY2FiMmZkNWIyODZiXkEyXkFqcGdeQXVyMTMxODk2OTU@._V1_.jpg", year=2014, description="A team of explorers travel through a wormhole in space to ensure humanity's survival.", is_verified=True),
            Movie(title="Superbad", category="Comedy", poster_url="https://m.media-amazon.com/images/M/MV5BY2VkMDg4ZTYtN2M3Yy00NWZhLWE0NTAtMDQxZjhlMTI5NTc4XkEyXkFqcGdeQXVyODY5Njk4Njc@._V1_.jpg", year=2007, description="Two high school seniors deal with separation anxiety after their plan to score alcohol goes awry.", is_verified=True)
        ]
        for movie in movies:
            db.session.add(movie)
        db.session.commit()
