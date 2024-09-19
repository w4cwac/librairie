from django.test import TestCase
from django.urls import reverse
from .models import Media, Emprunteur
from datetime import date, timedelta

class MediaTestCase(TestCase):

    def setUp(self):
        self.emprunteur = Emprunteur.objects.create(nom="Dupont", prenom="Jean")
        self.media = Media.objects.create(name="Harry Potter", disponible=True)

    def test_creation_media(self):
        self.assertEqual(Media.objects.count(), 1)
        self.assertEqual(self.media.name, "Harry Potter")
    
    def test_emprunt_media(self):
        url = reverse('emprunter_media', kwargs={'media_id': self.media.id})
        response = self.client.post(url, {'emprunteur_id': self.emprunteur.id})
        self.assertEqual(response.status_code, 302)
        media = Media.objects.get(id=self.media.id)
        self.assertFalse(media.disponible)
        self.assertEqual(media.emprunteur, self.emprunteur)
    
    def test_rendu_media(self):
        self.media.emprunteur = self.emprunteur
        self.media.disponible = False
        self.media.save()
        url = reverse('rendre_media', kwargs={'emprunteur_id': self.emprunteur.id, 'media_id': self.media.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        media = Media.objects.get(id=self.media.id)
        self.assertTrue(media.disponible)
        self.assertIsNone(media.emprunteur)

    def test_limite_emprunt(self):
        Media.objects.create(name="Livre1", disponible=True)
        Media.objects.create(name="Livre2", disponible=True)
        Media.objects.create(name="Livre3", disponible=True)
        Media.objects.create(name="Livre4", disponible=True, date_emprunt=date.today() - timedelta(days=8))
        url = reverse('emprunter_media', kwargs={'media_id': 4})
        response = self.client.post(url, {'emprunteur_id': self.emprunteur.id})
        self.assertEqual(response.status_code, 302)
        media = Media.objects.get(id=4)
        self.assertTrue(media.disponible, "Le média devrait être disponible après avoir dépassé la limite d'emprunt.")
        self.assertIsNone(media.emprunteur)