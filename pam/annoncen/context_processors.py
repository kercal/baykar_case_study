from .models import Kategorie, Annonce
from .helper_functions import expired, pending

def getData(request):
    c = {}
    c["kategorien"] = Kategorie.objects.all()
    if request.user.is_authenticated:
        c["expired"] = expired(Annonce.objects.all().filter(author=request.user))
        c["pending"] = pending(Annonce.objects.all().filter(author=request.user))
    return c