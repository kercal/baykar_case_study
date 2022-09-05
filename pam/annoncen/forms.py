from django import forms
from .models import Annonce, Profile, Kategorie
from django.core.validators import MinValueValidator
from django.utils.timezone import datetime
from django.utils.translation import gettext_lazy as _

# cats = Kategorie.objects.all().values_list('name', 'name',) 
cats_list = [
    ('Wohnen', 'Wohnen'),
    ('Musik', 'Musik'),
    ('Kleidung', 'Kleidung'),
    ('Tiere', 'Tiere'),
    ('Elektronik', 'Elektronik')
    ]

CHOICES = [
    ('biete', 'Ich biete'),
    ('suche', 'Ich suche'),
]

class AnnonceForm(forms.ModelForm):
    titel = forms.CharField(label = 'Titel:')
    straße = forms.CharField(label = 'Straße (optional):', required = False,)
    hausnummer = forms.IntegerField(label = 'Hausnummer (optional):', required = False, 
                                    validators=[MinValueValidator(1)])
    stadt = forms.CharField(label = 'Stadt (optional)', required = False)
    postleitzahl = forms.IntegerField(label = 'Postleitzahl (optional):', required = False, 
                                        validators=[MinValueValidator(1)])
    adresszusatz = forms.CharField(label='Adresszusatz (optional);', required=False)

    nachricht = forms.CharField(label = '', required = False, widget = forms.Textarea,)
    beschreibung = forms.CharField(label = 'Beschreibung:', widget = forms.Textarea,)
    kontakt = forms.CharField(label = 'Kontaktmöglichkeit (Email oder Telefonnummer):')
    typ = forms.ChoiceField(label = 'Art der Annonce:', choices=CHOICES)
    kategorie = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple(),
                                        label ='', choices=cats_list, required=False)
    bild_1 = forms.ImageField(label = 'Hauptbild zur Anzeige:', required = False)
    bild_2 = forms.ImageField(label = 'Lade bis zu zwei weitere Bilder hoch:', required = False)
    bild_3 = forms.ImageField(label = '', required = False)

    width = forms.IntegerField(label= "Breite (in cm):", required=False, validators=[MinValueValidator(0)])
    height = forms.IntegerField(label= "Höhe (in cm):", required=False, validators=[MinValueValidator(0)])
    length = forms.IntegerField(label= "Länge (in cm):", required=False, validators=[MinValueValidator(0)])

    available_until = forms.DateField(label='Bis wann soll die Annonce angezeigt werden?:', required=False,
                                        widget=forms.DateInput(attrs={'class':'form-control', 'type':'date'}))

    class Meta:
        model = Annonce
        fields = "__all__"
        exclude = ('author', 'name', 'typ', 'bild_1', 'bild_2', 'bild_3', 'location',)

form = AnnonceForm()

class ProfileForm(forms.ModelForm):
    bio = forms.CharField(label = 'Bio (schreibe etwas über dich):', required = False, 
                                widget = forms.Textarea)
    enableChat = forms.BooleanField(label='Chat aktivieren?',
                                required = False, help_text='Soll man dir Nachrichten schicken können?',)
    bild_1 = forms.ImageField(label='Profilbild:', required=False)
    straße = forms.CharField(label = 'Straße:', required = False)
    hausnummer = forms.IntegerField(label = 'Hausnummer:', required = False, 
                                    validators=[MinValueValidator(1)])
    vorname = forms.CharField(label='Vorname:', required=False)
    nachname = forms.CharField(label='Nachname:', required=False)
    stadt = forms.CharField(label = 'Stadt:', required = False)
    postleitzahl = forms.IntegerField(label = 'Postleitzahl:', required = False, 
                                        validators=[MinValueValidator(1)])
    adresszusatz = forms.CharField(label='Adresszusatz (optional);', required=False)
    searchRadius = forms.IntegerField(label='Lege einen Suchradius für vorgeschlagene Annoncen in der Nähe fest (in km):')

    class Meta:
        model = Profile
        fields = "__all__"
        exclude = ('user',)
        
class ExtendForm(forms.Form):
    available_until = forms.DateField(label='Bis wann soll die Annonce angezeigt werden?:',
                                        widget=forms.DateInput(attrs={'class':'form-control', 'type':'date'}))

    def clean(self):
        au = self.cleaned_data.get('available_until')
        if au <= datetime.today().date():
            raise forms.ValidationError({'available_until': _("Datum muss in der Zukunft liegen."),})
        return au