from django.contrib import admin
from django.urls import path

from f1app.views import (
    home,
    drivers,
    teams,
    races,
    standings,
    analytics,
    login_view,
    signup_view,
    logout_view,
)


urlpatterns = [
    path('admin/', admin.site.urls),

    path('', home, name='home'),
    path('drivers/', drivers, name='drivers'),
    path('teams/', teams, name='teams'),
    path('races/', races, name='races'),
    path('standings/', standings, name='standings'),
    path('analytics/', analytics, name='analytics'),

    path('login/', login_view, name='login'),
    path('signup/', signup_view, name='signup'),
    path('logout/', logout_view, name='logout'),
]