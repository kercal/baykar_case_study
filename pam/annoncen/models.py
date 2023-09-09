from multiprocessing import AuthenticationError
from django.db import models
from django.conf import settings
from django.db.models import SET_NULL
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.forms import ValidationError
from django.utils.translation import gettext_lazy as _
from datetime import date as d
from dateutil.relativedelta import relativedelta
from django.utils.timezone import datetime


class Kategorie(models.Model):
    name=models.CharField(max_length=40)

    def __str__(self): 
        return (self.name)

    class Meta:
        verbose_name        = "Kategorie"
        verbose_name_plural = "Kategorien"

class Annonce(models.Model):
    
    # Author
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=None, null=True, related_name='author')
            
    #Titel der Annonce
    titel = models.CharField(max_length= 30)
    
    #Anschrift 
    straße = models.CharField(max_length=40, null=True, blank=True)
    hausnummer = models.PositiveIntegerField(null=True, blank=True)
    stadt = models.CharField(max_length=20,null=True, blank=True)
    postleitzahl = models.PositiveIntegerField(null=True, blank=True)
    adresszusatz = models.CharField(max_length=20, null=True, blank=True)


    #Kontaktmöglichkeit 
    kontakt = models.CharField(max_length=40)

    #Kategorie
    kategorie = models.ManyToManyField(Kategorie)
    
    #Objektbeschreibung
    beschreibung = models.TextField()

    #Datum der Erstellung
    date = models.DateTimeField(auto_now_add=True)

    #Persönliche Nachricht des Erstellers
    nachricht = models.TextField(null=True, blank=True)

    #0 für eine Angebots-Annonce, 1 für eine Nachfrage-Annonce
    typ = models.BooleanField(null=True, default=0)

    #0 für frei, 1 für reserviert, 2 für möchte reservieren
    reserviert = models.IntegerField(default=0, blank=True)
    # User, der reservieren möchte/reserviert hat
    reserviert_von = models.ManyToManyField(settings.AUTH_USER_MODEL, default=None, blank=True , related_name='reservierer')

    # möchte merken
    gemerkt= models.IntegerField(default=0, blank=True)

    # User, der merken möchte
    gemerkt_von = models.ManyToManyField(settings.AUTH_USER_MODEL, default=None, blank=True , related_name='merker')

    #Maße des Objekts
    width = models.PositiveIntegerField(null=True, blank=True)
    length = models.PositiveIntegerField(null=True, blank=True)
    height = models.PositiveIntegerField(null=True, blank=True)

    # Tag, bis zu dem die Annonce verfügbar sein soll
    available_until = models.DateField(default=d.today()+relativedelta(months=+3))

    # Koordinaten der Adresse
    latitude = models.FloatField(default=None, null=True, blank=True)
    longitude = models.FloatField(default=None, null=True, blank=True)

    class Meta: 
        verbose_name        = "Annonce"
        verbose_name_plural = "Annoncen"

    def __str__(self): 
        return (self.titel)

    # gibt alle Gesuche aus
    @classmethod
    def get_gesuche(cls):
        return cls.objects.filter(typ = True)

    # gibt alle Angebote aus
    @classmethod
    def get_angebote(cls):
        return cls.objects.filter(typ = False)

    def clean(self):
        super().clean()
        # stelle sicher, dass nur alle Maße oder keines eingegeben wurde
        n = 0
        for field in [self.width, self.height, self.length]:
            if field: 
                n = n + 1
        if n != 0 and n != 3:
            raise ValidationError({'height': _("Bitte gebe alle drei Maße oder keine Maße an."),
                                    'width': _("Bitte gebe alle drei Maße oder keine Maße an."),
                                    'length': _("Bitte gebe alle drei Maße oder keine Maße an."),})

        # verfügbar bis Datum darf nicht in der Vergangenheit liegen
        if self.available_until != None:
            if self.available_until < datetime.today().date():
                raise ValidationError({'available_until': _("Datum muss in der Zukunft liegen."),})
        

class Bild(models.Model):

    #Bild zu den Annoncen
    bild = models.ImageField(upload_to='annoncen')

    #Cover-Bild
    isCoverImage = models.BooleanField(default= False)

    #ForeignKey für die zuordnung zur jeweiligen Annonce
    annonce = models.ForeignKey(Annonce, on_delete=models.CASCADE)
    
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null = True, default=None)
    bio = models.TextField(max_length=500, null=True, blank=True)
    enableChat = models.BooleanField(default=True)
    searchRadius = models.PositiveIntegerField(default=20)
    profilbild = models.ImageField(upload_to='profilbilder', null=True, blank=True)

    vorname = models.CharField(max_length=40, null=True, blank=True)
    nachname = models.CharField(max_length=40, null=True, blank=True)
    straße = models.CharField(max_length=40, null=True, blank=True)
    hausnummer = models.PositiveIntegerField(null=True, blank=True)
    stadt = models.CharField(max_length=20,null=True, blank=True)
    postleitzahl = models.PositiveIntegerField(null=True, blank=True)
    adresszusatz = models.CharField(max_length=20, null=True, blank=True)

    class Meta: 
        verbose_name        = "Profil"
        verbose_name_plural = "Profile"

    def __str__(self): 
        return ('Profil von ' + self.user.username)

    def address_is_set(self):
        if self.straße or self.hausnummer or self.stadt or self.postleitzahl:
            return True
        return False

# Es wird automatisch ein Profil erstellt, wenn ein neuer Nutzer registriert wird
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
