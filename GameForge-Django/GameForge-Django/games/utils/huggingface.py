import os, io, base64, random
from PIL import Image, ImageDraw, ImageFont
import requests

HF_API_KEY = os.getenv("HUGGINGFACE_API_KEY", "").strip()
# Utiliser des modèles plus accessibles
HF_TEXT_URL = "https://api-inference.huggingface.co/models/microsoft/DialoGPT-medium"
HF_IMAGE_URL = "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5"

def _headers():
    if HF_API_KEY:
        return {"Authorization": f"Bearer {HF_API_KEY}"}
    return {}

def generate_text(prompt: str, max_new_tokens: int = 512) -> str:
    # Toujours générer du contenu de démonstration pour s'assurer que ça fonctionne
    random.seed(hash(prompt) % (2**32))
    
    # Génération basée sur le prompt pour plus de variété
    universes = [
        "Dans un monde où la technologie et la magie s'entremêlent, les cités verticales dominent un paysage de ruines anciennes. L'équilibre fragile entre les corporations et les mages rebelles menace de s'effondrer à tout moment.",
        "Un royaume flottant suspendu au-dessus des nuages, où les cristaux d'énergie alimentent une civilisation avancée. Mais les cristaux s'éteignent un à un, plongeant le monde dans l'obscurité.",
        "Une métropole cyberpunk où les hackers se battent contre des IA corrompues pour le contrôle du réseau neural global. La réalité et le virtuel se mélangent dangereusement.",
        "Un monde post-apocalyptique où la nature a repris ses droits, et où les derniers humains coexistent avec des créatures mutantes dans des cités-jardins fortifiées."
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
    
    # Sélection aléatoire basée sur le hash du prompt
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
    
    # Si on a une clé API, on essaie la génération AI, sinon on retourne le contenu de démo
    if HF_API_KEY:
        try:
            # Essayer plusieurs modèles si le premier échoue
            models_to_try = [
                "microsoft/DialoGPT-medium",
                "gpt2",
                "distilgpt2"
            ]
            
            for model in models_to_try:
                try:
                    url = f"https://api-inference.huggingface.co/models/{model}"
                    payload = {
                        "inputs": f"Génère un univers de jeu vidéo basé sur: {prompt}",
                        "parameters": {
                            "max_new_tokens": max_new_tokens,
                            "temperature": 0.7,
                            "do_sample": True
                        }
                    }
                    
                    r = requests.post(url, headers=_headers(), json=payload, timeout=30)
                    
                    if r.status_code == 200:
                        data = r.json()
                        if isinstance(data, list) and data:
                            ai_generated = data[0].get("generated_text", "")
                            if ai_generated and len(ai_generated) > len(prompt):
                                return ai_generated[len(prompt):].strip()
                        elif isinstance(data, dict) and "generated_text" in data:
                            ai_generated = data["generated_text"]
                            if len(ai_generated) > len(prompt):
                                return ai_generated[len(prompt):].strip()
                    
                except Exception as e:
                    print(f"Erreur avec le modèle {model}: {e}")
                    continue
            
        except Exception as e:
            print(f"Erreur générale de génération AI: {e}")
    
    # Retourner le contenu de démonstration dans tous les cas
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
    if not HF_API_KEY:
        img = _placeholder_image(prompt)
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        return buf.getvalue()
    try:
        r = requests.post(HF_IMAGE_URL, headers=_headers(), json={"inputs": prompt}, timeout=120)
        r.raise_for_status()
        return r.content  # image bytes
    except Exception as e:
        img = _placeholder_image(f"offline: {e}")
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        return buf.getvalue()
