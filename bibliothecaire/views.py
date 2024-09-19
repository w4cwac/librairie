from django.shortcuts import render, redirect, get_object_or_404
from .models import Media, Emprunteur, JeuDePlateau
from .forms import MediaTypeForm, LivreForm, CdForm, DvdForm, EmprunteurForm, JeuDePlateauForm
from datetime import date, timedelta
from django.contrib import messages

def choix_media_type(request):
    if request.method == 'POST':
        form = MediaTypeForm(request.POST)
        if form.is_valid():
            media_type = form.cleaned_data['media_type']
            return redirect ('ajout_media', media_type=media_type)

    else:
        form = MediaTypeForm()
    return render(request, 'bibliothecaire/choix_media_type.html', {'form':form})

def ajout_media(request, media_type):
    if media_type == 'Livre':
        FormClass = LivreForm
    elif media_type == 'Cd':
        FormClass = CdForm
    elif media_type == 'Dvd':
        FormClass = DvdForm
    else:
        return redirect('choix_media_type')
    
    if request.method == 'POST':
        form = FormClass(request.POST)
        if form.is_valid():
            form.save()
            return redirect('media_list')
    else:
        form = FormClass()

    return render(request, 'bibliothecaire/ajout_media.html', {'form': form, 'media_type': media_type })


def media_list(request):
    medias = Media.objects.all()
    emprunteurs = Emprunteur.objects.all()
    return render(request, 'bibliothecaire/media_list.html', {'medias': medias, 'emprunteurs': emprunteurs})


def create_emprunteur(request):
    if request.method == 'POST':
        form = EmprunteurForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('emprunteur_list')
    
    else:
        form = EmprunteurForm()

    return render (request, 'bibliothecaire/create_emprunteur.html', {'form': form})
    

def emprunteur_list(request):
    emprunteurs = Emprunteur.objects.all()
    return render(request, 'bibliothecaire/emprunteur_list.html', {'emprunteurs': emprunteurs})

def maj_emprunteur(request, emprunteur_id):
    emprunteur = get_object_or_404(Emprunteur, id=emprunteur_id)
    if request.method == 'POST':
        form = EmprunteurForm(request.POST, instance=emprunteur)
        if form.is_valid():
            form.save()
            return redirect('emprunteur_list')
    
    else:
        form = EmprunteurForm(instance=emprunteur)
    return render(request, 'bibliothecaire/maj_emprunteur.html', {'form': form, 'emprunteur': emprunteur})

def delete_emprunteur(request, emprunteur_id):
    emprunteur = get_object_or_404(Emprunteur, id=emprunteur_id)
    if request.method == 'POST':
        emprunteur.delete()
        return redirect('emprunteur_list')
    return render(request, 'bibliothecaire/delete_emprunteur.html', {'emprunteur': emprunteur})


def media_emprunteur(request, emprunteur_id, media_id):
    media = get_object_or_404(Media, id=media_id)
    emprunteur = get_object_or_404(Emprunteur, id=emprunteur_id)
    
    if media.emprunteur is None:
        if emprunteur.media_set.count() < 3:
            media.emprunteur = emprunteur
            media.save()

        else:
            pass
    return redirect('media_list')


def emprunter_media(request, media_id):
    if request.method == "POST":
        emprunteur_id = request.POST.get('emprunteur_id')
        emprunteur = get_object_or_404(Emprunteur, id=emprunteur_id)
        media = get_object_or_404(Media, id=media_id)

        try:
            if media.emprunteur:
                raise ValueError("Ce média est déjà emprunté.")
            
            if emprunteur.media_emprunt.filter(disponible=False).count() >= 3:
                raise ValueError("Vous ne pouvez pas emprunter plus de 3 médias.")
            
            if emprunteur.emprunt_en_retard():
                raise ValueError('Vous avez un ou plusieurs emprunts en retard')

            media.emprunteur = emprunteur
            media.disponible = False
            media.date_emprunt = date.today()
            media.date_retour = date.today() + timedelta(weeks=1)
            media.save()

            messages.success(request, 'Media emprunté avec succès !')
            return redirect('media_list')
        
        except ValueError as e:
            messages.error(request, str(e))
            return redirect('media_list')
    else:
        return redirect('media_list')
    
def rendre_media(request, emprunteur_id, media_id):
    emprunteur = get_object_or_404(Emprunteur, id=emprunteur_id)
    media = get_object_or_404(Media, id=media_id)

    if media.emprunteur == emprunteur:
        media.disponible = True
        media.emprunteur = None
        media.date_emprunt = None
        media.date_retour = None
        media.save()

        return redirect('media_list')
    
def jeu_plateau_list(request):
    jeux = JeuDePlateau.objects.all()
    return render(request, 'bibliothecaire/jeu_plateau_list.html', {'jeux': jeux})

def ajout_plateau(request):
    if request.method == 'POST':
        form = JeuDePlateauForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('jeu_plateau_list')
    
    else:
        form = JeuDePlateauForm()

    return render(request, 'bibliothecaire/ajout_plateau.html', {'form': form})