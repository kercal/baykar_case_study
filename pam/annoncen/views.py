from django.contrib.auth import get_user_model

from django.http import HttpResponseRedirect

from django.shortcuts import render, redirect, get_object_or_404, reverse

from .models import Annonce, Bild, Kategorie, Profile

from .forms import AnnonceForm, ProfileForm, ExtendForm

from django.core.exceptions import PermissionDenied

from django.contrib.auth.decorators import login_required

from .geo import getLocation, getDistance
from .helper_functions import active, blocked_from
from datetime import date as d
from django.db.models.functions import Lower

from dateutil.relativedelta import relativedelta
import folium


def home(request):

    annoncen = active(Annonce.objects.exclude(reserviert=2), request.user).order_by('-date')
    title = 'Alle Annoncen'

    return render(request, 'annoncen/home.html', {'annoncen': annoncen, 'title': title})

def sortbydate(request):
    annoncen = active(Annonce.objects.exclude(reserviert=2), request.user).order_by('-date')
    title = "Alle Annoncen sortiert nach Datum:"

    return render(request, 'annoncen/home.html', {'annoncen': annoncen, 'title': title})

def a_sortbydate(request):
    annoncen = active(Annonce.get_angebote().exclude(reserviert=2), request.user).order_by('-date')
    title = "Alle Angebote sortiert nach Datum:"

    return render(request, 'annoncen/home.html', {'annoncen': annoncen, 'title': title})

def g_sortbydate(request):
    annoncen = active(Annonce.get_gesuche().exclude(reserviert=2), request.user).order_by('-date')
    title = "Alle Gesuche sortiert nach Datum:"

    return render(request, 'annoncen/home.html', {'annoncen': annoncen, 'title': title})

def sortbyavailold(request):
    annoncen = active(Annonce.objects.exclude(reserviert=2), request.user).order_by('available_until')
    title = "Alle Annoncen sortiert nach Ablaufdatum:"

    return render(request, 'annoncen/home.html', {'annoncen': annoncen, 'title': title})

def a_sortbyavailold(request):
    annoncen = active(Annonce.get_angebote().exclude(reserviert=2), request.user).order_by('available_until')
    title = "Alle Angebote sortiert nach Ablaufdatum:"

    return render(request, 'annoncen/home.html', {'annoncen': annoncen, 'title': title})

def g_sortbyavailold(request):
    annoncen = active(Annonce.get_gesuche().exclude(reserviert=2), request.user).order_by('available_until')
    title = "Alle Gesuche sortiert nach Ablaufdatum:"

    return render(request, 'annoncen/home.html', {'annoncen': annoncen, 'title': title})

def sortbytitle(request):
    
    annoncen = active(Annonce.objects.exclude(reserviert=2), request.user).order_by(Lower('titel'))
    title = "Alle Annoncen sortiert nach Titel A-Z:"

    return render(request, 'annoncen/home.html', {'annoncen': annoncen, 'title': title})

def a_sortbytitle(request):
    
    annoncen = active(Annonce.get_angebote().exclude(reserviert=2),request.user).order_by(Lower('titel'))
    title = "Alle Angebote sortiert nach Titel A-Z:"

    return render(request, 'annoncen/home.html', {'annoncen': annoncen, 'title': title})

def g_sortbytitle(request):
    
    annoncen = active(Annonce.get_gesuche().exclude(reserviert=2),request.user).order_by(Lower('titel'))
    title = "Alle Gesuche sortiert nach Titel A-Z:"

    return render(request, 'annoncen/home.html', {'annoncen': annoncen, 'title': title})

def sortbytitlereverse(request):
    
    annoncen = active(Annonce.objects.exclude(reserviert=2), request.user).order_by(Lower('titel').desc())
    title = "Alle Annoncen sortiert nach Titel Z-A:"

    return render(request, 'annoncen/home.html', {'annoncen': annoncen, 'title': title})

