from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.views.generic import (
    TemplateView,
    UpdateView,
)
from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from .forms import MessageReplyForm, NewMsgForm
from .models import Thread, Message, UserThread

try:
    from account.decorators import login_required
except:  # noqa
    from django.contrib.auth.decorators import login_required


class InboxView(TemplateView):
    """
    View inbox thread list.
    """
    template_name = "chat/inbox.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.kwargs.get("deleted", None):
            threads = Thread.ordered(Thread.deleted(self.request.user))
            folder = "deleted"
        else:
            threads = Thread.ordered(Thread.inbox(self.request.user))
            folder = "inbox"

        context.update({
            "folder": folder,
            "threads": threads,
            "threads_unread": Thread.ordered(Thread.unread(self.request.user))
        })
        return context


class ThreadView(UpdateView):
    """
    View a single Thread or POST a reply.
    """
    model = Thread
    form_class = MessageReplyForm
    context_object_name = "thread"
    template_name = "chat/thread_detail.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(userthread__user=self.request.user).distinct()
        return qs

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        thread = self.get_object()
        chatOpen = False
        blocked = False
        for user in thread.users.all():
            if user.profile.enableChat and user != self.request.user:
                chatOpen = True
                if user in self.request.user.blocked.all():
                    blocked = True
                break
        data['chatOpen'] = chatOpen
        data['blocked'] = blocked
        return data

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({
            "user": self.request.user,
            "thread": self.object
        })
        return kwargs

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        self.object.userthread_set.filter(user=request.user).update(unread=False)
        return response

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        users = self.object.users.all()
        for user in users:
            if user != request.user and not user.profile.enableChat:
                raise PermissionDenied
        return super().post(request, *args, **kwargs)

@login_required
def createMessage(request, username):
    to_user = get_object_or_404(get_user_model(), username=username)
    if to_user == request.user:
        raise PermissionDenied
    threads = Thread.objects.filter(users=to_user).filter(users=request.user)
    if threads:
        return HttpResponseRedirect(reverse('chat:thread_detail', args=(threads[0].pk,)))
    if not to_user.profile.enableChat:
        raise PermissionDenied
    if request.method == "POST":
        form = NewMsgForm(request.POST)
        if form.is_valid():
            from_user = request.user
            subject = form.cleaned_data['subject']
            content = form.cleaned_data['content']
            msg = Message.new_message(from_user, [to_user], subject, content)
            msg.save()
            thread = Thread.objects.get(messages__pk=msg.pk)
            return HttpResponseRedirect(reverse('chat:thread_detail', args=(thread.pk,)))
    else:
        form = NewMsgForm()
    return render(request, 'chat/message_create.html', {'form': form, 'to_user': to_user})


def bestätigt(request, author, user, annonce):
    if get_user_model().objects.filter(username='System').count() == 1:
        from_user = get_user_model().objects.get(username='System')
    else:
        #Das hier ist nicht clean...
        from_user = get_user_model()(username='System', password='dasjdjaspfjd')
        from_user.save()
    to_user = get_object_or_404(get_user_model(), username=user)
    subject = 'Reservierungen'
    content = 'Deine Reservierung für die Annonce '+annonce+' wurde bestätigt! Sie wird nun in deiner Reservierungsliste angezeigt.'
    threads = Thread.objects.filter(users=to_user).filter(users=from_user)
    if threads:
        msg = Message.new_reply(threads[0], from_user, content)
    else:
        msg = Message.new_message(from_user, [to_user], subject, content)
    return HttpResponseRedirect(reverse('chat:inbox'))

def abgelehnt(request, author, user, annonce):

    if get_user_model().objects.filter(username='System').count() == 1:
        from_user = get_user_model().objects.get(username='System')
    else:
        #Das hier ist nicht clean...
        from_user = get_user_model()(username='System', password='dasjdjaspfjd')
        from_user.save()
    to_user = get_object_or_404(get_user_model(), username=user)
    subject = 'Reservierungen'
    content = 'Die Reservierung für die Annonce '+annonce+' wurde abgelehnt.'
    threads = Thread.objects.filter(users=to_user).filter(users=from_user)
    if threads:
        msg = Message.new_reply(threads[0], from_user, content)
    else:
        msg = Message.new_message(from_user, [to_user], subject, content)
    return HttpResponseRedirect(reverse('chat:inbox'))

def offene_reservierungen(request):


    return render(request, "chat/offene_reservierungen.html", {})