import jwt
from datetime import datetime, timedelta
from django.conf import settings
from django.contrib.auth import get_user_model
from typing import Dict, List, Optional
import logging

User = get_user_model()
logger = logging.getLogger(__name__)

class AuthenticationService:
    """Centralized authentication service for microservices"""
    
    @staticmethod
    def get_user_permissions(user) -> List[str]:
        """Get user permissions based on roles and groups"""
        permissions = []
        
        # Basic permissions for all authenticated users
        permissions.extend([
            'cart.view', 'cart.create', 'cart.update', 'cart.delete',
            'order.view', 'order.create'
        ])
        
        # Staff permissions
        if user.is_staff:
            permissions.extend([
                'products.create', 'products.update', 'products.delete',
                'users.view', 'orders.manage'
            ])
        
        # Superuser permissions
        if user.is_superuser:
            permissions.extend([
                'admin.full_access', 'system.manage'
            ])
        
        # Group-based permissions
        for group in user.groups.all():
            if group.name == 'product_managers':
                permissions.extend(['products.create', 'products.update'])
            elif group.name == 'customer_service':
                permissions.extend(['orders.view', 'orders.update', 'users.view'])
        
        return list(set(permissions))  # Remove duplicates
    
    @staticmethod
    def create_jwt_token(user) -> str:
        """Create JWT token with user info and permissions"""
        permissions = AuthenticationService.get_user_permissions(user)
        
        payload = {
            'user_id': user.id,
            'username': user.username,
            'email': user.email,
            'is_staff': user.is_staff,
            'is_superuser': user.is_superuser,
            'permissions': permissions,
            'iat': datetime.utcnow(),
            'exp': datetime.utcnow() + timedelta(hours=24),
            'iss': 'user-service',  # Token issuer
            'aud': ['product-service', 'cart-service', 'order-service']  # Valid audiences
        }
        
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
        return token
    
    @staticmethod
    def create_refresh_token(user) -> str:
        """Create refresh token for token renewal"""
        payload = {
            'user_id': user.id,
            'token_type': 'refresh',
            'iat': datetime.utcnow(),
            'exp': datetime.utcnow() + timedelta(days=7),
            'iss': 'user-service'
        }
        
        return jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    
    @staticmethod
    def validate_token(token: str) -> Optional[Dict]:
        """Validate JWT token and return payload"""
        try:
            payload = jwt.decode(
                token, 
                settings.SECRET_KEY, 
                algorithms=['HS256'],
                options={'verify_exp': True}
            )
            return payload
        except jwt.ExpiredSignatureError:
            logger.warning("Token has expired")
            return None
        except jwt.InvalidTokenError as e:
            logger.warning(f"Invalid token: {e}")
            return None
    
    @staticmethod
    def refresh_access_token(refresh_token: str) -> Optional[str]:
        """Generate new access token from refresh token"""
        payload = AuthenticationService.validate_token(refresh_token)
        
        if not payload or payload.get('token_type') != 'refresh':
            return None
        
        try:
            user = User.objects.get(id=payload['user_id'])
            return AuthenticationService.create_jwt_token(user)
        except User.DoesNotExist:
            return None
