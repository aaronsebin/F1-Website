
from django.db import models
from django.contrib.auth.models import User


# ============================= DRIVER =============================

class Driver(models.Model):

    driver_id = models.SlugField(
        max_length=100,
        unique=True,
        null=True,
        blank=True
    )

    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100, blank=True)

    team = models.CharField(max_length=100)
    nationality = models.CharField(max_length=100)

    number = models.PositiveSmallIntegerField(
        null=True,
        blank=True
    )

    short_name = models.CharField(max_length=10, blank=True)
    profile_url = models.URLField(blank=True)

    points = models.FloatField(default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} {self.surname}".strip()


# ============================= RACE NOTES =============================

class RaceNote(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="race_notes"
    )

    race_name = models.CharField(max_length=100)
    season = models.PositiveSmallIntegerField()
    circuit = models.CharField(max_length=150, blank=True)
    notes = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at"]

    def __str__(self):
        return f"{self.race_name} ({self.season})"


# ============================= USER PROFILE =============================

class UserProfile(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile"
    )

    profile_image = models.ImageField(
        upload_to="profile_images/",
        blank=True,
        null=True
    )

    def __str__(self):
        return f"{self.user.username}'s Profile"
