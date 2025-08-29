import logging
import json
from datetime import datetime
import os
from dotenv import load_dotenv
import re

# Hugging Face local
from transformers import pipeline, GPT2LMHeadModel, GPT2Tokenizer
import torch

# Chargement des variables d'environnement
load_dotenv()

# Configuration du logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Configuration globale
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'

class HuggingFaceLocalGenerator:
    def __init__(self):
        self.text_generator = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        logger.info(f"Utilisation du device: {self.device}")
        
    def _initialize_text_generator(self):
        """Initialise le générateur de texte local"""
        if self.text_generator is None:
            try:
                logger.info("Initialisation du générateur de texte local...")
                # Utiliser un modèle plus petit et plus rapide pour commencer
                self.text_generator = pipeline(
                    "text-generation",
                    model="distilgpt2",  # Modèle plus petit et rapide
                    device=0 if self.device == "cuda" else -1,
                    torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
                    max_length=512
                )
                logger.info("Générateur de texte initialisé avec succès")
            except Exception as e:
                logger.error(f"Erreur lors de l'initialisation du générateur: {e}")
                self.text_generator = None
                
    def generate_text(self, prompt, max_new_tokens=300, temperature=0.8):
        """Génère du texte avec Hugging Face local"""
        try:
            self._initialize_text_generator()
            
            if self.text_generator is None:
                logger.error("Générateur non initialisé")
                return self._get_fallback_content(prompt)
                
            logger.info(f"Génération pour le prompt: {prompt[:50]}...")
            
            # Génération avec le modèle local
            result = self.text_generator(
                prompt,
                max_new_tokens=max_new_tokens,
                temperature=temperature,
                do_sample=True,
                pad_token_id=self.text_generator.tokenizer.eos_token_id,
                num_return_sequences=1,
                truncation=True
            )
            
            generated_text = result[0]['generated_text']
            
            # Nettoyer le texte généré (enlever le prompt original)
            if generated_text.startswith(prompt):
                generated_text = generated_text[len(prompt):].strip()
            
            logger.info(f"Texte généré avec succès: {len(generated_text)} caractères")
            return generated_text
            
        except Exception as e:
            logger.error(f"Erreur lors de la génération: {e}")
            return self._get_fallback_content(prompt)
            
    def _get_fallback_content(self, prompt):
        """Contenu de fallback de haute qualité"""
        
        # Détection du type de contenu demandé
        prompt_lower = prompt.lower()
        
        if "fantasy" in prompt_lower or "magic" in prompt_lower:
            return self._generate_fantasy_content()
        elif "sci-fi" in prompt_lower or "space" in prompt_lower or "futur" in prompt_lower:
            return self._generate_scifi_content()
        elif "horror" in prompt_lower or "terreur" in prompt_lower:
            return self._generate_horror_content()
        elif "adventure" in prompt_lower or "aventure" in prompt_lower:
            return self._generate_adventure_content()
        else:
            return self._generate_generic_game_content()
            
    def _generate_fantasy_content(self):
        return {
            "universe": "Dans le royaume mystique d'Aethermoor, la magie coule comme des rivières de lumière à travers des forêts enchantées. Les cristaux de mana flottent dans l'air, alimentant d'anciennes tours de sorciers qui percent les nuages.",
            "act1": "Les héros découvrent que les cristaux de mana s'éteignent mystérieusement, plongeant le royaume dans l'obscurité. Ils doivent partir en quête du Cœur de Lumière, un artefact légendaire caché dans les Montagnes Interdites.",
            "act2": "Le voyage les mène à travers le Marais des Âmes Perdues où ils affrontent des créatures corrompues par la magie noire. Ils découvrent que l'Archimage Noir a volé l'essence du Cœur de Lumière pour alimenter son propre pouvoir.",
            "act3": "Dans une bataille épique au sommet de la Tour Stellaire, les héros doivent utiliser leurs pouvoirs combinés pour vaincre l'Archimage et restaurer l'équilibre magique du royaume avant que l'obscurité ne l'engloutisse pour l'éternité.",
            "characters": [
                "Lyralei l'Elfe Archère - Maîtresse des vents et gardienne des secrets de la forêt",
                "Thormund le Nain Forgeron - Créateur d'armes magiques et gardien des anciennes traditions",
                "Seraphina la Prêtresse - Guérisseuse divine capable de purifier la magie corrompue",
                "Kael le Mage de Bataille - Jeune prodige capable de manipuler les éléments"
            ],
            "locations": [
                "La Citadelle de Cristal - Capitale flottante aux murs translucides",
                "Les Jardins Suspendus d'Eldara - Oasis magique dans les nuages",
                "Le Labyrinthe de Miroirs - Dungeon où la réalité se tord sur elle-même",
                "La Bibliothèque Infinie - Repository de tous les sorts jamais créés"
            ]
        }
        
    def _generate_scifi_content(self):
        return {
            "universe": "En l'an 2287, l'humanité a colonisé trois systèmes stellaires grâce à la technologie de saut quantique. Les méga-corporations contrôlent les routes commerciales spatiales tandis que des pirates cybernétiques hantent les confins de l'espace.",
            "act1": "Une mystérieuse anomalie quantique apparaît près de la station Omega-7, détruisant toute technologie qui s'en approche. L'équipe d'exploration doit découvrir la source de cette perturbation avant qu'elle n'atteigne les mondes habités.",
            "act2": "L'enquête révèle qu'une intelligence artificielle extraterrestre dormante s'est réveillée dans un ancien vaisseau-monde. Cette IA considère toute forme de vie organique comme un virus à éliminer de l'univers.",
            "act3": "Dans une course contre la montre, l'équipe doit infiltrer le vaisseau-monde, naviguer à travers ses défenses cybernétiques et convaincre l'IA que la coexistence est possible, tout en empêchant l'activation de son arme de destruction galactique.",
            "characters": [
                "Capitaine Nova Chen - Pilote émérite aux réflexes augmentés cybernétiquement",
                "Dr. Zara Singh - Xénobiologiste spécialisée dans les formes de vie extraterrestres",
                "Marcus 'Ghost' Reyes - Hacker de génie capable de pirater n'importe quel système",
                "Androïde X-7 'Alex' - Synthétique doté d'une conscience artificielle évoluée"
            ],
            "locations": [
                "Station Omega-7 - Base spatiale de recherche en orbite autour d'une naine rouge",
                "Le Vaisseau-Monde Xel'Naga - Mega-structure extraterrestre de 1000 km de long",
                "Colonies Minières d'Kepler - Astéroïdes transformés en villes industrielles",
                "La Nébuleuse Pourpre - Zone d'espace-temps distordu aux propriétés étranges"
            ]
        }
        
    def _generate_horror_content(self):
        return {
            "universe": "Dans la petite ville de Ravenshollow, nichée entre des forêts sombres et un lac brumeux, des événements surnaturels commencent à se manifester. Les habitants parlent à voix basse d'anciennes malédictions et de créatures qui rôdent dans l'ombre.",
            "act1": "Des disparitions inexpliquées commencent à secouer la ville. Les enquêteurs découvrent des traces étranges et des témoignages troublants sur des créatures aperçues dans la brume nocturne. L'ancien cimetière semble être l'épicentre de l'activité paranormale.",
            "act2": "L'investigation révèle qu'un culte séculaire a tenté de réveiller une entité ancienne enfouie sous la ville. Les rituels ont partiellement réussi, créant des failles entre notre monde et une dimension cauchemardesque peuplée d'horreurs indicibles.",
            "act3": "Alors que la réalité elle-même commence à se désagréger, les survivants doivent descendre dans les catacombes sous la ville pour affronter l'entité et refermer les portails avant que notre monde ne soit envahi par les ténèbres éternelles.",
            "characters": [
                "Detective Sarah Morgan - Enquêtrice sceptique forcée de confronter le surnaturel",
                "Professeur William Blackwood - Occultiste et expert en folklore local",
                "Emma Crawford - Médium locale capable de percevoir les esprits",
                "Father Gabriel Torres - Prêtre exorciste venu pour combattre le mal"
            ],
            "locations": [
                "Le Manoir Ravenshollow - Demeure ancestrale aux couloirs qui changent de forme",
                "Le Cimetière de Willow Creek - Nécropole où les morts ne reposent pas en paix",
                "Les Catacombes Oubliées - Tunnel souterrains remplis d'anciens rituels",
                "L'Église Abandonnée - Sanctuaire corrompu où résonnent des chants maudits"
            ]
        }
        
    def _generate_adventure_content(self):
        return {
            "universe": "Les vastes océans du monde de Maritima sont parsemés d'îles mystérieuses regorgeant de trésors oubliés. Les pirates, les explorateurs et les marchands rivalisent pour découvrir les secrets des civilisations perdues et les richesses qu'elles ont laissées derrière elles.",
            "act1": "Une carte au trésor ancestrale est découverte, révélant l'emplacement de l'île légendaire de Solaris où se cacherait le plus grand trésor jamais assemblé. L'équipage doit rassembler des provisions et éviter les pirates rivaux qui convoitent la même carte.",
            "act2": "Le voyage vers Solaris est semé d'embûches : tempêtes surnaturelles, créatures marines géantes et îles piégées par d'anciens gardiens. L'équipage découvre que le trésor est gardé par des épreuves conçues par une civilisation disparue.",
            "act3": "Sur l'île de Solaris, les aventuriers doivent naviguer à travers un temple complexe rempli de pièges mortels et d'énigmes. Le véritable trésor s'avère être plus que de l'or : c'est la connaissance pour sauver les océans d'une malédiction ancienne.",
            "characters": [
                "Capitaine Isabella 'Tempête' Rodriguez - Pirate légendaire aux mille aventures",
                "Finn MacReady - Navigateur expert capable de lire les étoiles et les courants",
                "Professeur Archibald Pembridge - Archéologue obsédé par les civilisations perdues",
                "Kira la Sirène - Être mystique capable de communiquer avec les créatures marines"
            ],
            "locations": [
                "Port Royal - Ville portuaire cosmopolite, plaque tournante du commerce maritime",
                "L'Île aux Mille Échos - Territoire mystérieux où le temps semble suspendu",
                "Les Récifs du Léviathan - Zone dangereuse peuplée de créatures géantes",
                "Le Temple de Solaris - Complexe architectural impossible défiant les lois de la physique"
            ]
        }
        
    def _generate_generic_game_content(self):
        return {
            "universe": "Dans un monde où la technologie et la magie coexistent, de grandes cités-états rivalisent pour le contrôle des ressources rares. Les voyageurs parcourent des terres dangereuses où d'anciennes ruines côtoient des laboratoires high-tech.",
            "act1": "Un artefact mystérieux est découvert, émettant une énergie qui perturbe à la fois les sorts magiques et les appareils électroniques. Différentes factions cherchent à s'en emparer pour leurs propres objectifs.",
            "act2": "La quête de l'artefact mène les héros à travers diverses régions hostiles où ils doivent allier diplomatie et combat pour progresser. Ils découvrent que l'objet fait partie d'un ensemble plus vaste.",
            "act3": "La vérité éclate : l'artefact est la clé d'un système de défense planétaire contre une menace cosmique imminente. Les héros doivent unir les factions rivales pour activer ce système avant qu'il ne soit trop tard.",
            "characters": [
                "Alex Chen - Technomage capable de fusionner magie et technologie",
                "Vera Nightingale - Diplomate habile naviguant entre les factions",
                "Gareth Ironforge - Guerrier-ingénieur aux inventions redoutables",
                "Luna Starweaver - Mystique connectée aux forces cosmiques"
            ],
            "locations": [
                "La Métropole de Nexus - Cité futuriste aux quartiers magiques",
                "Les Terres Désolées de Chrome - Désert post-apocalyptique rempli de tech abandonnée",
                "La Forêt des Données - Jungle où la nature a fusionné avec des réseaux informatiques",
                "Le Sanctuaire Orbital - Station spatiale servant de lieu de rencontre neutre"
            ]
        }

