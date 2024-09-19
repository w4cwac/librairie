from django.db import models
import datetime
from datetime import timedelta, date

class Emprunteur(models.Model):
    nom = models.CharField(max_length=155)
    prenom = models.CharField(max_length=155)
    bloque = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.nom} {self.prenom}'
    
    def nombre_emprunt(self):
        return self.media_emprunt.filter(disponible=False).count()
    
    def emprunt_en_retard(self):
        return self.media_emprunt.filter(date_retour__lt=date.today(), disponible=False).exists()
    
    def peut_emprunter(self):
        return self.nombre_emprunt() < 3

    def emprunter_media(self, media):
        if self.peut_emprunter():
            media.disponible = False
            media.emprunteur = self
            media.date_emprunt = datetime.date.today()
            media.date_retour = datetime.date.today() + timedelta(weeks=1)
            media.save()
        else:
            raise ValueError("Cet emprunteur a déjà 3 emprunts en cours ou a un emprunt en retard.")

class Media(models.Model):
    name = models.CharField(max_length=155)
    disponible = models.BooleanField(default=True)
    date_emprunt = models.DateField(null=True, blank=True)
    date_retour = models.DateField(null=True, blank=True)
    emprunteur = models.ForeignKey(Emprunteur, on_delete=models.SET_NULL, null=True, blank=True, related_name='media_emprunt')

    def rendre(self):
        if self.emprunteur:
            self.disponible = True
            self.emprunteur = None
            self.date_emprunt = None
            self.date_retour = None
            self.save()

    def emprunter(self, emprunteur):
        if not self.emprunteur:
            if emprunteur.peut_emprunter():
                self.emprunteur = emprunteur
                self.disponible = False
                self.date_emprunt = datetime.date.today()
                self.date_retour = self.date_emprunt + timedelta(weeks=1)
                self.save()
            else:
                raise ValueError('Vous ne pouvez pas emprunter plus de 3 médias ou vous avez un emprunt en retard')

    def get_media_type(self):
        return self.__class__.__name__
    
    def __str__(self):
        return f'{self.name} - {self.get_media_type()}'

class Livre(Media):
    auteur = models.CharField(max_length=155)

class Cd(Media):
    artiste = models.CharField(max_length=155)

class Dvd(Media):
    realisateur = models.CharField(max_length=155)

class JeuDePlateau(models.Model):
    nom = models.CharField(max_length=155)
    fabricant = models.CharField(max_length=155)
    description = models.CharField(max_length=155)

    def __str__(self):
        return self.nom
