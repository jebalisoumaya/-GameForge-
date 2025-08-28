from django.contrib import admin
from .models import GameProject, Favorite, DailyUsage

@admin.register(GameProject)
class GameProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "genre", "created_by", "is_public", "created_at")
    search_fields = ("title", "genre", "ambiance", "keywords")
    list_filter = ("genre", "is_public", "created_at")

admin.site.register(Favorite)
admin.site.register(DailyUsage)
