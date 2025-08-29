"""
Test du nouveau système Hugging Face local car en ligne no luck ca marche pas
"""
import os
import sys

sys.path.append('C:/Users/soumayaj/Downloads/Django/projet/-GameForge-/GameForge-Django/GameForge-Django')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gameforge.settings')

import django
django.setup()

from games.utils.huggingface import generate_text, generate_game_universe, generate_image_placeholder

def test_local_generation():
    print("🧪 Test du générateur Hugging Face local")
    print("=" * 50)
    
    # Test 1: Génération de texte
    print("\n1. Test génération de texte...")
    prompt = "Créez une histoire fantasy avec des dragons"
    result = generate_text(prompt)
    print(f" Résultat ({len(result)} chars): {result[:200]}...")
    
    # Test 2: Génération d'univers
    print("\n2. Test génération d'univers...")
    universe = generate_game_universe("fantasy")
    print(f" Univers généré:")
    for key, value in universe.items():
        if isinstance(value, list):
            print(f"  {key}: {len(value)} éléments")
            for item in value[:2]:
                print(f"    - {item}")
        else:
            print(f"  {key}: {value[:100]}...")
    
    # Test 3: Image placeholder
    print("\n3. Test génération image...")
    image_data = generate_image_placeholder("dragon fantasy castle", 512, 512)
    if image_data:
        print(f"✅ Image générée: {len(image_data)} chars (base64)")
    else:
        print("❌ Erreur génération image")
    
    print("\n🎉 Tests terminés !")

if __name__ == "__main__":
    test_local_generation()
