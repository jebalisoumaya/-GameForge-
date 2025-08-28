from django.conf import settings
from django.db import models
from django.utils import timezone

class GameProject(models.Model):
    GENRE_CHOICES = [
        ("RPG", "RPG"),
        ("FPS", "FPS"),
        ("Metroidvania", "Metroidvania"),
        ("Visual Novel", "Visual Novel"),
        ("Strategy", "Strategy"),
        ("Puzzle", "Puzzle"),
    ]
    title = models.CharField(max_length=120)
    genre = models.CharField(max_length=32, choices=GENRE_CHOICES)
    ambiance = models.CharField(max_length=120)
    keywords = models.CharField(max_length=200, blank=True)
    references = models.CharField(max_length=200, blank=True)

    universe_text = models.TextField(blank=True)
    story_act1 = models.TextField(blank=True)
    story_act2 = models.TextField(blank=True)
    story_act3 = models.TextField(blank=True)
    story_twist = models.TextField(blank=True)

    characters = models.JSONField(default=list, blank=True)
    locations = models.JSONField(default=list, blank=True)

    character_image = models.ImageField(upload_to="characters/", blank=True, null=True)
    environment_image = models.ImageField(upload_to="environments/", blank=True, null=True)

    is_public = models.BooleanField(default=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Favorite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    game = models.ForeignKey(GameProject, on_delete=models.CASCADE, related_name='favorites')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'game')

class DailyUsage(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateField()
    count = models.PositiveIntegerField(default=0)

    @classmethod
    def can_increment(cls, user, limit=10):
        today = timezone.localdate()
        obj, _ = cls.objects.get_or_create(user=user, date=today)
        return obj.count < limit

    @classmethod
    def increment(cls, user):
        today = timezone.localdate()
        obj, _ = cls.objects.get_or_create(user=user, date=today)
        obj.count += 1
        obj.save()
