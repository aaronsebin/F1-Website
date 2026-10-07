from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages

# ============================= HOME =============================
def home(request):
    return render(request, 'index.html')

# ============================= DRIVERS =============================
def drivers(request):
    return render(request, 'pages/drivers.html')

# ============================= TEAMS =============================
def teams(request):
    teams = [
        {
            'name': 'McLaren',
            'slug': 'mclaren',
            'short_name': 'MCL',
            'car_image': 'f1app/images/teams/mclaren.png',
        },
        {
            'name': 'Mercedes',
            'slug': 'mercedes',
            'short_name': 'MER',
            'car_image': 'f1app/images/teams/mercedes.png',
        },
        {
            'name': 'Red Bull Racing',
            'slug': 'red-bull-racing',
            'short_name': 'RBR',
            'car_image': 'f1app/images/teams/redbull.png',
        },
        {
            'name': 'Ferrari',
            'slug': 'ferrari',
            'short_name': 'FER',
            'car_image': 'f1app/images/teams/ferrari.png',
        },
        {
            'name': 'Williams',
            'slug': 'williams',
            'short_name': 'WIL',
            'car_image': 'f1app/images/teams/williams.png',
        },
        {
            'name': 'Racing Bulls',
            'slug': 'racing-bulls',
            'short_name': 'RB',
            'car_image': 'f1app/images/teams/racing-bulls.png',
        },
        {
            'name': 'Aston Martin',
            'slug': 'aston-martin',
            'short_name': 'AMR',
            'car_image': 'f1app/images/teams/aston-martin.png',
        },
        {
            'name': 'Haas',
            'slug': 'haas',
            'short_name': 'HAA',
            'car_image': 'f1app/images/teams/haas.png',
        },
        {
            'name': 'Audi',
            'slug': 'audi',
            'short_name': 'AUD',
            'car_image': 'f1app/images/teams/audi.png',
        },
        {
            'name': 'Alpine',
            'slug': 'alpine',
            'short_name': 'ALP',
            'car_image': 'f1app/images/teams/alpine.png',
        },
        {
            'name': 'Cadillac',
            'slug': 'cadillac',
            'short_name': 'CAD',
            'car_image': 'f1app/images/teams/cadillac.png',
        },
    ]

    return render(request, 'pages/teams.html', {'teams': teams})


def team_detail(request, slug):
    teams = {
        'mclaren': {
            'name': 'McLaren',
            'short_name': 'MCL',
            'car_image': 'f1app/images/teams/mclaren.png',
        },
        'mercedes': {
            'name': 'Mercedes',
            'short_name': 'MER',
            'car_image': 'f1app/images/teams/mercedes.png',
        },
        'red-bull-racing': {
            'name': 'Red Bull Racing',
            'short_name': 'RBR',
            'car_image': 'f1app/images/teams/redbull.png',
        },
        'ferrari': {
            'name': 'Ferrari',
            'short_name': 'FER',
            'car_image': 'f1app/images/teams/ferrari.png',
        },
        'williams': {
            'name': 'Williams',
            'short_name': 'WIL',
            'car_image': 'f1app/images/teams/williams.png',
        },
        'racing-bulls': {
            'name': 'Racing Bulls',
            'short_name': 'RB',
            'car_image': 'f1app/images/teams/racing-bulls.png',
        },
        'aston-martin': {
            'name': 'Aston Martin',
            'short_name': 'AMR',
            'car_image': 'f1app/images/teams/aston-martin.png',
        },
        'haas': {
            'name': 'Haas',
            'short_name': 'HAA',
            'car_image': 'f1app/images/teams/haas.png',
        },
        'audi': {
            'name': 'Audi',
            'short_name': 'AUD',
            'car_image': 'f1app/images/teams/audi.png',
        },
        'alpine': {
            'name': 'Alpine',
            'short_name': 'ALP',
            'car_image': 'f1app/images/teams/alpine.png',
        },
        'cadillac': {
            'name': 'Cadillac',
            'short_name': 'CAD',
            'car_image': 'f1app/images/teams/cadillac.png',
        },
    }

    team = teams.get(slug)

    if team is None:
        return redirect('teams')

    return render(
        request,
        'pages/team_detail.html',
        {'team': team}
    )

# ============================= RACES =============================
def races(request):
    return render(request, 'pages/races.html')

# ============================= STANDINGS =============================
def standings(request):
    return render(request, 'pages/standings.html')

# ============================= ANALYTICS =============================
def analytics(request):
    return render(request, 'pages/analytics.html')

# ============================= LOGIN =============================
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

# ============================= LOGOUT =============================
def logout_view(request):
    logout(request)
    return redirect('home')

# ============================= SIGNUP =============================
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