import os, io, base64, random
from PIL import Image, ImageDraw, ImageFont
import requests

HF_API_KEY = os.getenv("HUGGINGFACE_API_KEY", "").strip()
HF_TEXT_URL = "https://api-inference.huggingface.co/models/mistralai/Mixtral-8x7B-Instruct"  # indicatif
HF_IMAGE_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2-1"

def _headers():
    if HF_API_KEY:
        return {"Authorization": f"Bearer {HF_API_KEY}"}
    return {}

def generate_text(prompt: str, max_new_tokens: int = 512) -> str:
    if not HF_API_KEY:
        random.seed(hash(prompt) % (2**32))
        blocks = [
            "Univers: Un monde où la technologie et la magie s'entremêlent, "
            "avec des cités verticales et des ruines anciennes.",
            "Acte I: Le protagoniste découvre un artefact et attire l'attention "
            "d'une faction secrète.",
            "Acte II: Trahisons et révélations; une IA oubliée manipule les évènements.",
            "Acte III: Confrontation finale; choix moraux affectant l'issue.",
            "Twist: L'artefact est un fragment de mémoire du héros, effacé autrefois.",
            "Personnages: [Ari, éclaireuse], [Kade, technomage], [Sera, archiviste].",
            "Lieux: La Verrière, Les Souterrains, L'Observatoire Astral."
        ]
        return "\n".join(blocks)
    try:
        payload = {"inputs": prompt, "parameters": {"max_new_tokens": max_new_tokens}}
        r = requests.post(HF_TEXT_URL, headers=_headers(), json=payload, timeout=60)
        r.raise_for_status()
        data = r.json()
        if isinstance(data, list) and data:
            # Some HF models return [{"generated_text": "..."}]
            return data[0].get("generated_text") or str(data)
        return str(data)
    except Exception as e:
        return f"Univers: Génération hors-ligne.\n{str(e)}"

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
