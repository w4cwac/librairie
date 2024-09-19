from django.shortcuts import render
from bibliothecaire.models import Media, JeuDePlateau

def media_list(request):
    medias = Media.objects.all()
    jeux = JeuDePlateau.objects.all()
    return render(request, 'consultation/media_list.html', {'medias': medias, 'jeux': jeux})