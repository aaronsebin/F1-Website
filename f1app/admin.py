from django.contrib import admin
from .models import Driver, RaceNote, Race


@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "surname",
        "team",
        "number",
        "nationality",
        "is_active",
    )

    search_fields = (
        "name",
        "surname",
        "team",
        "nationality",
    )

    list_filter = (
        "team",
        "nationality",
        "is_active",
    )


@admin.register(RaceNote)
class RaceNoteAdmin(admin.ModelAdmin):

    list_display = (
        "race_name",
        "season",
        "circuit",
        "user",
        "updated_at",
    )

    search_fields = (
        "race_name",
        "circuit",
        "user__username",
    )

    list_filter = ("season",)
    
    
@admin.register(Race)
class RaceAdmin(admin.ModelAdmin):

    list_display = (
        "race_name",
        "season",
        "round",
        "circuit",
        "country",
        "race_date",
        "status",
    )

    search_fields = (
        "race_name",
        "circuit",
        "country",
    )

    list_filter = (
        "season",
        "status",
        "country",
    )

    ordering = ("season", "round")
