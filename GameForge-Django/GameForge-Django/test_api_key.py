#!/usr/bin/env python
import requests
import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

def test_api_key():
    api_key = os.getenv("HUGGINGFACE_API_KEY", "").strip()
    print(f"Clé API: {api_key}")
    print(f"Longueur: {len(api_key)} caractères")
    
    # Test de l'API pour essayer de debug le problem
    headers = {"Authorization": f"Bearer {api_key}"}
    
    # Essayer une requête simple sur des modèle accessible pour que ca marche
    test_models = [
        "openai-community/gpt2",
        "microsoft/DialoGPT-small", 
        "google/flan-t5-small",
        "distilbert-base-uncased"
    ]
    
    for model in test_models:
        print(f"\n--- Test du modèle: {model} ---")
        url = f"https://api-inference.huggingface.co/models/{model}"
        
        
        response = requests.post(
            url, 
            headers=headers, 
            json={"inputs": "Hello world"}, 
            timeout=30
        )
        
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text[:200]}...")
        
        if response.status_code == 200:
            print(" SUCCESS - Ce modèle fonctionne!")
            return model
        elif response.status_code == 403:
            print(" ERREUR 403 - Clé API invalide ou pas d'accès")
        elif response.status_code == 404:
            print(" ERREUR 404 - Modèle introuvable")
        elif response.status_code == 503:
            print("⏳ ERREUR 503 - Modèle en cours de chargement")
        else:
            print(f" ERREUR {response.status_code}")
    
    return None

if __name__ == "__main__":
    working_model = test_api_key()
    if working_model:
        print(f"\n MODÈLE FONCTIONNEL TROUVÉ: {working_model}")
    else:
        print("\n AUCUN MODÈLE FONCTIONNEL TROUVÉ")
