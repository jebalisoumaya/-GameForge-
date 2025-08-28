import re, json
from .huggingface import generate_text, generate_image

def _extract_sections(raw: str):
    sections = {"universe": "", "act1": "", "act2": "", "act3": "", "twist": "", "characters": [], "locations": []}
    
    # Si le contenu brut est vide, générer du contenu de fallback
    if not raw or len(raw.strip()) < 50:
        raw = """Univers: Dans un monde mystérieux où magie et technologie coexistent, les héros doivent découvrir les secrets du passé pour sauver l'avenir.

Acte I: Le protagoniste découvre un artefact ancien qui révèle une prophétie oubliée. Des forces obscures se réveillent et menacent l'équilibre du monde.

Acte II: Les héros rassemblent des alliés et découvrent la véritable nature de la menace. Des révélations choquantes remettent en question tout ce qu'ils croyaient savoir.

Acte III: Dans une confrontation épique, les héros doivent faire des choix difficiles qui détermineront le destin du monde et de tous ses habitants.

Twist: L'ennemi principal était en réalité un ancien héros corrompu, et le seul moyen de le vaincre nécessite un sacrifice ultime.

Personnages: [Ayla - Mage/Contrôle - Gardienne des secrets anciens], [Riven - Guerrier/Tank - Protecteur loyal du groupe], [Zara - Voleuse/Dégâts - Espionne aux motivations mystérieuses], [Kai - Clerc/Soins - Guérisseur sage et patient]

Lieux: Le Temple Oublié (sanctuaire ancien rempli de mystères), La Cité Flottante (métropole suspendue dans les nuages), Les Grottes Cristallines (cavernes aux pouvoirs magiques), L'Arène Temporelle (lieu où le temps s'écoule différemment)"""
    
    # Diviser le texte par paragraphes
    paragraphs = [p.strip() for p in raw.split('\n\n') if p.strip()]
    
    for paragraph in paragraphs:
        lines = [l.strip() for l in paragraph.split('\n') if l.strip()]
        if not lines:
            continue
            
        first_line = lines[0].lower()
        
        # Extraction basée sur les mots-clés
        if first_line.startswith("univers"):
            sections["universe"] = paragraph.replace("Univers:", "").strip()
        elif "acte i" in first_line or first_line.startswith("acte 1"):
            sections["act1"] = paragraph.replace("Acte I:", "").replace("Acte 1:", "").strip()
        elif "acte ii" in first_line or first_line.startswith("acte 2"):
            sections["act2"] = paragraph.replace("Acte II:", "").replace("Acte 2:", "").strip()
        elif "acte iii" in first_line or first_line.startswith("acte 3"):
            sections["act3"] = paragraph.replace("Acte III:", "").replace("Acte 3:", "").strip()
        elif "twist" in first_line or "retournement" in first_line:
            sections["twist"] = paragraph.replace("Twist:", "").strip()
        elif "personnage" in first_line:
            # Extraire les personnages entre crochets
            content = paragraph.replace("Personnages:", "").strip()
            characters = re.findall(r'\[([^\]]+)\]', content)
            if characters:
                sections["characters"] = characters
            else:
                # Fallback: diviser par virgules
                parts = content.split(',')
                sections["characters"] = [p.strip() for p in parts if p.strip()]
        elif "lieu" in first_line:
            # Extraire les lieux
            content = paragraph.replace("Lieux:", "").strip()
            # Diviser par virgules et nettoyer
            locations = [loc.strip() for loc in content.split(',') if loc.strip()]
            sections["locations"] = locations
    
    # Vérifications de sécurité et fallbacks
    if not sections["universe"]:
        sections["universe"] = "Un monde fantastique rempli de mystères et d'aventures où les héros doivent affronter des défis extraordinaires."
    
    if not sections["act1"]:
        sections["act1"] = "Le protagoniste découvre sa destinée et entame une quête périlleuse pour sauver son monde."
    
    if not sections["act2"]:
        sections["act2"] = "Des révélations changent la donne et les héros doivent surmonter de nouveaux obstacles."
    
    if not sections["act3"]:
        sections["act3"] = "La confrontation finale détermine le sort du monde et l'accomplissement de la prophétie."
    
    if not sections["twist"]:
        sections["twist"] = "Un allié se révèle être l'ennemi, et le véritable pouvoir vient de l'intérieur du héros."
    
    if not sections["characters"]:
        sections["characters"] = [
            "Héros - Protagoniste/Leader - Destiné à sauver le monde",
            "Mentor - Sage/Guide - Détient les connaissances anciennes", 
            "Allié - Guerrier/Combat - Fidèle compagnon d'armes",
            "Oracle - Mystique/Magie - Voit l'avenir et guide les choix"
        ]
    
    if not sections["locations"]:
        sections["locations"] = [
            "Le Village Natal (point de départ paisible)",
            "La Forêt Enchantée (lieu mystique plein de dangers)",
            "Le Château du Mal (forteresse de l'antagoniste)",
            "Le Temple Final (lieu de la confrontation ultime)"
        ]
    
    return sections

def build_prompts(title, genre, ambiance, keywords, references):
    base = f"Titre: {title}\nGenre: {genre}\nAmbiance: {ambiance}\nMots-clés: {keywords}\nRéférences: {references}"
    sys = "Tu es un game designer senior. Rédige en français."
    text_prompt = sys + "\n" + base + "\n" +             "Génère: Univers détaillé; Acte I; Acte II; Acte III; Twist; Personnages (2-4, nom/classe/rôle/background/gameplay); Lieux (3+)."
    char_prompt = f"Portrait conceptuel stylisé d'un personnage principal, style {ambiance}, jeu {genre}, {keywords}"
    env_prompt = f"Environnement emblématique du jeu {title}, style {ambiance}, {keywords}"
    return text_prompt, char_prompt, env_prompt

def generate_full(title, genre, ambiance, keywords, references):
    text_prompt, char_prompt, env_prompt = build_prompts(title, genre, ambiance, keywords, references)
    raw = generate_text(text_prompt, max_new_tokens=600)
    sections = _extract_sections(raw)
    char_img = generate_image(char_prompt)
    env_img = generate_image(env_prompt)
    return sections, char_img, env_img
