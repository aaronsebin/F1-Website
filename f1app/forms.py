
from django import forms
from .models import RaceNote, UserProfile


# ============================= RACE NOTE FORM =============================

class RaceNoteForm(forms.ModelForm):

    class Meta:
        model = RaceNote
        fields = [
            "race_name",
            "season",
            "circuit",
            "notes",
        ]

        widgets = {
            "race_name": forms.TextInput(attrs={
                "placeholder": "Enter race name"
            }),
            "season": forms.NumberInput(attrs={
                "placeholder": "e.g. 2026"
            }),
            "circuit": forms.TextInput(attrs={
                "placeholder": "Enter circuit name"
            }),
            "notes": forms.Textarea(attrs={
                "placeholder": "Write your race notes",
                "rows": 5,
            }),
        }


# ============================= USER PROFILE FORM =============================

class UserProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ["profile_image"]

    def clean_profile_image(self):

        image = self.cleaned_data.get("profile_image")

        # Allow an empty image when updating or removing a picture
        if not image:
            return image

        # Check file size (maximum 5 MB)
        max_size = 5 * 1024 * 1024

        if image.size > max_size:
            raise forms.ValidationError(
                "Image size must not exceed 5 MB."
            )

        # Check image extension
        allowed_extensions = ["jpg", "jpeg", "png", "webp"]

        extension = image.name.rsplit(".", 1)[-1].lower() if "." in image.name else ""

        if extension not in allowed_extensions:
            raise forms.ValidationError(
                "Only JPG, JPEG, PNG and WebP images are allowed."
            )

        # Check that the uploaded file is a valid image
        try:
            from PIL import Image

            img = Image.open(image)
            img.verify()

        except Exception:
            raise forms.ValidationError(
                "Please upload a valid image file."
            )

        return image
