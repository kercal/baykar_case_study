from django.contrib import admin
from .models import Annonce, Profile, Bild, Kategorie

admin.site.register(Annonce)
admin.site.register(Profile)
admin.site.register(Bild)
admin.site.register(Kategorie)