def a_sortbytitlereverse(request):
    
    annoncen = active(Annonce.get_angebote().exclude(reserviert=2),request.user).order_by(Lower('titel').desc())
    title = "Alle Angebote sortiert nach Titel Z-A:"

    return render(request, 'annoncen/home.html', {'annoncen': annoncen, 'title': title})

def g_sortbytitlereverse(request):
    
    annoncen = active(Annonce.get_gesuche().exclude(reserviert=2),request.user).order_by(Lower('titel').desc())
    title = "Alle Gesuche sortiert nach Titel Z-A:"

    return render(request, 'annoncen/home.html', {'annoncen': annoncen, 'title': title})

def gesuche(request):
    annoncen = active(Annonce.get_gesuche().exclude(reserviert=2),request.user).order_by('-date')
    title = "Alle Gesuche"

    return render(request, 'annoncen/home.html', {'annoncen': annoncen, 'title': title})


def angebote(request):
    annoncen = active(Annonce.get_angebote().exclude(reserviert=2),request.user).order_by('-date')
    title = "Alle Angebote"

    return render(request, 'annoncen/home.html', {'annoncen': annoncen, 'title': title})


@login_required

def createannonce(request):

    if request.method == "POST":

        form = AnnonceForm(request.POST)

        if form.is_valid():

            post = form.save(commit=False)

            if not form.cleaned_data['available_until']:

                post.available_until = d.today()+relativedelta(months=+3)

            else:
                
                available_until = min(form.cleaned_data['available_until'], d.today()+relativedelta(months=+3))

                post.available_until = available_until

            post.author = request.user

            if form.cleaned_data['typ'] == 'suche':

                post.typ = True

            elif form.cleaned_data['typ'] == 'biete':

                post.typ = False

            if request.POST.get('address') == 'default_address':

                # Nutze Adresse aus Profil

                post.straße = request.user.profile.straße

                post.hausnummer = request.user.profile.hausnummer

                post.stadt = request.user.profile.stadt

                post.postleitzahl = request.user.profile.postleitzahl


            # setze Koordinaten aus Adresse
            address = ''

            for item in [post.straße, post.hausnummer, post.postleitzahl, post.stadt]:

                if  item != None:

                    address = address + ' ' + str(item)

            location = getLocation(address)

            if location:
                post.latitude = location.latitude

                post.longitude = location.longitude

            post.save()


            # Verlinke die Annonce mit den eingegebenen Kategorien

            if form.cleaned_data['kategorie']:

                for kat in form.cleaned_data['kategorie']:

                    if Kategorie.objects.filter(name=kat).count()==1:

                        post.kategorie.add(Kategorie.objects.get(name=kat).pk)

                    else:

                        k=Kategorie(name=kat)

                        k.save()

                        post.kategorie.add(k.pk)


            annonce = Annonce.objects.get(pk = post.pk)
            

            # Speichere die Bilder und verlinke sie mit der Annonce

            if "bild_1" in request.FILES:

                bild_1= request.FILES['bild_1']

                b=Bild(bild=bild_1, annonce=annonce, isCoverImage=True)

                b.save()

            if "bild_2" in request.FILES:

                bild_2= request.FILES['bild_2']

                b=Bild(bild=bild_2, annonce=annonce)

                b.save()

            if "bild_3" in request.FILES:

                bild_3= request.FILES['bild_3']

                b=Bild(bild=bild_3, annonce=annonce)

                b.save()


            return HttpResponseRedirect(reverse('annoncen:action_successfull') + '?a=' + str(annonce.pk))

    else:

        form = AnnonceForm()

    address_is_set = Profile.address_is_set(request.user.profile)

    return render(request, 'annoncen/createannonce.html', {'form': form, 'address_is_set': address_is_set})



