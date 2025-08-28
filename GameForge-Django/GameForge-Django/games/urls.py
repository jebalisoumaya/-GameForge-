from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('create/', views.create_game, name='create_game'),
    path('explore/', views.explore, name='explore'),
    path('detail/<int:pk>/', views.detail, name='detail'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('favorites/', views.favorites, name='favorites'),
    path('toggle-favorite/<int:pk>/', views.toggle_favorite, name='toggle_favorite'),
    path('toggle-visibility/<int:pk>/', views.toggle_visibility, name='toggle_visibility'),
    path('export-pdf/<int:pk>/', views.export_pdf, name='export_pdf'),
]
