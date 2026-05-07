from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import (
    authenticate,
    login as auth_login,
    logout as auth_logout,
)
from django.contrib.auth.models import User
from django.contrib import messages
from django.db import IntegrityError

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from .models import UserProfile
from .serializers import (
    UserSerializer,
    UserRegistrationSerializer,
    UserProfileUpdateSerializer,
    ChangePasswordSerializer,
)


# ──────────────────────────────────────────────
# Template / Web Views
# ──────────────────────────────────────────────

def login_view(request):
    """User login page"""
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        username = request.POST.get('username') or request.POST.get('email')
        password = request.POST.get('password')

        # Allow login by email
        if username and '@' in username:
            try:
                user_obj = User.objects.get(email=username)
                username = user_obj.username
            except User.DoesNotExist:
                pass

        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            next_url = request.GET.get('next', 'dashboard')
            messages.success(request, f'Welcome back, {user.first_name or user.username}!')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username/email or password.')

    return render(request, 'account/login.html', {'page_title': 'Login'})


def signup_view(request):
    """User registration / signup page"""
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        phone = request.POST.get('phone_number', '')
        org = request.POST.get('organization', '')

        if password != password2:
            messages.error(request, 'Passwords do not match.')
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken.')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')
        else:
            try:
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password,
                    first_name=first_name,
                    last_name=last_name,
                )
                UserProfile.objects.create(
                    user=user,
                    phone_number=phone,
                    organization=org,
                )
                auth_login(request, user)
                messages.success(request, f'Account created! Welcome, {user.first_name or user.username}!')
                return redirect('dashboard')
            except IntegrityError:
                messages.error(request, 'An error occurred. Please try again.')

    return render(request, 'account/signup.html', {'page_title': 'Sign Up'})


@login_required
def logout_view(request):
    """Logout and redirect to home"""
    auth_logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('home')


@login_required
def profile_view(request):
    """User profile view and update"""
    profile, _ = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        request.user.first_name = request.POST.get('first_name', request.user.first_name)
        request.user.last_name = request.POST.get('last_name', request.user.last_name)
        request.user.email = request.POST.get('email', request.user.email)
        request.user.save()

        profile.phone_number = request.POST.get('phone_number', profile.phone_number)
        profile.organization = request.POST.get('organization', profile.organization)
        profile.timezone = request.POST.get('timezone', profile.timezone)
        profile.language = request.POST.get('language', profile.language)
        profile.save()

        messages.success(request, 'Profile updated successfully!')
        return redirect('profile')

    return render(request, 'account/profile.html', {
        'page_title': 'My Profile',
        'profile': profile,
    })


@login_required
def user_data_view(request):
    """View user data summary"""
    from home.models import Farm, Cattle
    farms = Farm.objects.filter(user=request.user)
    cattle_count = Cattle.objects.filter(farm__in=farms).count()
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    return render(request, 'account/user-data.html', {
        'page_title': 'User Data',
        'farms': farms,
        'cattle_count': cattle_count,
        'profile': profile,
    })


# ──────────────────────────────────────────────
# API Views
# ──────────────────────────────────────────────

@api_view(['POST'])
@permission_classes([AllowAny])
def api_register(request):
    """API: Register a new user and return auth token"""
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user': UserSerializer(user).data,
            'message': 'Registration successful.',
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def api_login(request):
    """API: Login and return auth token"""
    username = request.data.get('username') or request.data.get('email')
    password = request.data.get('password')

    if not username or not password:
        return Response(
            {'error': 'Username/email and password are required.'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Allow email login
    if '@' in username:
        try:
            user_obj = User.objects.get(email=username)
            username = user_obj.username
        except User.DoesNotExist:
            pass

    user = authenticate(request, username=username, password=password)
    if user:
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user': UserSerializer(user).data,
        })
    return Response({'error': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_logout(request):
    """API: Logout — delete auth token"""
    try:
        request.user.auth_token.delete()
    except Exception:
        pass
    return Response({'message': 'Logged out successfully.'})


@api_view(['GET', 'PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def api_profile(request):
    """API: Get or update the authenticated user's profile"""
    profile, _ = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'GET':
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    serializer = UserProfileUpdateSerializer(profile, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(UserSerializer(request.user).data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_change_password(request):
    """API: Change password"""
    serializer = ChangePasswordSerializer(data=request.data)
    if serializer.is_valid():
        user = request.user
        if not user.check_password(serializer.validated_data['old_password']):
            return Response(
                {'old_password': 'Current password is incorrect.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        # Re-create token after password change
        Token.objects.filter(user=user).delete()
        token = Token.objects.create(user=user)
        return Response({'message': 'Password changed successfully.', 'token': token.key})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
