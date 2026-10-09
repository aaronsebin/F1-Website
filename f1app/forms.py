
from django import forms
from .models import RaceNote


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
