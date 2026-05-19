# user_service/authentication/views.py
from django.contrib.auth import authenticate
from django.http import JsonResponse
from shared.jwt_utils import create_jwt_token

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(username=username, password=password)
        if user:
            token = create_jwt_token({
                'id': user.id,
                'username': user.username,
                'is_staff': user.is_staff
            })
            
            return JsonResponse({
                'token': token,
                'user_id': user.id,
                'is_admin': user.is_staff
            })
        
        return JsonResponse({'error': 'Invalid credentials'}, status=401)
