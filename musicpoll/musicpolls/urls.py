# -*- coding: utf-8 -*-
from django.conf.urls import *
from django.core.urlresolvers import reverse_lazy
from django.views.generic import TemplateView
from .views import ChoiceListView, VoteView


urlpatterns = patterns(
    '',

    url(r'^choices/$', ChoiceListView.as_view(),name='choices'),
    url(r'^vote/$', VoteView.as_view(),name='vote'),
    url(r'^search/$',TemplateView.as_view(template_name='musicpolls/search_form.html'), name='search'),
)
