from django.http import Http404, HttpResponse
from django.views.generic import ListView, CreateView, DeleteView, View
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.models import User
from django.db.models import Count, Sum

import json

from .models import Choice, Song
from .forms import ChoiceForm, AddSongForm, ChoiceDeleteForm

from django.core import serializers

class AJAXListMixin(object):

     def dispatch(self, request, *args, **kwargs):
         if not request.is_ajax():
             raise Http404("This is an ajax view, friend.")
         return super(AJAXListMixin, self).dispatch(request, *args, **kwargs)

     def get_queryset(self):
         return (
            super(AJAXListMixin, self)
            .get_queryset()
            .filter(ajaxy_param=self.request.GET.get('some_ajaxy_param'))
         )

     def get(self, request, *args, **kwargs):
         return HttpResponse(serializers.serialize('json', self.get_queryset()))


class AjaxSongListView(AJAXListMixin, ListView):
    model = Song

    def get_queryset(self):
        songs = Song.objects.all().annotate(count=Count('choice'))
#        items = [(song.pk, song.name, song.artist, song.last_url, song.choice_set.count())]
#        for song in songs:
#            song.fields['count'] = song.choice_set.count()
        return songs #list(songs.values())

    def get(self, request, *args, **kwargs):
        return HttpResponse(serializers.serialize('json', self.get_queryset(),\
             use_natural_keys=True

             ))

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

    def get_queryset(self):
        return Choice.objects.filter(user=self.request.user).order_by("-index")


class AddSongView(CreateView):
    model = Song
    form_class = AddSongForm
    success_url = reverse_lazy('choices')

    def get_form_kwargs(self):
        kwargs = super(AddSongView, self).get_form_kwargs()
        kwargs.update({'requestuser': self.request.user})
        return kwargs

    def form_valid(self, form):
        if not form.cleaned_data['pk']:
            self.object = form.save()
        else:
            self.object = Song.objects.get(id=form.cleaned_data['pk'])
        user = self.request.user
        song = self.object
        previous_index = Choice.objects.filter(user=self.request.user).\
                order_by('-index').last()
        index = 10
        if previous_index:
            index = previous_index.index-1
        if index > 0:
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
#    form_class = ChoiceDeleteForm
    success_url ='/choices'

    def get_object(self, queryset=None):
        """ Hook to ensure object is owned by request.user. """
        obj = super(RemoveChoiceView, self).get_object()
        if not obj.user == self.request.user:
            raise Http404
        return obj

class VoteListView(ListView):
    model = Choice

    def get_queryset(self):
        return Choice.objects.all().\
                values('song__lasturl', 'song__name', 'song__artist').\
                annotate(dcount=Count('song'),votes=Sum('index')).\
                order_by('-votes')
