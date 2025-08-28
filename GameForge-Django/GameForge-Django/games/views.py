import io, random
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.db.models import Q
from django.core.files.base import ContentFile

from .models import GameProject, Favorite, DailyUsage
from .forms import GamePromptForm
from .utils.generator import generate_full

def home(request):
    q = request.GET.get("q","").strip()
    games = GameProject.objects.filter(is_public=True)
    if q:
        games = games.filter(Q(title__icontains=q) | Q(genre__icontains=q))
    games = games.order_by("-created_at")
    return render(request, "home.html", {"games": games, "q": q})

@login_required
def create_game(request):
    if request.method == "POST":
        if not DailyUsage.can_increment(request.user, limit=10):
            messages.error(request, "Limite quotidienne atteinte. Réessayez demain.")
            return redirect("dashboard")
        form = GamePromptForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.created_by = request.user
            instance.is_public = True
            instance.save()
            sections, char_img, env_img = generate_full(
                instance.title, instance.genre, instance.ambiance, instance.keywords, instance.references
            )
            instance.universe_text = sections.get("universe","").strip()
            instance.story_act1 = sections.get("act1","").strip()
            instance.story_act2 = sections.get("act2","").strip()
            instance.story_act3 = sections.get("act3","").strip()
            instance.story_twist = sections.get("twist","").strip()
            instance.characters = sections.get("characters", [])
            instance.locations = sections.get("locations", [])
            if char_img:
                instance.character_image.save(f"{instance.pk}_char.png", ContentFile(char_img), save=False)
            if env_img:
                instance.environment_image.save(f"{instance.pk}_env.png", ContentFile(env_img), save=False)
            instance.save()
            DailyUsage.increment(request.user)
            messages.success(request, "Jeu généré.")
            return redirect("detail", pk=instance.pk)
    else:
        form = GamePromptForm()
    return render(request, "create.html", {"form": form})

@login_required
def explore(request):
    # génération libre avec valeurs aléatoires
    genres = ["RPG","FPS","Metroidvania","Visual Novel","Strategy","Puzzle"]
    ambs = ["cyberpunk","dark fantasy","onirique","post-apo","low poly pastel","pixel art"]
    keys = ["boucle temporelle","IA rebelle","vengeance","exploration","alchimie","méchas"]
    params = {
        "title": f"Prototype #{random.randint(1000,9999)}",
        "genre": random.choice(genres),
        "ambiance": random.choice(ambs),
        "keywords": ", ".join(random.sample(keys, k=2)),
        "references": "indie mix"
    }
    if not DailyUsage.can_increment(request.user, limit=10):
        messages.error(request, "Limite quotidienne atteinte. Réessayez demain.")
        return redirect("dashboard")
    instance = GameProject.objects.create(created_by=request.user, is_public=True, **params)
    sections, char_img, env_img = generate_full(
        instance.title, instance.genre, instance.ambiance, instance.keywords, instance.references
    )
    instance.universe_text = sections.get("universe","").strip()
    instance.story_act1 = sections.get("act1","").strip()
    instance.story_act2 = sections.get("act2","").strip()
    instance.story_act3 = sections.get("act3","").strip()
    instance.story_twist = sections.get("twist","").strip()
    instance.characters = sections.get("characters", [])
    instance.locations = sections.get("locations", [])
    if char_img:
        instance.character_image.save(f"{instance.pk}_char.png", ContentFile(char_img), save=False)
    if env_img:
        instance.environment_image.save(f"{instance.pk}_env.png", ContentFile(env_img), save=False)
    instance.save()
    DailyUsage.increment(request.user)
    messages.success(request, "Exploration libre: jeu généré.")
    return redirect("detail", pk=instance.pk)

def detail(request, pk):
    game = get_object_or_404(GameProject, pk=pk)
    if not game.is_public and (not request.user.is_authenticated or game.created_by != request.user):
        messages.error(request, "Ce projet est privé.")
        return redirect("home")
    is_fav = False
    if request.user.is_authenticated:
        is_fav = Favorite.objects.filter(user=request.user, game=game).exists()
    return render(request, "detail.html", {"game": game, "is_fav": is_fav})

