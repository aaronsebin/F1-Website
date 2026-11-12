from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
from datetime import date
from .models import RaceNote, UserProfile
from .forms import RaceNoteForm, UserProfileForm, UserUpdateForm
from .f1_api import get_f1_data, F1APIError

# ============================= HOME =============================

def home(request):
    from .f1_api import get_f1_data, F1APIError

    context = {
        "api_error": False,
        "season": date.today().year,
        "driver_count": 0,
        "team_count": 0,
        "race_count": 0,
        "next_race": None,
        "latest_race": None,
    }

    try:
        # Get current-season drivers
        driver_data = get_f1_data("current/drivers")
        drivers = driver_data.get("drivers", [])

        # Get current-season race calendar
        calendar_data = get_f1_data("current")
        races = calendar_data.get("races", calendar_data.get("race", []))

        # Calculate counts
        context["season"] = calendar_data.get("season", date.today().year)
        context["driver_count"] = driver_data.get("total", len(drivers))
        context["team_count"] = len({
            driver.get("teamId")
            for driver in drivers
            if driver.get("teamId")
        })
        context["race_count"] = calendar_data.get("total", len(races))

        # Find the next race
        upcoming_races = []

        for race in races:
            schedule = race.get("schedule", {})
            race_schedule = schedule.get("race", {})
            race_date = race_schedule.get("date") or race.get("date")

            if not race_date:
                continue

            try:
                parsed_date = date.fromisoformat(race_date[:10])
            except (ValueError, TypeError):
                continue

            if parsed_date >= date.today():
                race["display_date"] = parsed_date.strftime("%d %b %Y")
                upcoming_races.append((parsed_date, race))

        if upcoming_races:
            upcoming_races.sort(key=lambda item: item[0])
            context["next_race"] = upcoming_races[0][1]
            
        
        # Fetch current drivers' championship standings----------------------------------
        try:
            standings_data = get_f1_data(
                "current/drivers-championship"
            )

            standings = standings_data.get(
                "drivers_championship", []
            )

            # Keep the top four drivers
            standings = sorted(
                standings,
                key=lambda item: (
                    item.get("position") is None,
                    item.get("position") or 999
                )
            )[:4]

            max_points = max(
                (float(item.get("points") or 0)
                for item in standings),
                default=0
            )

            for item in standings:
                position = item.get("position")
                item["display_position"] = (
                    f"{position:02d}"
                    if position is not None
                    else "—"
                )

                points = float(item.get("points") or 0)
                item["bar_pct"] = (
                    points / max_points * 100
                    if max_points else 0
                )

            context["championship_standings"] = standings

        except F1APIError as error:
            print("Standings API error:", error)
            context["championship_standings"] = []


        # Fetch the latest race results-----------------------------------------
        try:
            latest_data = get_f1_data("current/last/race")
            latest_race = latest_data.get("races")

            if isinstance(latest_race, dict):
                results = latest_race.get("results", [])
                latest_race["results"] = (
                    results if isinstance(results, list) else []
                )
                context["latest_race"] = latest_race

        except F1APIError as error:
            print("Latest race API error:", error)

    except F1APIError as error:
        print("F1 API error:", error)
        context["api_error"] = True

    return render(request, "index.html", context)

# ============================= DRIVERS =============================

def drivers(request):
    try:
        data = get_f1_data("current/drivers")

        return render(
            request,
            "pages/drivers.html",
            {
                "drivers": data.get("drivers", []),
                "api_error": None,
            },
        )

    except F1APIError:
        return render(
            request,
            "pages/drivers.html",
            {
                "drivers": [],
                "api_error": (
                    "Formula 1 data is temporarily unavailable. "
                    "Please try again later."
                ),
            },
        )


