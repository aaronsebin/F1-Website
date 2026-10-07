from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages


def home(request):
    return render(request, 'index.html')


def drivers(request):
    return render(request, 'pages/drivers.html')


def teams(request):
    return render(request, 'pages/teams.html')


def races(request):
    return render(request, 'pages/races.html')


def standings(request):
    return render(request, 'pages/standings.html')


def analytics(request):
    return render(request, 'pages/analytics.html')


def login_view(request):

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        # Check if username exists
        if not User.objects.filter(username=username).exists():

            messages.error(
                request,
                'Account does not exist. Please check your username.'
            )

            return redirect('login')

        # Check username and password
        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            return redirect('home')

        else:

            messages.error(
                request,
                'Incorrect password. Please try again.'
            )

            return redirect('login')

    return render(request, 'pages/login.html')

def logout_view(request):
    logout(request)
    return redirect('home')


def signup_view(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:

            messages.error(
                request,
                'Passwords do not match.'
            )

            return redirect('signup')

        if User.objects.filter(username=username).exists():

            messages.error(
                request,
                'Username already exists.'
            )

            return redirect('signup')

        if User.objects.filter(email=email).exists():

            messages.error(
                request,
                'Email is already registered.'
            )

            return redirect('signup')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        messages.success(
            request,
            'Account created successfully. You can now log in.'
        )

        return redirect('login')

    return render(request, 'pages/signup.html')