def annonce(request, id):

    def get_annonce_within_20km(requested_annonce, annonce_latitude, annonce_longitude):

                closestAnnoncen = []

                for annonce in active(Annonce.objects.all(),request.user).order_by('-date').values():

                    if annonce['id'] != requested_annonce.pk and annonce['latitude'] != None:

                        distance = getDistance((annonce_latitude, annonce_longitude), (annonce['latitude'], annonce['longitude']))

                        if request.user.is_authenticated:

                            if distance < request.user.profile.searchRadius:
                                closestAnnoncen.append(annonce)

                        else:

                            if distance < 20:
                                closestAnnoncen.append(annonce)

                return closestAnnoncen

    def get_map_with_surrounding_annoncen(annonce_latitude, annonce_longitude, annoncen_within_20km):

                annonce_titel = requested_annonce.titel

                actualmap = folium.Map(location=[annonce_latitude, annonce_longitude], zoom_start=14)

                folium.Marker(location=[annonce_latitude, annonce_longitude], popup=annonce_titel ,

                                icon=folium.Icon(color='red')).add_to(actualmap)


                for close_annonce in annoncen_within_20km:

                    close_annonce_latitude = close_annonce['latitude']

                    close_annonce_longitude = close_annonce['longitude']

                    close_annonce_titel = close_annonce['titel']

                    folium.Marker(location=[close_annonce_latitude, close_annonce_longitude], popup=close_annonce_titel).add_to(actualmap)

                actualmap = actualmap._repr_html_()

                return(actualmap)

    def get_annonceproperties_from_coordinates(requested_annonce):

        threeclosest = []

        actualmap = None

        if requested_annonce.latitude != None:

            annonce_latitude = requested_annonce.latitude

            annonce_longitude = requested_annonce.longitude

            annoncen_within_20km = get_annonce_within_20km(requested_annonce, annonce_latitude, annonce_longitude)

            threeclosest = annoncen_within_20km[:3]

            actualmap = get_map_with_surrounding_annoncen(annonce_latitude, annonce_longitude, annoncen_within_20km)

        return (threeclosest, actualmap)

    requested_annonce = get_object_or_404(Annonce, id=id)


    # erhalte vier neueste Annoncen mit mindestens einer gleichen Kategorie

    categories = requested_annonce.kategorie.all()

    same_category = Annonce.objects.none()

    for category in categories:

        a = active(Kategorie.objects.get(name=category.name).annonce_set.all().exclude(pk=id),request.user)

        same_category = same_category.union(a)

    same_category = same_category.order_by('-date')[:4:1]



    three_newest_annonce_with_same_author = active(Annonce.objects.filter(author=requested_annonce.author).exclude(pk=id), request.user).order_by('-date')[:3:1]

    #Holt die drei nähesten Annoncen der ausgewählten Annonce in 20 km und eine Karte mit der Annonce und die innerhalb von 20km.
    (closest, actualmap) = get_annonceproperties_from_coordinates(requested_annonce)



    #hat der request.user diese Annonce reserviert

    hat_reserviert = False

    if request.user in requested_annonce.reserviert_von.all():

        hat_reserviert = True


    context = { 'id': id,

                'annonce': requested_annonce,

                'same_category': same_category,

                'three_newest_annonce_with_same_author': three_newest_annonce_with_same_author,

                'closest': closest,

                'hat_reserviert': hat_reserviert,

                'actualmap':actualmap} 
    #hat der request.user diese Annonce gemerkt
    hat_gemerkt = False
    if request.user in requested_annonce.gemerkt_von.all():
        hat_gemerkt = True

    

    context = { 'id': id, 
                'annonce': requested_annonce,
                'same_category': same_category,
                'three_newest_annonce_with_same_author': three_newest_annonce_with_same_author,
                'closest': closest,
                'hat_reserviert': hat_reserviert,
                'actualmap':actualmap,
                'hat_gemerkt':hat_gemerkt}
    return render(request, 'annoncen/annonce.html', context)