# ============================= TEAMS =============================
def teams(request):
    teams = [
        {
            'name': 'McLaren',
            'slug': 'mclaren',
            'short_name': 'MCL',
            'car_image': 'f1app/images/teams/mclaren.webp',
        },
        {
            'name': 'Mercedes',
            'slug': 'mercedes',
            'short_name': 'MER',
            'car_image': 'f1app/images/teams/mercedes.webp',
        },
        {
            'name': 'Red Bull Racing',
            'slug': 'red-bull-racing',
            'short_name': 'RBR',
            'car_image': 'f1app/images/teams/redbull.webp',
        },
        {
            'name': 'Ferrari',
            'slug': 'ferrari',
            'short_name': 'FER',
            'car_image': 'f1app/images/teams/ferrari.webp',
        },
        {
            'name': 'Williams',
            'slug': 'williams',
            'short_name': 'WIL',
            'car_image': 'f1app/images/teams/williams.webp',
        },
        {
            'name': 'Racing Bulls',
            'slug': 'racing-bulls',
            'short_name': 'RB',
            'car_image': 'f1app/images/teams/racing-bulls.webp',
        },
        {
            'name': 'Aston Martin',
            'slug': 'aston-martin',
            'short_name': 'AMR',
            'car_image': 'f1app/images/teams/aston-martin.webp',
        },
        {
            'name': 'Haas',
            'slug': 'haas',
            'short_name': 'HAA',
            'car_image': 'f1app/images/teams/haas.webp',
        },
        {
            'name': 'Audi',
            'slug': 'audi',
            'short_name': 'AUD',
            'car_image': 'f1app/images/teams/audi.webp',
        },
        {
            'name': 'Alpine',
            'slug': 'alpine',
            'short_name': 'ALP',
            'car_image': 'f1app/images/teams/alpine.webp',
        },
        {
            'name': 'Cadillac',
            'slug': 'cadillac',
            'short_name': 'CAD',
            'car_image': 'f1app/images/teams/cadillac.webp',
        },
    ]

    return render(request, 'pages/teams.html', {'teams': teams})


