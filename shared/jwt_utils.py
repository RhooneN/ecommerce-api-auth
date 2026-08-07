import jwt
from datetime import datetime, timedelta
from django.conf import settings
from rest_framework_simplejwt.authentication import JWTAuthentication

def create_jwt_token(user_data):
    """Simple JWT token creation"""
    payload = {
        'user_id': user_data['id'],
        'username': user_data['username'],
        'is_admin': user_data.get('is_staff', False),
        'exp': datetime.utcnow() + timedelta(hours=24)
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

def verify_jwt_token(token):
    """Simple JWT token verification"""
    try:
        return JWTAuthentication().get_validated_token(token)
    except InvalidToken:
        return None
