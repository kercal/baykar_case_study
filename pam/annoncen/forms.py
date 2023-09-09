from django import forms
from .models import Annonce, Profile, Kategorie
from django.core.validators import MinValueValidator
from django.utils.timezone import datetime
from django.utils.translation import gettext_lazy as _

# cats = Kategorie.objects.all().values_list('name', 'name',) 
cats_list = [
    ('Multi-rotor', 'Multi-rotor'),
    ('Fixed-wing', 'Fixed-wing'),
    ('Single-rotor', 'Single-rotor'),
    ('VTOL', 'VTOL')
    ]

CHOICES = [
    ('biete', 'Ich biete'),
    ('suche', 'Ich suche'),
]

class AnnonceForm(forms.ModelForm):
    titel = forms.CharField(label = 'Title:')
    straße = forms.CharField(label = 'Street:', required = False,)
    hausnummer = forms.IntegerField(label = 'House Number:', required = False, 
                                    validators=[MinValueValidator(1)])
    stadt = forms.CharField(label = 'City:', required = False)
    postleitzahl = forms.IntegerField(label = 'Zip Code:', required = False, 
                                        validators=[MinValueValidator(1)])
    adresszusatz = forms.CharField(label='Additional Address Information:', required=False)

    nachricht = forms.CharField(label = '', required = False, widget = forms.Textarea,)
    beschreibung = forms.CharField(label = 'Desription:', widget = forms.Textarea,)
    kontakt = forms.CharField(label = 'Contact (Email or Phone Number):')
    typ = forms.ChoiceField(label = 'Type of Post:', required = False, choices=CHOICES)
    kategorie = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple(),
                                        label ='', choices=cats_list, required=False)
    bild_1 = forms.ImageField(label = 'Main Photo:', required = False)
    bild_2 = forms.ImageField(label = 'Add upto 2 more photos:', required = False)
    bild_3 = forms.ImageField(label = '', required = False)

    width = forms.IntegerField(label= "Width (in cm):", required=False, validators=[MinValueValidator(0)])
    height = forms.IntegerField(label= "Height (in cm):", required=False, validators=[MinValueValidator(0)])
    length = forms.IntegerField(label= "Length (in cm):", required=False, validators=[MinValueValidator(0)])
    weight = forms.IntegerField(label= "Weight (in kg):", required=False, validators=[MinValueValidator(0)])

    available_until = forms.DateField(label='Until when is the rental available? :', required=False,
                                        widget=forms.DateInput(attrs={'class':'form-control', 'type':'date'}))

    class Meta:
        model = Annonce
        fields = "__all__"
        exclude = ('author', 'name', 'typ', 'bild_1', 'bild_2', 'bild_3', 'location',)

form = AnnonceForm()

class ProfileForm(forms.ModelForm):
    bio = forms.CharField(label = 'Bio (write something about yourself):', required = False, 
                                widget = forms.Textarea)
    enableChat = forms.BooleanField(label='Chat aktivieren?',
                                required = False, help_text='Soll man dir Nachrichten schicken können?',)
    bild_1 = forms.ImageField(label='Profile Picture:', required=False)
    straße = forms.CharField(label = 'Street:', required = False)
    hausnummer = forms.IntegerField(label = 'Hausnummer:', required = False, 
                                    validators=[MinValueValidator(1)])
    vorname = forms.CharField(label='Name:', required=False)
    nachname = forms.CharField(label='Surname:', required=False)
    stadt = forms.CharField(label = 'City:', required = False)
    postleitzahl = forms.IntegerField(label = 'Zip Code:', required = False, 
                                        validators=[MinValueValidator(1)])
    adresszusatz = forms.CharField(label='Additional Adress:', required=False)
    searchRadius = forms.IntegerField(label='Lege einen Suchradius für vorgeschlagene Annoncen in der Nähe fest (in km):')

    class Meta:
        model = Profile
        fields = "__all__"
        exclude = ('user',)
        
class ExtendForm(forms.Form):
    available_until = forms.DateField(label='Until when is the rental available?:',
                                        widget=forms.DateInput(attrs={'class':'form-control', 'type':'date'}))

    def clean(self):
        au = self.cleaned_data.get('available_until')
        if au <= datetime.today().date():
            raise forms.ValidationError({'available_until': _("The date must be in the future."),})
        return au