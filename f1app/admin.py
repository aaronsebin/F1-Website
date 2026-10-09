
from django.contrib import admin
from .models import RaceNote


@admin.register(RaceNote)
class RaceNoteAdmin(admin.ModelAdmin):
    list_display = (
        "race_name",
        "season",
        "circuit",
        "user",
        "updated_at",
    )

    search_fields = ("race_name", "circuit", "user__username")
    list_filter = ("season",)
