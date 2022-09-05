from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

app_name = 'annoncen'
urlpatterns = [
    path('', views.home, name='home'),
    path('createannonce/', views.createannonce, name='createannonce'),
    path('annonce/<int:id>/', views.annonce, name='annonce'),
    path('edit/<int:id>/', views.edit, name='edit'),
    path('delete/<int:id>/', views.delete, name='delete'),
    path('delete_u/<int:pk>/', views.delete_u, name="delete_u"),
    path('profile/<str:username>', views.profile, name='profile'),
    path('profile/<str:username>/settings', views.profile_settings, name='profile_settings'),
    path('searchresult', views.searchresult, name='search_result'),
    path('reservierungsliste/<str:username>', views.reservierungsliste, name='reservierungsliste'),
    path('action_successfull/', views.action_successfull, name='action_successfull'),
    path('annonce/angebote', views.angebote, name='angebote'),
    path('annonce/gesuche',views.gesuche, name='gesuche'),
    path('annonce/sortbydate',views.sortbydate, name='sortbydate'),
    path('annonce/a_sortbydate',views.a_sortbydate, name='a_sortbydate'),
    path('annonce/g_sortbydate',views.g_sortbydate, name='g_sortbydate'),
    path('annonce/sortbyavailold',views.sortbyavailold, name='sortbyavailold'),
    path('annonce/a_sortbyavailold',views.a_sortbyavailold, name='a_sortbyavailold'),
    path('annonce/g_sortbyavailold',views.g_sortbyavailold, name='g_sortbyavailold'),
    path('annonce/sortbytitle',views.sortbytitle, name='sortbytitle'),
    path('annonce/a_sortbytitle',views.a_sortbytitle, name='a_sortbytitle'),
    path('annonce/g_sortbytitle',views.g_sortbytitle, name='g_sortbytitle'),
    path('annonce/sortbytitlereverse',views.sortbytitlereverse, name='sortbytitlereverse'),
    path('annonce/a_sortbytitlereverse',views.a_sortbytitlereverse, name='a_sortbytitlereverse'),
    path('annonce/g_sortbytitlereverse',views.g_sortbytitlereverse, name='g_sortbytitlereverse'),
    path('kategorie/<str:cats>/', views.kategorie, name='category'),
    path('profile/<str:username>/angebote', views.profile_angebote, name='profile_angebote'),
    path('profile/<str:username>/gesuche', views.profile_gesuche, name='profile_gesuche'),
    path('extend/<int:id>', views.extend, name="extend"),
    path('block/<int:id>', views.block, name="block"),
    path('reservieren/<int:user_id>/<int:annoncen_id>/<int:todo>/', views.reservieren, name='reservieren'),
    path('merken/<int:user_id>/<int:annoncen_id>/<int:todo>/', views.merken, name='merken'),
    path('profile/merkliste/<str:username>', views.merkliste, name='merkliste'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
