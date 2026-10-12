from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, login_not_required
from .forms import RegistrationForm, AccountAuthenticationForm
from django.contrib import messages
from django.http import HttpResponseForbidden
from .models import Account

@login_not_required
def signup_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegistrationForm()
    return render(request, 'auth/signup.html', {'form': form})

@login_not_required
def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)
            if user:
                login(request, user)
                return redirect('home')
    else:
        form = AccountAuthenticationForm()
    return render(request, 'auth/login.html', {'form': form})

@login_required
def profile_view(request):
    return render(request, 'auth/profile.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('home')


@login_required
def manage_users(request):
    # only allow admins (or staff) to access
    if not getattr(request.user, 'is_admin', False):
        return HttpResponseForbidden('Forbidden')

    if request.method == 'POST':
        action = request.POST.get('action')
        target_username = request.POST.get('username')
        try:
            target = Account.objects.get(username=target_username)
        except Account.DoesNotExist:
            messages.error(request, 'User not found')
            return redirect('manage_users')

        if action == 'promote':
            new_role = request.POST.get('role')
            valid_roles = [r[0] for r in Account.ROLE_CHOICES]
            if new_role in valid_roles:
                target.role = new_role
                target.save()
                messages.success(request, f"Updated role for {target.username} to {new_role}.")
            else:
                messages.error(request, 'Invalid role')

        elif action == 'delete':
            if target.username == request.user.username:
                messages.error(request, 'You cannot delete your own account here')
            else:
                target.delete()
                messages.success(request, f"Deleted user {target_username}.")

        return redirect('manage_users')

    users = Account.objects.all().order_by('-date_joined')
    return render(request, 'auth/manage_users.html', {'users': users, 'roles': Account.ROLE_CHOICES})