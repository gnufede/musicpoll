from django.core import serializers
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.models import User
from django.db import connection
from django.db.models import Count, Sum, Max
from django.http import Http404, HttpResponse
from django.views.generic import ListView, CreateView, DeleteView, View


import json

from .models import Choice, Song
from .forms import ChoiceForm, AddSongForm, ChoiceDeleteForm


class MySongsJsonView(View):

    def get(self, *args, **kwargs):
        choices = Choice.objects.filter(user=self.request.user)
        songs = [choice.song for choice in choices]
        result = [ob.as_json(count=0) for ob in songs]
        return HttpResponse(json.dumps(result), mimetype="application/json" )


class SongsJsonView(View):

    def get(self, *args, **kwargs):
        songs = Song.objects.all().annotate(count=Count('choice'))
        result = [ob.as_json(ob.count) for ob in songs]
        return HttpResponse(json.dumps(result), mimetype="application/json" )


class ChoiceListView(ListView):
    model = Choice

    def get_queryset(self,):
        requested_user = User.objects.get(username=self.kwargs['username']) if\
            'username' in self.kwargs and self.request.user.is_superuser else\
            self.request.user
        return Choice.objects.filter(user=requested_user).order_by("-index")


class AddSongView(CreateView):
    model = Song
    form_class = AddSongForm
    success_url = reverse_lazy('choices')

    def get_form_kwargs(self):
        kwargs = super(AddSongView, self).get_form_kwargs()
        kwargs.update({'requestuser': self.request.user})
        return kwargs

    def form_valid(self, form):
        self.object = Song.objects.get(id=form.cleaned_data['pk']) if\
            form.cleaned_data['pk'] else form.save()
        user = self.request.user
        song = self.object
        previous_index = Choice.objects.filter(user=user).\
                order_by('-index').last()
        index = previous_index.index-1 if previous_index else 10
        if index > 0 or 'Litri' == user.username:
            new_choice = Choice(user=user, song=song, index=index)
            new_choice.save()
        return super(AddSongView, self).form_valid(form)


class VoteView(CreateView):
    model = Choice
    form_class = ChoiceForm
    success_url = reverse_lazy('choices')

    def get_initial(self):
        initial = super(CreateView, self).get_initial()
        initial['user'] = self.request.user
        return initial

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(VoteView, self).form_valid(form)


class RemoveChoiceView(DeleteView):
    model = Choice
    success_url ='/choices'

    def get_object(self, queryset=None):
        """ Hook to ensure object is owned by request.user. """
        obj = super(RemoveChoiceView, self).get_object()
        if not obj.user == self.request.user:
            raise Http404
        return obj


class VoteListView(ListView):
    model = Choice

    def get_context_data(self, **kwargs):
        context = super(VoteListView, self).get_context_data(**kwargs)
        context['maxvotes'] = Choice.objects.values('song').annotate(dcount=Count('user__id')).order_by('-dcount').values('dcount')[0]['dcount']
        return context

    def get_queryset(self):
        return Choice.objects.all().\
                values('song__photourl', 'song__lasturl',\
                         'song__name', 'song__artist').\
                annotate(dcount=Count('song')).\
                order_by('-dcount')
#                aggregate(Max('dcount'))

                #.
                #order_by('-votes')
