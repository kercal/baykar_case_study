from django.db.models import Q
from django.utils.timezone import datetime
from django.contrib.auth import get_user_model

def active(qs,user):
    if user.is_authenticated:
        a = qs.filter(available_until__gte=datetime.today().date()).filter(~Q(author__in=blocked_from(user)))
    else:
        a = qs.filter(available_until__gte = datetime.today().date())
    return a

def expired(qs):
    a = qs.filter(available_until__lt = datetime.today().date())
    return a

def pending(qs):
    a = qs.filter(reserviert = 1)
    return a

def blocked_from(username):
    a = get_user_model().objects.get(username=username).blocked.all()
    return a