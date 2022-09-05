from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.db import models
from annoncen.models import Annonce, Bild
from annoncen.geo import getLocation
from annoncen.helper_functions import active
import folium
import base64

# Create your views here.

def makemap (request):
    return (rendermap(request, 49.424831, 7.742753))
    #gerade irgendwo bei Kurt-Schumacher-Straße, vielleicht eher Adresse des Users

def makemapwithstartpoint (request, id):
    requested_annonce = get_object_or_404(Annonce, id=id)
    requested_annonce_latitude = requested_annonce.latitude
    if requested_annonce_latitude != None:
        return (rendermap(request, requested_annonce_latitude, requested_annonce.longitude))
    else:
        return HttpResponse(request)

def rendermap (request, longitude, latitude):

    actualmap = folium.Map(location=[longitude, latitude], zoom_start=14)

    for annonce in active(Annonce.objects.all(), request.user).order_by('-date'):
        annonce_latitude = annonce.latitude
        #imagetooltip = ""
        
        if annonce_latitude != None:

            
            if annonce.bild_set.all():
                for image in annonce.bild_set.all():
                    if image.isCoverImage:
                        image_popup = '<img src="' + image.bild.url +'" height=175>'
           
                link_popup = '<a href="/annonce/' + str(annonce.id) + '" target="_blank">' + image_popup + '</a>'
            else:
                link_popup = '<a href="/annonce/' + str(annonce.id) + '" target="_blank"> Klick hier für mehr Info! </a>'
            
            titel_popup = '<h2>' + annonce.titel + '</h2>'
            annonce_popup = titel_popup + link_popup

            annonce_longitude = annonce.longitude

            folium.Marker(location=[annonce_latitude, annonce_longitude], popup=annonce_popup).add_to(actualmap)
        

    actualmap = actualmap._repr_html_()
    context = {
        "actualmap":actualmap,
    }

    return render(request, "maps/bigmap.html", context)