def team_detail(request, slug):
    teams = {
        'mclaren': {
            'name': 'McLaren',
            'short_name': 'MCL',
            'car_image': 'f1app/images/teams/mclaren.webp',
        },
        'mercedes': {
            'name': 'Mercedes',
            'short_name': 'MER',
            'car_image': 'f1app/images/teams/mercedes.webp',
        },
        'red-bull-racing': {
            'name': 'Red Bull Racing',
            'short_name': 'RBR',
            'car_image': 'f1app/images/teams/redbull.webp',
        },
        'ferrari': {
            'name': 'Ferrari',
            'short_name': 'FER',
            'car_image': 'f1app/images/teams/ferrari.webp',
        },
        'williams': {
            'name': 'Williams',
            'short_name': 'WIL',
            'car_image': 'f1app/images/teams/williams.webp',
        },
        'racing-bulls': {
            'name': 'Racing Bulls',
            'short_name': 'RB',
            'car_image': 'f1app/images/teams/racing-bulls.webp',
        },
        'aston-martin': {
            'name': 'Aston Martin',
            'short_name': 'AMR',
            'car_image': 'f1app/images/teams/aston-martin.webp',
        },
        'haas': {
            'name': 'Haas',
            'short_name': 'HAA',
            'car_image': 'f1app/images/teams/haas.webp',
        },
        'audi': {
            'name': 'Audi',
            'short_name': 'AUD',
            'car_image': 'f1app/images/teams/audi.webp',
        },
        'alpine': {
            'name': 'Alpine',
            'short_name': 'ALP',
            'car_image': 'f1app/images/teams/alpine.webp',
        },
        'cadillac': {
            'name': 'Cadillac',
            'short_name': 'CAD',
            'car_image': 'f1app/images/teams/cadillac.webp',
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

        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')

        # Check required fields
        if not username or not email or not password or not confirm_password:
            messages.error(
                request,
                'Please fill in all the fields.'
            )
            return redirect('signup')

        # Check username length
        if len(username) < 3:
            messages.error(
                request,
                'Username must be at least 3 characters long.'
            )
            return redirect('signup')

        # Check password length
        if len(password) < 6:
            messages.error(
                request,
                'Password must be at least 6 characters long.'
            )
            return redirect('signup')

        # Check password confirmation
        if password != confirm_password:
            messages.error(
                request,
                'Passwords do not match.'
            )
            return redirect('signup')

        # Check whether username already exists
        if User.objects.filter(username=username).exists():
            messages.error(
                request,
                'Username already exists.'
            )
            return redirect('signup')

        # Check whether email already exists
        if User.objects.filter(email__iexact=email).exists():
            messages.error(
                request,
                'Email is already registered.'
            )
            return redirect('signup')

        # Create user
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



# ============================= RACE NOTES: READ =============================

@login_required
def race_notes(request):

    # Retrieve notes belonging to the logged-in user
    notes = RaceNote.objects.filter(user=request.user)

    # Divide records into pages of 5
    paginator = Paginator(notes, 5)

    # Get the requested page number from the URL
    page_number = request.GET.get('page')

    # Return the requested page
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        'pages/race_notes.html',
        {
            'page_obj': page_obj,
            'notes': page_obj,
        }
    )


# ============================= RACE NOTES: CREATE =============================

@login_required
def race_note_create(request):
    if request.method == 'POST':
        form = RaceNoteForm(request.POST)

        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note.save()

            messages.success(request, 'Race note created successfully.')
            return redirect('race_notes')
    else:
        form = RaceNoteForm()

    return render(
        request,
        'pages/race_note_form.html',
        {
            'form': form,
            'page_title': 'Add Race Note',
        }
    )


# ============================= RACE NOTES: UPDATE =============================

@login_required
def race_note_update(request, pk):
    note = get_object_or_404(
        RaceNote,
        pk=pk,
        user=request.user
    )

    if request.method == 'POST':
        form = RaceNoteForm(request.POST, instance=note)

        if form.is_valid():
            form.save()
            messages.success(request, 'Race note updated successfully.')
            return redirect('race_notes')
    else:
        form = RaceNoteForm(instance=note)

    return render(
        request,
        'pages/race_note_form.html',
        {
            'form': form,
            'page_title': 'Edit Race Note',
        }
    )


# ============================= RACE NOTES: DELETE =============================

@login_required
def race_note_delete(request, pk):
    note = get_object_or_404(
        RaceNote,
        pk=pk,
        user=request.user
    )

    if request.method == 'POST':
        note.delete()
        messages.success(request, 'Race note deleted successfully.')
        return redirect('race_notes')

    return render(
        request,
        'pages/race_note_confirm_delete.html',
        {'note': note}
    )



# ============================= USER PROFILE =============================

@login_required
def profile_view(request):

    profile, created = UserProfile.objects.get_or_create(
        user=request.user
    )

    if request.method == 'POST':

        action = request.POST.get('action')

        # UPDATE ACCOUNT DETAILS
        if action == 'update_details':

            user_form = UserUpdateForm(
                request.POST,
                instance=request.user
            )

            if user_form.is_valid():

                user_form.save()

                messages.success(
                    request,
                    'Account details updated successfully.'
                )

                return redirect('profile')

            image_form = UserProfileForm(instance=profile)

        # UPDATE PROFILE PICTURE
        else:

            image_form = UserProfileForm(
                request.POST,
                request.FILES,
                instance=profile
            )

            if image_form.is_valid():

                # Save the old image filename before updating
                old_image_name = (
                    profile.profile_image.name
                    if profile.profile_image else None
                )

                updated_profile = image_form.save()

                new_image_name = (
                    updated_profile.profile_image.name
                    if updated_profile.profile_image else None
                )

                # Delete the old image if a new one was uploaded
                if old_image_name and old_image_name != new_image_name:
                    profile.profile_image.storage.delete(old_image_name)

                messages.success(
                    request,
                    'Profile picture updated successfully.'
                )

                return redirect('profile')

            user_form = UserUpdateForm(instance=request.user)

    else:

        user_form = UserUpdateForm(instance=request.user)
        image_form = UserProfileForm(instance=profile)

    return render(
        request,
        'pages/profile.html',
        {
            'profile': profile,
            'form': image_form,
            'user_form': user_form
        }
    )



# ============================= REMOVE PROFILE IMAGE =============================

@login_required
@require_POST
def remove_profile_image(request):

    # Find the logged-in user's profile
    profile, created = UserProfile.objects.get_or_create(
        user=request.user
    )

    # Check whether a profile image exists
    if profile.profile_image:

        # Delete the physical image file
        profile.profile_image.delete(save=False)

        # Clear the database field
        profile.profile_image = None
        profile.save()

        messages.success(
            request,
            'Profile picture removed successfully.'
        )

    else:
        messages.info(
            request,
            'You do not have a profile picture to remove.'
        )

    return redirect('profile')
