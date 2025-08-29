
import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gameforge.settings')
django.setup()

from games.utils.huggingface import generate_text

def test_ai_generation():
    print("=== TEST DE GÉNÉRATION IA ===")
    
    prompt = "Titre: Fantasy Quest\nGenre: RPG\nAmbiance: Epic Fantasy\nMots-clés: magic, adventure\nRéférences: Lord of the Rings"
    
    print(f"Prompt de test: {prompt}")
    print("-" * 50)
    
    result = generate_text(prompt)
    
    print("-" * 50)
    print("RÉSULTAT:")
    print(result)
    print("-" * 50)

if __name__ == "__main__":
    test_ai_generation()
