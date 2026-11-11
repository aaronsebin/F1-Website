from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from f1app.views import (
    home,
    drivers,
    teams,
    team_detail,
    races,
    standings,
    analytics,
    login_view,
    signup_view,
    logout_view,
    race_notes,
    race_note_create,
    race_note_update,
    race_note_delete,
    profile_view,
    remove_profile_image,
)


urlpatterns = [
    path('admin/', admin.site.urls),

    path('', home, name='home'),
    path('drivers/', drivers, name='drivers'),
    path('teams/', teams, name='teams'),
    path('teams/<slug:slug>/', team_detail, name='team_detail'),
    path('races/', races, name='races'),
    path('standings/', standings, name='standings'),
    path('analytics/', analytics, name='analytics'),

    path('login/', login_view, name='login'),
    path('signup/', signup_view, name='signup'),
    path('logout/', logout_view, name='logout'),
    
    # Race Notes CRUD
    path('race-notes/', race_notes, name='race_notes'),
    path('race-notes/create/', race_note_create, name='race_note_create'),
    path('race-notes/<int:pk>/edit/', race_note_update, name='race_note_update'),
    path('race-notes/<int:pk>/delete/', race_note_delete, name='race_note_delete'),
    
    # User Profile
    path('profile/', profile_view, name='profile'),
    path(
        'profile/remove-image/',
        remove_profile_image,
        name='remove_profile_image'
),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )