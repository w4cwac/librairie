from django import forms
from .models import Media, Livre, Cd, Dvd, Emprunteur, JeuDePlateau

class MediaTypeForm(forms.Form):
    media_type = forms.ChoiceField(choices=[
        ('Livre', 'LIVRE'),
        ('Cd', 'CD'),
        ('Dvd', 'DVD'),
    ])

class MediaForm(forms.ModelForm):
    class Meta:
        model = Media
        fields = ['name']
        
class LivreForm(MediaForm):
    class Meta(MediaForm.Meta):
        model = Livre
        fields = MediaForm.Meta.fields + ['auteur']

class CdForm(MediaForm):
    class Meta(MediaForm.Meta):
        model = Cd
        fields = MediaForm.Meta.fields + ['artiste']

class DvdForm(MediaForm):
    class Meta(MediaForm.Meta):
        model = Dvd
        fields = MediaForm.Meta.fields + ['realisateur']

class EmprunteurForm(forms.ModelForm):
    class Meta:
        model = Emprunteur
        fields = ['nom', 'prenom']

    def clean(self):
        cleaned_data = super().clean()
        emprunteur = self.instance
        
        if emprunteur.pk:
            if not emprunteur.peut_emprunter():
                raise forms.ValidationError('Cet emprunteur a déjà 3 emprunts en cours.')
        
        return cleaned_data
    
class JeuDePlateauForm(forms.ModelForm):
    class Meta:
        model = JeuDePlateau
        fields = ['nom', 'fabricant', 'description']