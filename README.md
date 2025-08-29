#GROUPE 8
#FEDE NDINGE Hoda, JEBALI Soumaya, BEJI Souhir, HMAMED Chaimae. 

# -GameForge-

**GameForge - Générateur de Concepts de Jeux Vidéo avec IA**

GameForge est une application web Django qui génère automatiquement des concepts complets de jeux vidéo grâce à l'intelligence artificielle. Les utilisateurs peuvent créer des projets de jeu détaillés avec scénarios, personnages, lieux et concept art via une interface web intuitive.


**Collaboration et organisation du travail**

Bien que nous ayons réparti les tâches entre les membres de l’équipe (backend : Souhir, Chaimae et Soumaya ; frontend : Hoda), nous avons travaillé de manière collaborative tout au long du projet. Certaines personnes ont rencontré des difficultés techniques, notamment des problèmes de connexion à GitHub sur leur ordinateur. Pour contourner cela, nous avons partagé notre code et nos fichiers sous forme de dossiers compressés (ZIP) et nous les avons testés au fur et à mesure ensemble. 

Ainsi, même si nous n’avons pas créé chacune une branche distincte sur Git, nous avons échangé régulièrement nos parties respectives, intégré et testé le code collectivement. Cela nous a permis de progresser de façon collaborative, de résoudre ensemble les problèmes rencontrés et d’assurer la cohérence du projet final. 

Nous avons également utilisé Trello pour organiser les tâches, suivre l’avancement du projet et assurer une meilleure coordination entre les membres. (sur Teams aussi) 

Lien pour le Trello : https://trello.com/invite/b/68b0239667a6d3495e8b5d62/ATTIa0e3b19eab4a6783129e4b2de49f4431AF42A20A/gameforgedjango-m1-touil 

<img width="1910" height="997" alt="image" src="https://github.com/user-attachments/assets/1b5fd45a-9f71-463d-bd4d-afd2db151756" />


<img width="1910" height="997" alt="image" src="https://github.com/user-attachments/assets/4ccc5867-8308-4b14-858d-26f4d315843e" />





**Fonctionnalités**

- Génération IA : Création automatique d’univers de jeu, scénarios, personnages et lieux grâce aux modèles Hugging Face.  
- Gestion des utilisateurs : Système complet d’authentification avec inscription et connexion.  
- Système de favoris : Sauvegarde et organisation des projets de jeu favoris.  
- Limites d’utilisation : Limites quotidiennes de génération pour gérer les coûts API.  
- Design responsive : Interface moderne et sombre, adaptée à tous les appareils.  
- Export PDF : Génération de documents PDF professionnels pour les concepts de jeu.  
- Recherche et filtrage : Trouver des projets par titre, genre ou créateur.  
- Contrôle de la confidentialité : Paramètres de visibilité publique/privée des projets.

**Architecture**

Backend :  
- Models (models.py) : Structures de données principales pour `GameProject`, `Favorite` et `DailyUsage`.  
- Views (games/views.py) : Logique métier pour les opérations CRUD et interactions utilisateurs.  
- AI Integration (games/utils/) : Intégration de l’API Hugging Face pour la génération de contenu.  
- Authentication (accounts/) : Gestion des utilisateurs et inscription.

Frontend :  
- Templates (templates/) : Templates Django avec CSS moderne.  
- Static Assets (static/) : CSS personnalisé avec thème sombre pour gamers.  
- Responsive Design : Approche mobile-first avec CSS Grid.




**problemes rencontrés**
- IA : dans notre application, nous n'avons pas réussit à faire en sorte que l'IA génère des images et du textes par exemple acte etc afin d'aider l'utilisateur.
- Trello : nous n'avons pas pu rajouté Chaimae car on a atteint le nombre de personnes maximales (gratuit autorisé)

 **Axe d'amélioration**
 - Design peut etre 

**Démarrage rapide**

Prérequis :  
- Python 3.8+  
- Django 4.2+  
- Clé API Hugging Face (optionnelle, modèles de secours disponibles)

**Installation et lancement :**  

```bash
# Cloner le dépôt
git clone https://github.com/yourusername/gameforge.git
cd gameforge

# Créer un environnement virtuel
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/Mac

# Installer les dépendances
pip install -r requirements.txt

# Configurer la base de données
python manage.py migrate

# Lancer le serveur de développement
python manage.py runserver

# Accéder à GameForge
# Ouvrir http://127.0.0.1:8000 dans votre navigateur



Structure du projet

GameForge/
├── gameforge/                 # Paramètres Django
│   ├── settings.py            # Configuration principale
│   ├── urls.py                # Routage des URLs
│   └── wsgi.py                # Configuration WSGI
├── games/                     # Application principale
│   ├── models.py              # Modèles de données
│   ├── views.py               # Logique métier
│   ├── forms.py               # Définitions de formulaires
│   ├── admin.py               # Interface admin
│   ├── urls.py                # URLs de l’app
│   └── utils/                 # Modules utilitaires
│       ├── generator.py       # Génération de contenu IA
│       └── huggingface.py     # Intégration API Hugging Face
├── accounts/                  # Authentification
│   ├── views.py               # Vues auth
│   └── urls.py                # URLs auth
├── templates/                 # Templates HTML
│   ├── base.html              # Template de base
│   ├── home.html              # Page d’accueil
│   ├── detail.html            # Détails d’un projet
│   ├── create.html            # Formulaire de création
│   └── registration/          # Templates d’authentification
├── static/                    # Assets statiques
│   └── css/
│       └── styles.css         # Styles principaux
├── media/                     # Uploads utilisateurs & images générées
├── requirements.txt           # Dépendances Python
└── .env                       # Variables d’environnement (NE PAS COMMIT)
