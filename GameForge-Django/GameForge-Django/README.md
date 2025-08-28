# GameForge – Générateur de jeux vidéo par IA

## Présentation
Plateforme web en Django permettant de générer des concepts de jeux vidéo à l’aide de modèles d’IA (Hugging Face).
L’application génère : univers, scénario en 3 actes, personnages, lieux, images conceptuelles et fiche de présentation.

## Installation rapide
```bash
git clone <votre_repo_ici>.git
cd GameForge-Django
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env  # configurez la clé HF si vous en avez une
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Variables d'environnement
- `HUGGINGFACE_API_KEY` : jeton HF Inference API (optionnel). Sans cette variable, le projet utilise des sorties factices déterministes et génère des images de remplacement avec Pillow.
- `DEBUG` : `True` par défaut.

## Modèles utilisés (indicatifs)
- Texte: modèle instruct hébergé sur Hugging Face Inference API (ex: `mistralai/Mixtral-8x7B-Instruct` ou similaire). Le code appelle l'endpoint générique de l'API Inference.
- Image: `stabilityai/stable-diffusion-2-1` via Inference API. En absence de clé, une image placeholder est générée.

## Fonctionnalités
- Authentification (inscription/connexion/déconnexion)
- Formulaire guidé de création
- Génération univers/scénario (3 actes + twist)/personnages/lieux
- Génération images conceptuelles (personnage + environnement)
- Mode exploration libre (sans formulaire)
- Page d’accueil (jeux publics de tous les utilisateurs + recherche)
- Tableau de bord (jeux de l’utilisateur)
- Page de détail d’un jeu
- Favoris (ajout/suppression + page dédiée)
- Public/Privé par jeu
- Limitation d’usage par utilisateur/jour

## Bonus inclus
- Export PDF de la fiche jeu (ReportLab)
- Barre de recherche (titre/genre)
- Pop-ups de chargement simples (CSS)

## Ce qui n’a pas été implémenté
- Narration dynamique interactive
- GDD très détaillé
- Files d’attente asynchrones

## Commandes utiles
- `python manage.py makemigrations`
- `python manage.py migrate`
- `python manage.py runserver`

## Captures d’écran
Ajoutez vos propres captures après lancement (pages: accueil, détail, création, dashboard, favoris).
