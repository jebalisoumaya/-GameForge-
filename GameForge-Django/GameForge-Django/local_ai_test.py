# Alternative : Utiliser Hugging Face Transformers localement
# Installez : pip install transformers torch

from transformers import pipeline, set_seed
import torch

def generate_with_local_model(prompt):
    """Utilise un modèle local au lieu de l'API"""
    try:
        # Utiliser un petit modèle qui fonctionne localement
        generator = pipeline('text-generation', 
                           model='gpt2',
                           device=0 if torch.cuda.is_available() else -1)
        
        set_seed(42)
        result = generator(f"Create a fantasy game: {prompt}", 
                         max_length=200, 
                         num_return_sequences=1,
                         temperature=0.7)
        
        return result[0]['generated_text']
    except Exception as e:
        print(f"Erreur modèle local: {e}")
        return None

# Test
if __name__ == "__main__":
    result = generate_with_local_model("epic adventure")
    print("Résultat:", result)
