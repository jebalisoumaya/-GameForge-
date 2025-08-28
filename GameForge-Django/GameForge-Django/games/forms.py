from django import forms
from .models import GameProject

class GamePromptForm(forms.ModelForm):
    title = forms.CharField(max_length=120, help_text="Nom de votre jeu")
    class Meta:
        model = GameProject
        fields = ["title", "genre", "ambiance", "keywords", "references"]
        widgets = {
            "ambiance": forms.TextInput(attrs={"placeholder": "Post-apo, onirique, cyberpunk..."}),
            "keywords": forms.TextInput(attrs={"placeholder": "boucle temporelle, IA rebelle..."}),
            "references": forms.TextInput(attrs={"placeholder": "Zelda, Hollow Knight... (facultatif)"}),
        }
