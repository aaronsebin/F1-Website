
from django.db import models
from django.contrib.auth.models import User


# ============================= DRIVER =============================

class Driver(models.Model):
    name = models.CharField(max_length=100)
    team = models.CharField(max_length=100)
    nationality = models.CharField(max_length=100)
    points = models.FloatField(default=0)

    def __str__(self):
        return self.name


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
