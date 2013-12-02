from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView, CreateView
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.models import User
from django.db.models import Count

from .models import Choice
from .forms import ChoiceForm

# Create your views here.
class ChoiceListView(ListView):
    model = Choice

    def get_queryset(self):
        return Choice.objects.filter(user=self.request.user)


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
        return Choice.objects.all().values('song__lasturl', 'song__name', 'song__artist').\
                annotate(dcount=Count('song')).\
                order_by('dcount')

