from django import http
from django.shortcuts import render
from django.views.generic import ListView, CreateView
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.models import User
from django.db.models import Count, Sum

from .models import Choice, Song
from .forms import ChoiceForm, AddSongForm

from django.core import serializers

class AJAXListMixin(object):

     def dispatch(self, request, *args, **kwargs):
         if not request.is_ajax():
             raise http.Http404("This is an ajax view, friend.")
         return super(AJAXListMixin, self).dispatch(request, *args, **kwargs)

     def get_queryset(self):
         return (
            super(AJAXListMixin, self)
            .get_queryset()
            .filter(ajaxy_param=self.request.GET.get('some_ajaxy_param'))
         )

     def get(self, request, *args, **kwargs):
         return http.HttpResponse(serializers.serialize('json', self.get_queryset()))


class AjaxSongListView(AJAXListMixin, ListView):
    model = Song

    def get_queryset(self):
        return Song.objects.all()



class ChoiceListView(ListView):
    model = Choice

    def get_queryset(self):
        return Choice.objects.filter(user=self.request.user).order_by("-index")


class AddSongView(CreateView):
    model = Song
    form_class = AddSongForm
    success_url = reverse_lazy('vote')


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


class VoteListView(ListView):
    model = Choice

    def get_queryset(self):
        return Choice.objects.all().\
                values('song__lasturl', 'song__name', 'song__artist').\
                annotate(dcount=Count('song'),votes=Sum('index')).\
                order_by('-votes')