def edit(request, id):

    edited_annonce = get_object_or_404(Annonce, id=id)

    if request.method == "POST":
        form = AnnonceForm(request.POST, request.FILES)

        if form.is_valid():
            #post = form.save(commit=False)
            post = edited_annonce

            if not form.cleaned_data['available_until']:

                post.available_until = d.today()+relativedelta(months=+3)

            else:
                
                available_until = min(form.cleaned_data['available_until'], d.today()+relativedelta(months=+3))

                post.available_until = available_until

            post.author = request.user

            if form.cleaned_data['typ'] == 'suche':

                post.typ = True

            elif form.cleaned_data['typ'] == 'biete':

                post.typ = False

            if form.cleaned_data['titel']:

                post.titel = form.cleaned_data['titel']

            if form.cleaned_data['straße']:

                post.straße = form.cleaned_data['straße']

            if form.cleaned_data['hausnummer']:

                post.hausnummer = form.cleaned_data['hausnummer']

            if form.cleaned_data['stadt']:

                post.stadt = form.cleaned_data['stadt']

            if form.cleaned_data['postleitzahl']:

                post.stadt = form.cleaned_data['postleitzahl']

            if form.cleaned_data['adresszusatz']:

                post.adresszusatz = form.cleaned_data['adresszusatz']

            if form.cleaned_data['kontakt']:

                post.kontakt = form.cleaned_data['kontakt']

            if form.cleaned_data['beschreibung']:

                post.beschreibung = form.cleaned_data['beschreibung']

            if form.cleaned_data['nachricht']:

                post.nachricht = form.cleaned_data['nachricht']

            if form.cleaned_data['width']:

                post.width = form.cleaned_data['width']

            if form.cleaned_data['height']:

                post.height = form.cleaned_data['height']

            if form.cleaned_data['length']:

                post.length = form.cleaned_data['length']


            # setze Koordinaten aus Adresse
            address = ''

            for item in [post.straße, post.hausnummer, post.postleitzahl, post.stadt]:

                if  item != None:

                    address = address + ' ' + str(item)

            location = getLocation(address)

            if location:
                post.latitude = location.latitude

                post.longitude = location.longitude

            post.save()


            # Verlinke die Annonce mit den eingegebenen Kategorien

            if form.cleaned_data['kategorie']:

                for kat in form.cleaned_data['kategorie']:

                    if Kategorie.objects.filter(name=kat).count()==1:

                        post.kategorie.add(Kategorie.objects.get(name=kat).pk)

                    else:

                        k=Kategorie(name=kat)

                        k.save()

                        post.kategorie.add(k.pk)


            annonce = Annonce.objects.get(pk = post.pk)
            

            # Speichere die Bilder und verlinke sie mit der Annonce

            if "bild_1" in request.FILES:

                #edited_annonce.bild_set.bild_1.delete()

                bild_1= request.FILES['bild_1']

                b=Bild(bild=bild_1, annonce=annonce, isCoverImage=True)

                b.save()

            if "bild_2" in request.FILES:

                bild_2= request.FILES['bild_2']

                b=Bild(bild=bild_2, annonce=annonce)

                b.save()

            if "bild_3" in request.FILES:

                bild_3= request.FILES['bild_3']

                b=Bild(bild=bild_3, annonce=annonce)

                b.save()


            return HttpResponseRedirect(reverse('annoncen:action_successfull') + '?a=' + str(annonce.pk))
    
        else:
            print(form.errors)
    else:

        form = AnnonceForm(initial={

                            'typ': edited_annonce.typ,

                            'titel': edited_annonce.titel,

                            'straße': edited_annonce.straße,

                            'hausnummer': edited_annonce.hausnummer,

                            'stadt': edited_annonce.stadt,

                            'postleitzahl': edited_annonce.postleitzahl,

                            'adresszusatz': edited_annonce.adresszusatz,

                            'kontakt': edited_annonce.kontakt,

                            'beschreibung': edited_annonce.beschreibung,

                            'nachricht': edited_annonce.nachricht,

                            'width': edited_annonce.width,

                            'height': edited_annonce.height,

                            'length': edited_annonce.length

                            })


        return render(request, 'annoncen/edit.html', {'form': form, 'annonce': edited_annonce})