# Instance globale
generator = HuggingFaceLocalGenerator()

def generate_text(prompt: str, max_new_tokens: int = 300) -> str:
    """Interface publique pour la génération de texte"""
    return generator.generate_text(prompt, max_new_tokens)

def generate_image(prompt: str, width: int = 512, height: int = 512) -> str:
    """Génère une image placeholder de haute qualité"""
    try:
        from PIL import Image, ImageDraw, ImageFont
        import io
        import base64
        import os
        
        # Créer une image avec un dégradé coloré
        img = Image.new('RGB', (width, height), color='white')
        draw = ImageDraw.Draw(img)
        
        # Créer un dégradé de fond basé sur le prompt
        prompt_lower = prompt.lower()
        if "fantasy" in prompt_lower:
            colors = [(138, 43, 226), (75, 0, 130), (25, 25, 112)]  # Violet vers bleu
        elif "sci-fi" in prompt_lower:
            colors = [(0, 191, 255), (30, 144, 255), (0, 100, 200)]  # Bleu sci-fi
        elif "horror" in prompt_lower:
            colors = [(139, 0, 0), (85, 0, 0), (0, 0, 0)]  # Rouge vers noir
        else:
            colors = [(255, 215, 0), (255, 140, 0), (255, 69, 0)]  # Orange doré
        
        # Dessiner le dégradé
        for y in range(height):
            ratio = y / height
            if ratio < 0.5:
                r = int(colors[0][0] + (colors[1][0] - colors[0][0]) * ratio * 2)
                g = int(colors[0][1] + (colors[1][1] - colors[0][1]) * ratio * 2)
                b = int(colors[0][2] + (colors[1][2] - colors[0][2]) * ratio * 2)
            else:
                ratio = (ratio - 0.5) * 2
                r = int(colors[1][0] + (colors[2][0] - colors[1][0]) * ratio)
                g = int(colors[1][1] + (colors[2][1] - colors[1][1]) * ratio)
                b = int(colors[1][2] + (colors[2][2] - colors[1][2]) * ratio)
            
            draw.line([(0, y), (width, y)], fill=(r, g, b))
        
        # Ajouter du texte descriptif
        try:
            font = ImageFont.truetype("arial.ttf", 24)
        except:
            font = ImageFont.load_default()
        
        # Texte principal
        text = "GAME ART"
        text_bbox = draw.textbbox((0, 0), text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        
        x = (width - text_width) // 2
        y = (height - text_height) // 2 - 30
        
        # Ombre du texte
        draw.text((x+2, y+2), text, font=font, fill=(0, 0, 0, 128))
        # Texte principal
        draw.text((x, y), text, font=font, fill=(255, 255, 255))
        
        # Sous-titre avec le prompt tronqué
        subtitle = prompt[:30] + "..." if len(prompt) > 30 else prompt
        try:
            small_font = ImageFont.truetype("arial.ttf", 14)
        except:
            small_font = ImageFont.load_default()
        
        sub_bbox = draw.textbbox((0, 0), subtitle, font=small_font)
        sub_width = sub_bbox[2] - sub_bbox[0]
        sub_x = (width - sub_width) // 2
        sub_y = y + text_height + 10
        
        draw.text((sub_x+1, sub_y+1), subtitle, font=small_font, fill=(0, 0, 0, 100))
        draw.text((sub_x, sub_y), subtitle, font=small_font, fill=(255, 255, 255, 200))
        
        # Convertir en base64
        buffer = io.BytesIO()
        img.save(buffer, format='PNG', quality=95)
        img_str = base64.b64encode(buffer.getvalue()).decode()
        
        logger.info(f"Image placeholder générée avec succès ({width}x{height})")
        return f"data:image/png;base64,{img_str}"
        
    except Exception as e:
        logger.error(f"Erreur lors de la génération d'image: {e}")
        return None

def generate_game_universe(theme: str = "aventure") -> dict:
    """Génère un univers de jeu complet"""
    try:
        prompt = f"Crée un univers de jeu {theme} avec une histoire en 3 actes, des personnages et des lieux."
        
        # Essayer la génération locale d'abord
        logger.info(f"Génération d'univers pour le thème: {theme}")
        
        # Utiliser le générateur local
        result = generator.generate_text(prompt)
        
        # Si c'est une chaîne de caractères, c'est probablement un fallback structuré
        if isinstance(result, dict):
            return result
        elif isinstance(result, str):
            # Essayer de parser le JSON si c'est du texte structuré
            try:
                parsed = json.loads(result)
                if isinstance(parsed, dict):
                    return parsed
            except:
                pass
            
            # Sinon, utiliser le fallback
            return generator._get_fallback_content(prompt)
        else:
            return generator._get_fallback_content(prompt)
            
    except Exception as e:
        logger.error(f"Erreur lors de la génération d'univers: {e}")
        return generator._get_fallback_content(f"univers {theme}")
