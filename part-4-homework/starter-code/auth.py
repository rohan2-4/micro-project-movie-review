# auth.py - Authentication Helpers

import jwt
from datetime import datetime, timedelta
from functools import wraps
from flask import request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash

SECRET_KEY = "movie-hub-secret-key-change-in-production"
TOKEN_EXPIRATION_HOURS = 24


def hash_password(password):
    return generate_password_hash(password)


def verify_password(password_hash, password):
    return check_password_hash(password_hash, password)


def create_token(user_id, is_admin=False):
    payload = {
        'user_id': user_id,
        'is_admin': is_admin,
        'exp': datetime.utcnow() + timedelta(hours=TOKEN_EXPIRATION_HOURS),
        'iat': datetime.utcnow()
    }
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')


def decode_token(token):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def token_required(f):  # Decorator for protected routes
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            try:
                token = request.headers['Authorization'].split(" ")[1]
            except IndexError:
                return jsonify({'error': 'Invalid token format'}), 401

        if not token:
            return jsonify({'error': 'Token is missing'}), 401

        payload = decode_token(token)
        if not payload:
            return jsonify({'error': 'Token is invalid or expired'}), 401

        from models import User
        current_user = User.query.get(payload['user_id'])
        if not current_user:
            return jsonify({'error': 'User not found'}), 401

        return f(current_user, *args, **kwargs)
    return decorated


def admin_required(f):  # Decorator for admin-only routes
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            try:
                token = request.headers['Authorization'].split(" ")[1]
            except IndexError:
                return jsonify({'error': 'Invalid token format'}), 401

        if not token:
            return jsonify({'error': 'Token is missing'}), 401

        payload = decode_token(token)
        if not payload:
            return jsonify({'error': 'Token is invalid or expired'}), 401

        if not payload.get('is_admin', False):
            return jsonify({'error': 'Admin access required'}), 403

        from models import User
        current_user = User.query.get(payload['user_id'])
        if not current_user:
            return jsonify({'error': 'User not found'}), 401

        return f(current_user, *args, **kwargs)
    return decorated
