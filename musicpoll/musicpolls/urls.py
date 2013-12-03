# -*- coding: utf-8 -*-
from django.conf.urls import *
from django.core.urlresolvers import reverse_lazy
from django.views.generic import TemplateView
from .views import ChoiceListView, VoteView, VoteListView, AddSongView, AjaxSongListView


urlpatterns = patterns(
    '',
    url(r'^votes/$', VoteListView.as_view(template_name='musicpolls/vote_list.html'),name='votes'),
    url(r'^choices/$', ChoiceListView.as_view(),name='choices'),
    url(r'^vote/$', VoteView.as_view(),name='vote'),
    url(r'^search/$', AddSongView.as_view(),name='search'),
    url(r'^songlistjson/$', AjaxSongListView.as_view(),name='songlistjson'),
)
