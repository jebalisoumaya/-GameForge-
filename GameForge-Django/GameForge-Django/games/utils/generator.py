import re, json
from .huggingface import generate_text, generate_image

def _extract_sections(raw: str):
    sections = {"universe": "", "act1": "", "act2": "", "act3": "", "twist": "", "characters": [], "locations": []}
    lines = [l.strip() for l in raw.splitlines() if l.strip()]
    buf = []
    current = None
    for l in lines:
        low = l.lower()
        if low.startswith("univers"):
            current = "universe"
            continue
        if "acte i" in low or low.startswith("acte 1") or "acte i:" in low:
            current = "act1"; continue
        if "acte ii" in low or low.startswith("acte 2") or "acte ii:" in low:
            current = "act2"; continue
        if "acte iii" in low or low.startswith("acte 3") or "acte iii:" in low:
            current = "act3"; continue
        if "twist" in low or "retournement" in low:
            current = "twist"; continue
        if "personnage" in low:
            current = "characters"; continue
        if "lieu" in low:
            current = "locations"; continue
        if current in ("universe","act1","act2","act3","twist"):
            sections[current] += (l + "\n")
        elif current == "characters":
            sections["characters"].append(l.strip("- ").strip())
        elif current == "locations":
            sections["locations"].append(l.strip("- ").strip())
    if not sections["characters"]:
        # try bracket parsing
        for m in re.findall(r"\[(.*?)\]", raw):
            sections["characters"].append(m)
    if not sections["locations"]:
        for m in re.findall(r"Lieux?\s*:\s*(.*)", raw):
            sections["locations"].extend([s.strip() for s in m.split(",")])
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
