from rest_framework.permissions import IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly, DjangoModelPermissionsOrAnonReadOnly, AllowAny
from rest_framework import routers, serializers, viewsets, status, generics, permissions
from . serializers import UserSerializer, ProfileSerializer, AccountSerializer, LoginSerializer
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from rest_framework.response import Response
from .models import Profile
from shared.jwt_utils import create_jwt_token
from django.contrib.auth.views import LoginView, LogoutView
from .serializers import MyTokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, login
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.exceptions import PermissionDenied
class CustomerLoginView(LoginView):
    
        template_name = 'app/login2.html'
        

from django.http import JsonResponse

def health(request):
    return JsonResponse({"status": "ok"})

class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

class ProfileList(generics.ListCreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAdminUser]

class ProfileRetrieveView(generics.RetrieveAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return Profile.objects.get_or_create(user=self.request.user)[0]

class ProfileUpdateView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer

    def get_object(self):
        return Profile.objects.get(user=self.request.user)


        
class UserDetailView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser, IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        return User.objects.get(pk=pk)


class DeleteUserView(generics.DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    def delete(self, request, *args, **kwargs):
            user = self.request.user
            try:
                user.delete()
                return Response({'message': 'User deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
 


class UserCreateView(generics.CreateAPIView):
    serializer_class = AccountSerializer
    permission_classes = [AllowAny]
    
# PROFILES
class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    def get_permissions(self):
        if self.action == "list":
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        if self.action == "list":
            return Profile.objects.all()
        return Profile.objects.filter(user=self.request.user)

    @action(detail=False, methods=["get", "put"], url_path="me")
    def me(self, request):
        profile, _ = Profile.objects.get_or_create(user=request.user)
        if request.method == "GET":
            return Response(ProfileSerializer(profile).data)
        serializer = ProfileSerializer(profile, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


# AUTH
class LoginView(generics.GenericAPIView):
    """Vue de connexion"""
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = authenticate(
            username=serializer.validated_data['username'],
            password=serializer.validated_data['password']
        )
        
        if user:
           login(request, user)
           refresh = RefreshToken.for_user(user)
           refresh["username"] = user.username
           refresh["email"] = user.email
           refresh["is_admin"] = user.is_staff
           refresh["is_system"] = getattr(getattr(user, "system_profile", None), "is_sys", False)
           

           return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "user_id": user.id,
                "username": user.username,
                "email": user.email, #this key is only for notification service, make this response utmost bigger but temporary hack
                "is_admin": user.is_staff,
                "message": "Login successful",
                "is_system": getattr(getattr(user, "system_profile", None), "is_sys", False)
    })
        return Response(
            {'error': 'Invalid credentials'},
            status=status.HTTP_401_UNAUTHORIZED
        )

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
   
    def get_permissions(self):
        print("user", self.request.user)
        print("auth", self.request.auth)
        print("headers", self.request.headers)
        if self.action in ["list", "destroy", "retrieve", "update", "partial_update", "create"]:
            return [permissions.IsAdminUser()]  # admin only
        return [permissions.IsAuthenticated()]

    @action(detail=False, methods=["get", "put", "patch", "delete"], url_path="me",
            permission_classes=[permissions.IsAuthenticated])
    def me(self, request):
        user = request.user
        if request.method == "GET":
            serializer = UserSerializer(user, context={"request": request})
            return Response(serializer.data)
        elif request.method in ["PUT", "PATCH"]:
            serializer = UserSerializer(user, data=request.data, partial=True, context={"request": request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
            
