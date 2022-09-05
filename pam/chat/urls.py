from django.urls import re_path, path

from . import views

app_name = "chat"
urlpatterns = [
    re_path(r"^inbox/$", views.InboxView.as_view(),
        name="inbox"),
    path('create/<str:username>/', views.createMessage, name="message_user_create" ),
    re_path(r"^thread/(?P<pk>\d+)/$", views.ThreadView.as_view(),
        name="thread_detail"),
    path('bestätigt/<str:author>/<str:user>/<str:annonce>', views.bestätigt, name="bestätigt"),
    path('abgelehnt/<str:author>/<str:user>/<str:annonce>', views.abgelehnt, name="abgelehnt"),
    path('offene_reservierungen', views.offene_reservierungen, name="offene_reservierungen")
]