def delete(request, id):

    an = get_object_or_404(Annonce, id=id)

    if request.user != an.author:

        raise PermissionDenied
    an.delete()

    return HttpResponseRedirect(reverse('annoncen:action_successfull') + '?delete=' + str(an.titel))


def delete_u(request, pk):

    user = get_object_or_404(get_user_model(), id=pk)

    if request.user != user:

        raise PermissionDenied

    if request.method == 'POST':
        user.delete()

        return HttpResponseRedirect(reverse('annoncen:action_successfull') + '?deleteUser=' + user.username)

    return render(request, 'annoncen/delete_u.html', {'name': user.username})



def profile(request, username):

    user = get_object_or_404(get_user_model(), username=username)
    profil = user.profile
    blocked = False
    blocked_by = False
    if request.user != user and request.user.is_authenticated:
        if blocked_from(user).filter(username=request.user).exists():
            blocked = True
        if blocked_from(request.user).filter(username=user).exists():
            blocked_by = True
    annoncen = active(Annonce.get_angebote().filter(author=user),request.user).order_by('-date')
    hat_annoncen = False
    if annoncen:
        hat_annoncen = True
    return render(request, 'annoncen/profile.html', {'profil': profil, 'annoncen':annoncen, 'user':user, 'blocked':blocked, 'blocked_by':blocked_by, 'hat_annoncen':hat_annoncen})


def block(request, id):
    user = get_object_or_404(get_user_model(), id=id)
    profil = user.profile
    blocked = False
    blocked_by = False
    if blocked_from(user).filter(username=request.user).exists():
        user.blocked.remove(request.user)
    else:
        user.blocked.add(request.user)
        blocked = True
    if blocked_from(request.user).filter(username=user).exists():
        blocked_by = True

    if request.user != user:

        annoncen = active(Annonce.get_angebote().filter(author=user, reserviert=0), request.user).order_by('-date')

    else:

        annoncen = active(Annonce.get_angebote().filter(author=user), request.user).order_by('-date')

    return render(request, 'annoncen/profile.html', {'profil': profil, 'annoncen':annoncen, 'user':user, 'blocked':blocked, 'blocked_by':blocked_by})


def profile_angebote(request, username):

    user = get_object_or_404(get_user_model(), username=username)
    profil = user.profile

    if request.user != user:
        annoncen = active(Annonce.get_angebote().filter(author=user, reserviert=0),request.user).order_by('-date')
    else:
        annoncen = active(Annonce.get_angebote().filter(author=user), request.user).order_by('-date')
    return render(request, 'annoncen/profile.html', {'profil': profil, 'annoncen':annoncen, 'user':user, 'hat_annoncen' : True})


def profile_gesuche(request, username):

    user = get_object_or_404(get_user_model(), username=username)
    profil = user.profile

    if request.user != user:
        annoncen = active(Annonce.get_gesuche().filter(author=user, reserviert=0),request.user).order_by('-date')
    else:
        annoncen = active(Annonce.get_gesuche().filter(author=user),request.user).order_by('-date')

    return render(request, 'annoncen/profile.html', {'profil': profil, 'annoncen':annoncen, 'user':user, 'hat_annoncen':True})


@login_required

