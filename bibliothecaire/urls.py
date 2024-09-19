from django.urls import path
from .views import choix_media_type, ajout_media, media_list, create_emprunteur, emprunteur_list, ajout_plateau, jeu_plateau_list, emprunter_media, rendre_media, maj_emprunteur, delete_emprunteur

urlpatterns = [
    path('', media_list, name='media_list'),
    path('choix_media_type/', choix_media_type, name='choix_media_type'),
    path('ajout_media/<str:media_type>/', ajout_media, name='ajout_media'),
    path('create_emprunteur/', create_emprunteur, name='create_emprunteur'),
    path('emprunteur_list/', emprunteur_list, name='emprunteur_list'),
    path('media/<int:media_id>/emprunter/', emprunter_media, name='emprunter_media'),
    path('ajout_plateau/', ajout_plateau, name='ajout_plateau'),
    path('jeu_plateau_list/', jeu_plateau_list, name='jeu_plateau_list'),
    path('emprunteur/<int:emprunteur_id>/media/<int:media_id>/rendre/', rendre_media, name='rendre_media'),
    path('emprunteur/<int:emprunteur_id>/maj/', maj_emprunteur, name='maj_emprunteur'),
    path('emprunteur/<int:emprunteur_id>/delete/', delete_emprunteur, name='delete_emprunteur'),
]