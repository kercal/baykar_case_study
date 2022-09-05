from django.urls import path
from . import views

app_name = "maps"
urlpatterns = [
    path("bigmap", views.makemap, name="bigmap"),
    path("bigmap/<int:id>/", views.makemapwithstartpoint, name='bigmapwithstartpoint')
]