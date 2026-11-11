
from django import forms
from django.contrib.auth.models import User
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


# ============================= USER PROFILE IMAGE FORM =============================

class UserProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ["profile_image"]

        widgets = {
            "profile_image": forms.FileInput(attrs={
                "accept": ".jpg,.jpeg,.png,.webp",
                "class": "profile-file-input"
            })
        }

    def clean_profile_image(self):

        image = self.cleaned_data.get("profile_image")

        if not image:
            return image

        # Maximum file size: 5 MB
        max_size = 5 * 1024 * 1024

        if image.size > max_size:
            raise forms.ValidationError(
                "Image size must not exceed 5 MB."
            )

        # Check file extension
        allowed_extensions = ["jpg", "jpeg", "png", "webp"]

        extension = (
            image.name.rsplit(".", 1)[-1].lower()
            if "." in image.name else ""
        )

        if extension not in allowed_extensions:
            raise forms.ValidationError(
                "Only JPG, JPEG, PNG and WebP images are allowed."
            )

        # Validate the actual image format
        try:
            from PIL import Image

            img = Image.open(image)
            image_format = img.format
            img.verify()

            if image_format not in ["JPEG", "PNG", "WEBP"]:
                raise forms.ValidationError(
                    "The uploaded file must be a JPG, PNG or WebP image."
                )

            image.seek(0)

        except forms.ValidationError:
            raise

        except Exception:
            raise forms.ValidationError(
                "Please upload a valid image file."
            )

        return image


# ============================= USER ACCOUNT UPDATE FORM =============================

class UserUpdateForm(forms.ModelForm):

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            "placeholder": "Enter your email address"
        })
    )

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]

        widgets = {
            "first_name": forms.TextInput(attrs={
                "placeholder": "Enter your first name"
            }),
            "last_name": forms.TextInput(attrs={
                "placeholder": "Enter your last name"
            }),
        }

    def clean_email(self):

        email = self.cleaned_data.get("email")

        # Check whether another user already uses this email
        existing_user = User.objects.filter(
            email__iexact=email
        ).exclude(pk=self.instance.pk)

        if existing_user.exists():
            raise forms.ValidationError(
                "This email address is already registered."
            )

        return email
