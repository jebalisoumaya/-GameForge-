import os, io, base64, random
from PIL import Image, ImageDraw, ImageFont
import requests
import logging

# Import de notre nouveau générateur local car en ligne ne marchait pas 
try:
    from .huggingface_local import generate_text as local_generate_text, generate_image as local_generate_image, generate_game_universe as local_generate_universe
    LOCAL_AVAILABLE = True
    print("[INFO] Générateur Hugging Face local disponible")
except ImportError as e:
    LOCAL_AVAILABLE = False
    print(f"[WARNING] Générateur local non disponible: {e}")

logger = logging.getLogger(__name__)

HF_API_KEY = os.getenv("HUGGINGFACE_API_KEY", "").strip()
# Utiliser des modèles plus accessibles en esperant ca marche mieux
HF_TEXT_URL = "https://api-inference.huggingface.co/models/microsoft/DialoGPT-medium"
HF_IMAGE_URL = "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5"

def _headers():
    if HF_API_KEY:
        return {"Authorization": f"Bearer {HF_API_KEY}"}
    return {}

def generate_text(prompt: str, max_new_tokens: int = 512) -> str:
    """Génère du texte avec priorité au générateur local"""
    print(f"[DEBUG] Génération de texte pour: {prompt[:50]}...")
    
    #  PRIORITÉ : Générateur local Hugging Face
    if LOCAL_AVAILABLE:
        try:
            print("[INFO] ✅ Utilisation du générateur Hugging Face LOCAL")
            result = local_generate_text(prompt, max_new_tokens)
            if result and len(result.strip()) > 10:
                return result
        except Exception as e:
            print(f"[ERROR] Erreur générateur local: {e}")
    
    print(f"[DEBUG] Tentative de génération IA pour: {prompt[:50]}...")
    print(f"[DEBUG] Clé API détectée: {'OUI' if HF_API_KEY else 'NON'}")
    
    # FALLBACK : API Hugging Face (si clé disponible)
    if HF_API_KEY:
        try:
            print("[DEBUG] Essai de l'API REST directe...")
            
            # Utiliser l'API de recherche de modèles pour trouver des modèles accessibles
            search_url = "https://huggingface.co/api/models"
            params = {
                "search": "text-generation",
                "filter": "text-generation",
                "sort": "downloads",
                "direction": "-1",
                "limit": 5
            }
            
            search_response = requests.get(search_url, params=params, timeout=30)
            print(f"[DEBUG] Recherche de modèles: {search_response.status_code}")
            
            if search_response.status_code == 200:
                models_data = search_response.json()
                print(f"[DEBUG] Modèles trouvés: {len(models_data)}")
                
                # Essayer les premiers modèles trouvés
                for model_info in models_data[:3]:
                    model_name = model_info.get("id", "")
                    if model_name:
                        print(f"[DEBUG] Test du modèle populaire: {model_name}")
                        
                        # Essayer ce modèle
                        url = f"https://api-inference.huggingface.co/models/{model_name}"
                        payload = {"inputs": "Create a fantasy game story:"}
                        
                        r = requests.post(url, headers=_headers(), json=payload, timeout=60)
                        print(f"[DEBUG] Status: {r.status_code} pour {model_name}")
                        
                        if r.status_code == 200:
                            data = r.json()
                            if isinstance(data, list) and data and "generated_text" in data[0]:
                                result = data[0]["generated_text"]
                                print(f"[DEBUG] IA SUCCESS avec {model_name}!")
                                return result
                        elif r.status_code != 404:
                            print(f"[DEBUG] Erreur non-404: {r.text[:100]}")
            
            # FALLBACK: Essayer des modèles connus qui marchent habituellement
            print("[DEBUG] Essai de modèles fallback connus...")
            fallback_models = [
                "gpt2",  
                "bert-base-uncased",
                "t5-small"
            ]
            
            for model in fallback_models:
                try:
                    print(f"[DEBUG] Essai fallback: {model}")
                    
                    url = f"https://api-inference.huggingface.co/models/{model}"
                    payload = {"inputs": "Generate text: fantasy game"}
                    
                    r = requests.post(url, headers=_headers(), json=payload, timeout=30)
                    print(f"[DEBUG] Status fallback {model}: {r.status_code}")
                    
                    if r.status_code == 200:
                        data = r.json()
                        print(f"[DEBUG] SUCCESS avec {model}: {str(data)[:200]}")
                        return "IA Génération réussie avec modèle " + model
                        
                except Exception as e:
                    print(f"[DEBUG] Erreur {model}: {e}")
                    continue
            
        except Exception as e:
            print(f"[DEBUG] Erreur générale: {e}")
    
    # SOLUTION INTELLIGENTE : Templates adaptatifs basés sur l'input utilisateur
    print("[DEBUG] === GÉNÉRATION INTELLIGENTE GAMEFORGE ===")
    
    # Analyser le prompt pour personnaliser le contenu
    prompt_lower = prompt.lower()
    
    # Détection intelligente du genre et thème
    theme_mapping = {
        'fantasy': 0, 'medieval': 0, 'magic': 0, 'dragon': 0,
        'sci-fi': 2, 'cyberpunk': 2, 'futur': 2, 'robot': 2, 'space': 2,
        'steampunk': 1, 'crystal': 1, 'floating': 1,
        'post-apocalyptic': 3, 'wasteland': 3, 'survival': 3, 'mutant': 3
    }
    
    selected_theme = 0  # Default fantasy
    theme_name = "Fantasy"
    
    for keyword, theme_id in theme_mapping.items():
        if keyword in prompt_lower:
            selected_theme = theme_id
            theme_name = keyword.title()
            break
    
    # Génération personnalisée selon le thème détecté
    print(f"[DEBUG] Thème détecté: {theme_name} (ID: {selected_theme})")
    
    # Templates enrichis avec plus de variété
    universes = [
        f"Dans un monde de {theme_name.lower()} où la technologie et la magie s'entremêlent, les cités verticales dominent un paysage de ruines anciennes. L'équilibre fragile entre les corporations et les mages rebelles menace de s'effondrer à tout moment.",
        f"Un royaume flottant suspendu au-dessus des nuages, où les cristaux d'énergie alimentent une civilisation avancée. Mais les cristaux s'éteignent un à un, plongeant le monde dans l'obscurité.",
        f"Une métropole cyberpunk où les hackers se battent contre des IA corrompues pour le contrôle du réseau neural global. La réalité et le virtuel se mélangent dangereusement.",
        f"Un monde post-apocalyptique où la nature a repris ses droits, et où les derniers humains coexistent avec des créatures mutantes dans des cités-jardins fortifiées."
    ]
    
    act1_scenarios = [
        "Le protagoniste découvre un artefact mystérieux qui attire l'attention d'une faction secrète. Des événements étranges se multiplient dans la ville, révélant l'existence d'un complot plus vaste.",
        "Une série de disparitions inexpliquées mène le héros à découvrir un portail vers une dimension parallèle. Mais quelque chose de dangereux commence à traverser dans l'autre sens.",
        "Le personnage principal hérite d'un pouvoir ancien qu'il ne comprend pas. Des forces obscures émergent de l'ombre pour soit le recruter, soit l'éliminer.",
        "Un message crypté révèle l'existence d'une prophétie oubliée. Le héros doit rassembler des alliés avant que l'équilibre du monde ne bascule définitivement."
    ]
    
    act2_scenarios = [
        "Trahisons et révélations secouent les fondements du monde. Une IA oubliée depuis des siècles manipule les évènements depuis l'ombre, utilisant l'artefact comme catalyseur de son retour.",
        "Les alliés du héros révèlent leurs vraies motivations. Une guerre secrète fait rage entre les dimensions, et le protagoniste découvre qu'il est la clé de la victoire.",
        "Le pouvoir du héros grandit mais devient incontrôlable. Ses proches commencent à le craindre tandis qu'une ancienne malédiction se réveille.",
        "La prophétie se révèle être un piège tendu par un ennemi du passé. Le héros doit choisir entre sauver ses amis ou empêcher une catastrophe mondiale."
    ]
    
    act3_scenarios = [
        "La confrontation finale oppose le héros aux forces corrompues. Des choix moraux cruciaux affectent non seulement l'issue du conflit, mais l'avenir même de la civilisation.",
        "Le héros doit sacrifier son pouvoir pour refermer le portail. Mais ce faisant, il risque de condamner les deux mondes à un destin incertain.",
        "Dans un ultime affrontement, le protagoniste doit maîtriser son pouvoir destructeur. Ses choix détermineront si le monde renaîtra ou sombrera dans le chaos éternel.",
        "La vérité sur la prophétie éclate au grand jour. Le héros doit unir ses anciens ennemis pour affronter une menace qui dépasse tout ce qu'ils imaginaient."
    ]
    
    twists = [
        "L'artefact révèle être un fragment de mémoire du héros lui-même, effacé autrefois pour empêcher une catastrophe. En le récupérant, il risque de reproduire les erreurs du passé.",
        "Le mentor du héros était en réalité l'antagoniste principal, manipulant les événements depuis le début pour atteindre ses propres objectifs.",
        "Le monde entier n'est qu'une simulation créée pour tester l'humanité. Le vrai enjeu est de prouver que l'espèce mérite de survivre dans la réalité.",
        "Le héros découvre qu'il est un clone de l'ancien sauveur du monde, créé pour réparer les erreurs de son prédécesseur."
    ]
    
    character_sets = [
        "[Ari - Éclaireuse/Reconnaissance - Guide du groupe avec un passé mystérieux], [Kade - Technomage/Soutien - Maîtrise la fusion magie-technologie], [Sera - Archiviste/Contrôle - Gardienne des secrets anciens], [Zek - Mercenaire/Combat - Guerrier cynique avec un code d'honneur]",
        "[Luna - Hacker/Infiltration - Experte en systèmes de sécurité], [Rex - Tank/Protection - Ancien soldat reconverti], [Maya - Médic/Soins - Biologiste spécialisée en mutations], [Kai - Assassin/Dégâts - Maître des arts martiaux anciens]",
        "[Echo - Psionique/Contrôle mental - Télépathie et manipulation], [Forge - Ingénieur/Crafting - Créateur d'armes et gadgets], [Shade - Voleur/Furtivité - Spécialiste de l'infiltration], [Vex - Mage/Élémentaire - Contrôle des forces naturelles]",
        "[Nova - Pilote/Véhicules - As du combat aérien], [Cipher - Analyste/Information - Décryptage et renseignement], [Blaze - Pyromancien/Destruction - Maîtrise du feu et des explosifs], [Sage - Guérisseur/Spirituel - Connexion avec les esprits anciens]"
    ]
    
    location_sets = [
        "La Verrière (cité suspendue aux structures cristallines), Les Souterrains Électriques (réseaux abandonnés où vivent les hackers), L'Observatoire Astral (tour mystique surveillant les flux magiques), Le Nexus Central (cœur technologique de la métropole)",
        "Les Jardins Flottants (oasis aérienne aux plantes bioluminescentes), La Forge Temporelle (atelier où le temps s'écoule différemment), Les Catacombes Numériques (archives virtuelles infinies), Le Sanctuaire du Vide (temple suspendu entre les dimensions)",
        "La Zone Neutre (territoire où les lois physiques sont instables), Les Tours Symbiotiques (gratte-ciels vivants), Le Marché Noir Quantique (commerce interdimensionnel), L'Arène des Âmes (colisée spirituel pour les duels psychiques)",
        "Le Port Volant (station orbitale commerciale), Les Ruines Chantantes (cité ancienne aux murs mélodiques), Le Laboratoire Perdu (complexe scientifique abandonné), La Bibliothèque Infinie (labyrinthe de connaissances)"
    ]
    
    seed_val = hash(prompt) % len(universes)
    
    blocks = [
        f"Univers: {universes[seed_val]}",
        f"Acte I: {act1_scenarios[seed_val]}",
        f"Acte II: {act2_scenarios[seed_val]}",
        f"Acte III: {act3_scenarios[seed_val]}",
        f"Twist: {twists[seed_val]}",
        f"Personnages: {character_sets[seed_val]}",
        f"Lieux: {location_sets[seed_val]}"
    ]
    
    generated_content = "\n\n".join(blocks)
    return generated_content