def profile_settings(request, username):

    user = get_object_or_404(get_user_model(),username=username)

    if request.user != user:

        raise PermissionDenied
    profile = user.profile

    if request.method == "POST":

        form = ProfileForm(request.POST, request.FILES)

        if form.is_valid():

            profile.bio = form.cleaned_data['bio']

            profile.enableChat = form.cleaned_data['enableChat']

            profile.searchRadius = form.cleaned_data['searchRadius']


            # setze Felder auf None, wenn Einträge gelöscht werden

            if form.cleaned_data['straße'] == '':

                profile.straße = None

            else:

                profile.straße = form.cleaned_data['straße']

            if form.cleaned_data['stadt'] == '':

                profile.stadt = None

            else:

                profile.stadt = form.cleaned_data['stadt']

            if not form.cleaned_data['hausnummer']:

                profile.hausnummer = None

            else:

                profile.hausnummer = form.cleaned_data['hausnummer']

            if not form.cleaned_data['postleitzahl']:

                profile.postleitzahl = None

            else:

                profile.postleitzahl = form.cleaned_data['postleitzahl']

            if not form.cleaned_data['adresszusatz']:

                profile.adresszusatz = None

            else:

                profile.adresszusatz = form.cleaned_data['adresszusatz']

            if not form.cleaned_data['vorname']:

                profile.vorname = None

            else:

                profile.vorname = form.cleaned_data['vorname']

            if not form.cleaned_data['nachname']:

                profile.nachname = None

            else:

                profile.nachname = form.cleaned_data['nachname']

            if "bild_1" in request.FILES:

                profile.profilbild = request.FILES['bild_1']

            profile.save()

            return HttpResponseRedirect(reverse('annoncen:action_successfull') + '?profile=True')

    else:

        print(profile.searchRadius)

        form = ProfileForm(initial={

                            'bio': profile.bio,

                            'straße': profile.straße,

                            'hausnummer': profile.hausnummer,

                            'stadt': profile.stadt,

                            'postleitzahl': profile.postleitzahl,

                            'adresszusatz': profile.adresszusatz,

                            'searchRadius': profile.searchRadius,

                            'profilbild': profile.profilbild,

                            })

    return render(request, 'annoncen/profile_settings.html',

                    {'form': form, 'id': user.id, 'profile': profile})


def action_successfull(request):
    pk = request.GET.get('a', '')
    # created Annonce
    if pk:
        annonce = get_object_or_404(Annonce, pk = pk)
        annoncen = active(Annonce.objects.exclude(reserviert=2), request.user).order_by('-date')
        title = 'Alle Annoncen'
        return render(request, 'annoncen/home.html', {'annoncen': annoncen, 'title': title, 'createdAnnonce': annonce})

    profile = request.GET.get('profile', '')
    # changed profile settings
    if profile == 'True':
        user = request.user
        profil = user.profile
        annoncen = active(Annonce.get_angebote().filter(author=user), request.user).order_by('-date')
        return render(request, 'annoncen/profile.html', {'profil': profil, 'annoncen':annoncen, 'user':user, 'changedSettings': True, 'hat_annoncen': annoncen})

    logout = request.GET.get('logout', '')
    # user was logged out
    if logout == 'True':
        annoncen = active(Annonce.objects.exclude(reserviert=2), request.user).order_by('-date')
        title = 'Alle Annoncen'
        return render(request, 'annoncen/home.html', {'annoncen': annoncen, 'title': title, 'loggedOut': True})

    deletedName = request.GET.get('delete', '')
    if deletedName:
        annoncen = active(Annonce.objects.exclude(reserviert=2), request.user).order_by('-date')
        title = 'Alle Annoncen'
        return render(request, 'annoncen/home.html', {'annoncen': annoncen, 'title': title, 'deletedName': deletedName})

    deletedUser = request.GET.get('deleteUser', '')
    if deletedUser:
        annoncen = active(Annonce.objects.exclude(reserviert=2), request.user).order_by('-date')
        title = 'Alle Annoncen'
        return render(request, 'annoncen/home.html', {'annoncen': annoncen, 'title': title, 'deletedUser': deletedUser})


def searchresult(request):

    if request.method == "POST":

        searched = request.POST['searched']

        if searched != "":
            results = active(Annonce.objects.filter(titel__contains = searched), request.user).order_by('-date')
            return render(request, 'annoncen/searchresult.html', {'searched' : searched, 'results' : results})

        else:

            return HttpResponseRedirect(reverse('annoncen:home'))

    else:

        return render(request, 'annoncen/searchresult.html', {})
 