@login_required
def dashboard(request):
    games = GameProject.objects.filter(created_by=request.user).order_by("-created_at")
    return render(request, "dashboard.html", {"games": games})

@login_required
def favorites(request):
    favs = Favorite.objects.filter(user=request.user).select_related("game").order_by("-created_at")
    return render(request, "favorites.html", {"favs": favs})

@login_required
def toggle_favorite(request, pk):
    game = get_object_or_404(GameProject, pk=pk)
    fav = Favorite.objects.filter(user=request.user, game=game).first()
    if fav:
        fav.delete()
        messages.info(request, "Retiré des favoris.")
    else:
        Favorite.objects.create(user=request.user, game=game)
        messages.success(request, "Ajouté aux favoris.")
    return redirect("detail", pk=pk)

@login_required
def toggle_visibility(request, pk):
    game = get_object_or_404(GameProject, pk=pk, created_by=request.user)
    game.is_public = not game.is_public
    game.save()
    messages.success(request, f"Visibilité modifiée: {'Public' if game.is_public else 'Privé'}.")
    return redirect("detail", pk=pk)

@login_required
def export_pdf(request, pk):
    from reportlab.lib.pagesizes import A4
    from reportlab.pdfgen import canvas
    from reportlab.lib.units import cm

    game = get_object_or_404(GameProject, pk=pk, created_by=request.user)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="GameForge_{game.pk}.pdf"'
    p = canvas.Canvas(response, pagesize=A4)
    width, height = A4

    def draw_wrapped(text, x, y, max_width):
        lines = []
        for paragraph in text.split("\n"):
            words = paragraph.split()
            line = ""
            for w in words:
                test = (line + " " + w).strip()
                if p.stringWidth(test, "Helvetica", 10) > max_width:
                    lines.append(line)
                    line = w
                else:
                    line = test
            lines.append(line)
        for ln in lines:
            p.drawString(x, y, ln)
            y -= 12
        return y

    p.setFont("Helvetica-Bold", 16)
    p.drawString(2*cm, 28*cm, f"{game.title} ({game.genre})")
    p.setFont("Helvetica", 10)
    y = 26.5*cm
    y = draw_wrapped("Ambiance: " + game.ambiance, 2*cm, y, 17*cm)
    y = draw_wrapped("Mots-clés: " + (game.keywords or "-"), 2*cm, y, 17*cm)
    y = draw_wrapped("Références: " + (game.references or "-"), 2*cm, y, 17*cm)
    y -= 6

    p.setFont("Helvetica-Bold", 12); p.drawString(2*cm, y, "Univers"); y -= 14
    p.setFont("Helvetica", 10); y = draw_wrapped(game.universe_text or "-", 2*cm, y, 17*cm); y -= 6

    p.setFont("Helvetica-Bold", 12); p.drawString(2*cm, y, "Scénario"); y -= 14
    p.setFont("Helvetica", 10)
    y = draw_wrapped("Acte I: " + (game.story_act1 or "-"), 2*cm, y, 17*cm)
    y = draw_wrapped("Acte II: " + (game.story_act2 or "-"), 2*cm, y, 17*cm)
    y = draw_wrapped("Acte III: " + (game.story_act3 or "-"), 2*cm, y, 17*cm)
    y = draw_wrapped("Twist: " + (game.story_twist or "-"), 2*cm, y, 17*cm)

    p.showPage()
    p.setFont("Helvetica-Bold", 12); p.drawString(2*cm, 28*cm, "Personnages"); p.setFont("Helvetica", 10)
    y = 26.5*cm
    for ch in (game.characters or []):
        y = draw_wrapped("- " + str(ch), 2*cm, y, 17*cm)
    if not (game.characters or []):
        p.drawString(2*cm, y, "-")
    y -= 12
    p.setFont("Helvetica-Bold", 12); p.drawString(2*cm, y, "Lieux"); y -= 14; p.setFont("Helvetica", 10)
    for loc in (game.locations or []):
        y = draw_wrapped("- " + str(loc), 2*cm, y, 17*cm)
    if not (game.locations or []):
        p.drawString(2*cm, y, "-")
    p.showPage()
    p.save()
    return response
