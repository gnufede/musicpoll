from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView, CreateView
from .models import Choice
from django.core.urlresolvers import reverse_lazy

# Create your views here.
class ChoiceListView(ListView):
    model = Choice

    def head(self, *args, **kwargs):
        last_choice = self.get_queryset().latest('date')
        response = HttpResponse('')
        # RFC 1123 date format
        response['Last-Modified'] = last_book.publication_date.strftime('%a, %d %b %Y %H:%M:%S GMT')
        return response


class VoteView(CreateView):
    model = Choice
    fields = ['song', 'index', 'user']
    success_url = reverse_lazy('choices')