def kategorie(request, cats):

    kategorie = Kategorie.objects.get(name = cats)

    annoncen_kategorie = active(kategorie.annonce_set.all(), request.user)

    return render(request, 'annoncen/kategorie.html', {'cats':kategorie, 'annoncen_kategorie':annoncen_kategorie})


@login_required

def extend(request, id):

    annonce = get_object_or_404(Annonce, id = id)

    if request.user != annonce.author:

        raise PermissionDenied

    if request.method == "POST":

        form = ExtendForm(request.POST)

        if form.is_valid():

            extendedDate = request.POST['available_until']

            annonce.available_until = extendedDate

            annonce.save()

            return HttpResponseRedirect(reverse('annoncen:annonce', args=[annonce.id]))

    else:

        form = ExtendForm()

    datedifference = annonce.available_until - annonce.date.date()

    defaultextension = str(d.today() + datedifference)

    return render(request, 'annoncen/extend.html', {'form': form, 'annonce': annonce, 'defaultextension': defaultextension})


@login_required

def reservieren(request, user_id, annoncen_id, todo):

    annonce = get_object_or_404(Annonce, id=annoncen_id)

    user = get_object_or_404(get_user_model(), id=user_id)

    author = annonce.author

    #User möchte Annonce reservieren

    if int(todo) == 1:

        annonce.reserviert = 1

        annonce.reserviert_von.add(user)

        annonce.save()

    #User möchte seine Reservierung zurückziehen

    elif int(todo) == 0:

        annonce.reserviert_von.remove(user)

        if annonce.reserviert_von.count() == 0:

            annonce.reserviert = 0

        annonce.save()

    #Author bestätigt Reservierung

    elif int(todo) == 3:

        for u in annonce.reserviert_von.all():

            annonce.reserviert_von.remove(u)

        annonce.reserviert_von.add(user)

        annonce.reserviert = 2

        annonce.save()

        return HttpResponseRedirect(reverse('chat:bestätigt', args=(author.username, user.username, annonce.titel)))

    #Author zieht Reservierung zurück

    else:

        annonce.reserviert_von.remove(user)

        if annonce.reserviert_von.count() == 0:

            annonce.reserviert = 0

        annonce.save()

        return HttpResponseRedirect(reverse('chat:abgelehnt', args=(author.username, user.username, annonce.titel)))

    return HttpResponseRedirect(reverse('annoncen:annonce', args=(annonce.id,)))


@login_required

def reservierungsliste(request, username):

    user = get_object_or_404(get_user_model(), username=username)
    annoncen = active(Annonce.objects.filter(reserviert_von=user), request.user).order_by('-date')
    title = "Deine Reservierungen"
    return render(request, 'annoncen/home.html', {'annoncen': annoncen, 'title': title})

@login_required
def merken(request, user_id, annoncen_id, todo):
    annonce = get_object_or_404(Annonce, id=annoncen_id)
    user = get_object_or_404(get_user_model(), id=user_id)
    author = annonce.author
    #User möchte Annonce reservieren
    if int(todo) == 1:
        annonce.gemerkt = 1
        annonce.gemerkt_von.add(user)
        annonce.save()
    #User möchte seine Reservierung zurückziehen
    elif int(todo) == 0:
        annonce.gemerkt_von.remove(user)
        if annonce.gemerkt_von.count() == 0:
            annonce.gemerkt = 0
        annonce.save()
   
    return HttpResponseRedirect(request.META['HTTP_REFERER'])

@login_required
def merkliste(request, username):
    user = get_object_or_404(get_user_model(), username=username)
    annoncen = active(Annonce.objects.filter(gemerkt_von=user), request.user).order_by('-date')
    title = "Deine gespeicherten Annoncen"
    return render(request, 'annoncen/merkliste.html', {'annoncen': annoncen, 'title': title})

    