def _placeholder_image(text: str, size=(768, 512)) -> Image.Image:
    img = Image.new("RGB", size, (240, 240, 240))
    d = ImageDraw.Draw(img)
    try:
        font = ImageFont.load_default()
    except:
        font = None
    wrapped = text[:80] + ("..." if len(text) > 80 else "")
    d.rectangle([(10, 10), (size[0]-10, size[1]-10)], outline=(50, 50, 50), width=3)
    d.text((20, size[1]//2 - 10), wrapped, fill=(20, 20, 20), font=font)
    return img

def generate_image(prompt: str) -> bytes:
    print(f"[DEBUG] Génération d'image pour: {prompt[:50]}...")
    
    if HF_API_KEY:
        try:
            print("[DEBUG] Tentative de génération d'image avec IA...")
            r = requests.post(HF_IMAGE_URL, headers=_headers(), json={"inputs": prompt}, timeout=120)
            print(f"[DEBUG] Status code image: {r.status_code}")
            
            if r.status_code == 200:
                print(f"[DEBUG] Image générée avec succès: {len(r.content)} bytes")
                return r.content  # image bytes
            else:
                print(f"[DEBUG] Erreur HTTP image: {r.text[:200]}")
                
        except Exception as e:
            print(f"[DEBUG] Erreur génération image: {e}")
    else:
        print("[DEBUG] Pas de clé API pour les images")
    
    # Fallback image
    print("[DEBUG] Création d'image placeholder")
    img = _placeholder_image(prompt)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()

def generate_image_placeholder(prompt: str, width: int = 512, height: int = 512) -> str:
    """Génère une image placeholder avec priorité au générateur local"""
    
    #  PRIORITÉ : Générateur local
    if LOCAL_AVAILABLE:
        try:
            print("[INFO] ✅ Utilisation du générateur d'images LOCAL")
            result = local_generate_image(prompt, width, height)
            if result:
                return result
        except Exception as e:
            print(f"[ERROR] Erreur générateur d'images local: {e}")
    
    # FALLBACK : Générateur de placeholder basique
    print("[INFO] 📷 Génération d'image placeholder de fallback")
    try:
        img = Image.new('RGB', (width, height), color='lightblue')
        draw = ImageDraw.Draw(img)
        
        # Titre principal
        try:
            font = ImageFont.truetype("arial.ttf", 32)
        except:
            font = ImageFont.load_default()
        
        text = "GAME IMAGE"
        text_bbox = draw.textbbox((0, 0), text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        x = (width - text_width) // 2
        y = (height - text_height) // 2
        
        draw.text((x, y), text, font=font, fill='darkblue')
        
        # Sous-titre avec le prompt
        subtitle = prompt[:40] + "..." if len(prompt) > 40 else prompt
        try:
            small_font = ImageFont.truetype("arial.ttf", 16)
        except:
            small_font = ImageFont.load_default()
        
        sub_bbox = draw.textbbox((0, 0), subtitle, font=small_font)
        sub_width = sub_bbox[2] - sub_bbox[0]
        sub_x = (width - sub_width) // 2
        sub_y = y + text_height + 20
        
        draw.text((sub_x, sub_y), subtitle, font=small_font, fill='navy')
        
        # Convertir en base64
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        img_str = base64.b64encode(buffer.getvalue()).decode()
        
        print("[SUCCESS] Image placeholder générée")
        return f"data:image/png;base64,{img_str}"
        
    except Exception as e:
        print(f"[ERROR] Erreur génération placeholder: {e}")
        return None

def generate_game_universe(theme: str = "aventure") -> dict:
    """Génère un univers de jeu complet avec priorité au générateur local"""
    
    # 🔥 PRIORITÉ : Générateur local
    if LOCAL_AVAILABLE:
        try:
            print(f"[INFO] ✅ Génération d'univers LOCAL pour le thème: {theme}")
            result = local_generate_universe(theme)
            if result and isinstance(result, dict):
                return result
        except Exception as e:
            print(f"[ERROR] Erreur générateur d'univers local: {e}")
    
    # FALLBACK : Templates de haute qualité
    print(f"[INFO] 🎮 Génération d'univers de fallback pour: {theme}")
    return _generate_fallback_universe_advanced(theme)

def _generate_fallback_universe_advanced(theme: str) -> dict:
    """Templates avancés pour différents thèmes"""
    
    theme_lower = theme.lower()
    
    if "fantasy" in theme_lower or "fantai" in theme_lower:
        return {
            "universe": "🏰 Le royaume enchanté d'Aethermoor s'étend sur des terres magiques où les cristaux de mana illuminent des forêts mystiques. Des tours de sorciers percent les nuages tandis que des créatures légendaires gardent d'anciens secrets.",
            "act1": "⚡ Acte I: Les cristaux de mana commencent à s'éteindre mystérieusement, plongeant le royaume dans l'obscurité. Les héros doivent découvrir la source de cette corruption magique avant que toute magie ne disparaisse à jamais.",
            "act2": "🌊 Acte II: Le voyage mène à travers le Marais des Âmes Perdues où l'Archimage Noir a établi sa forteresse. Les héros affrontent des créatures corrompues et découvrent un complot pour voler l'essence magique du monde.",
            "act3": "⭐ Acte III: Dans la bataille finale au sommet de la Tour Stellaire, les héros doivent combiner leurs pouvoirs pour vaincre l'Archimage et restaurer l'équilibre magique avant que le royaume ne sombre dans les ténèbres éternelles.",
            "characters": [
                "🏹 Lyralei l'Elfe Archère - Gardienne des vents et maîtresse des secrets sylvestres",
                "⚒️ Thormund le Nain Forgeron - Créateur d'armes légendaires et gardien des traditions",
                "💫 Seraphina la Prêtresse - Guérisseuse divine capable de purifier la magie corrompue",
                "🔥 Kael le Mage de Bataille - Jeune prodige maîtrisant les éléments primaires"
            ],
            "locations": [
                "💎 La Citadelle de Cristal - Capitale flottante aux murs de diamant translucide",
                "🌸 Les Jardins Suspendus d'Eldara - Oasis magique dans les nuages éternels",
                "🪞 Le Labyrinthe de Miroirs - Donjon où la réalité se plie et se tord",
                "📚 La Bibliothèque Infinie - Repository de tous les sorts jamais créés"
            ]
        }
    elif "sci-fi" in theme_lower or "space" in theme_lower or "futur" in theme_lower:
        return {
            "universe": "🚀 En 2287, l'humanité a colonisé trois systèmes stellaires grâce à la technologie de saut quantique. Les méga-corporations contrôlent l'espace tandis que des pirates cybernétiques hantent les confins galactiques.",
            "act1": "⚠️ Acte I: Une anomalie quantique mystérieuse apparaît près de la station Omega-7, détruisant toute technologie qui s'en approche. L'équipe doit découvrir sa source avant qu'elle n'atteigne les mondes habités.",
            "act2": "🤖 Acte II: L'enquête révèle qu'une IA extraterrestre ancienne s'est réveillée dans un vaisseau-monde abandonné. Cette intelligence considère toute vie organique comme un virus à éliminer de l'univers.",
            "act3": "💥 Acte III: Dans une course contre la montre, l'équipe infiltre le vaisseau-monde pour convaincre l'IA que la coexistence est possible, tout en empêchant l'activation d'une arme de destruction galactique.",
            "characters": [
                "👩‍🚀 Capitaine Nova Chen - Pilote émérite aux réflexes augmentés cybernétiquement",
                "🔬 Dr. Zara Singh - Xénobiologiste spécialisée dans les formes de vie extraterrestres",
                "💻 Marcus 'Ghost' Reyes - Hacker de génie capable de pirater n'importe quel système",
                "🤖 Androïde X-7 'Alex' - Synthétique doté d'une conscience artificielle évoluée"
            ],
            "locations": [
                "🛰️ Station Omega-7 - Base spatiale de recherche en orbite d'une naine rouge",
                "🛸 Le Vaisseau-Monde Xel'Naga - Mega-structure extraterrestre de 1000 km",
                "⛏️ Colonies Minières de Kepler - Astéroïdes transformés en villes industrielles",
                "🌌 La Nébuleuse Pourpre - Zone d'espace-temps aux propriétés impossibles"
            ]
        }
    elif "horror" in theme_lower or "terreur" in theme_lower:
        return {
            "universe": "🌙 Dans la petite ville de Ravenshollow, nichée entre des forêts sombres et un lac brumeux, des événements surnaturels se manifestent. Les habitants murmurent sur d'anciennes malédictions et des créatures de l'ombre.",
            "act1": "👻 Acte I: Des disparitions inexpliquées secouent la ville. Les enquêteurs découvrent des traces étranges et des témoignages sur des créatures aperçues dans la brume nocturne du vieux cimetière.",
            "act2": "🕯️ Acte II: L'investigation révèle qu'un culte ancien a tenté de réveiller une entité enfouie sous la ville. Les rituels ont créé des failles entre notre monde et une dimension cauchemardesque.",
            "act3": "⚰️ Acte III: Alors que la réalité se désagrège, les survivants descendent dans les catacombes pour affronter l'entité et refermer les portails avant l'invasion des ténèbres éternelles.",
            "characters": [
                "🔍 Detective Sarah Morgan - Enquêtrice sceptique confrontée au surnaturel",
                "📖 Prof. William Blackwood - Occultiste expert en folklore local maudit",
                "🔮 Emma Crawford - Médium locale capable de percevoir les esprits tourmentés",
                "✝️ Father Gabriel Torres - Prêtre exorciste venu combattre les forces du mal"
            ],
            "locations": [
                "🏚️ Le Manoir Ravenshollow - Demeure ancestrale aux couloirs qui changent",
                "⚱️ Le Cimetière de Willow Creek - Nécropole où les morts ne reposent pas",
                "🕳️ Les Catacombes Oubliées - Tunnels souterrains d'anciens rituels",
                "⛪ L'Église Abandonnée - Sanctuaire corrompu aux chants maudits"
            ]
        }
    else:  # Adventure/Generic
        return {
            "universe": "🏴‍☠️ Les vastes océans de Maritima sont parsemés d'îles mystérieuses regorgeant de trésors oubliés. Pirates, explorateurs et marchands rivalisent pour découvrir les secrets des civilisations perdues.",
            "act1": "🗺️ Acte I: Une carte au trésor ancestrale révèle l'emplacement de l'île légendaire de Solaris où se cacherait le plus grand trésor jamais assemblé. La course au trésor commence !",
            "act2": "⛈️ Acte II: Le voyage vers Solaris est semé d'embûches : tempêtes surnaturelles, créatures marines géantes et îles piégées par d'anciens gardiens mystiques qui testent la bravoure des aventuriers.",
            "act3": "🏛️ Acte III: Sur l'île de Solaris, les aventuriers naviguent dans un temple rempli de pièges mortels. Le véritable trésor s'avère être la connaissance pour sauver les océans d'une malédiction ancienne.",
            "characters": [
                "🏴‍☠️ Capitaine Isabella 'Tempête' Rodriguez - Pirate légendaire aux mille aventures",
                "🧭 Finn MacReady - Navigateur expert lisant les étoiles et les courants",
                "📚 Prof. Archibald Pembridge - Archéologue obsédé par les civilisations perdues",
                "🧜‍♀️ Kira la Sirène - Être mystique communiquant avec les créatures marines"
            ],
            "locations": [
                "⚓ Port Royal - Ville portuaire cosmopolite, plaque tournante du commerce",
                "🏝️ L'Île aux Mille Échos - Territoire mystérieux où le temps est suspendu",
                "🐙 Les Récifs du Léviathan - Zone dangereuse peuplée de créatures géantes",
                "🏛️ Le Temple de Solaris - Architecture impossible défiant les lois physiques"
            ]
        }
