# -*- coding: utf-8 -*-
from django.conf.urls import *
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy
from django.views.generic import TemplateView
from .views import ChoiceListView, VoteView, VoteListView, AddSongView,\
                    SongsJsonView, MySongsJsonView,\
                    RemoveChoiceView


urlpatterns = patterns(
    '',
    url(r'^votes/$',
        VoteListView.as_view(template_name='musicpolls/vote_list.html'),
        name='votes'),
    url(r'^choices/$',
        login_required(ChoiceListView.as_view()), name='choices'),
    url(r'^vote/$', login_required(AddSongView.as_view()), name='vote'),
    url(r'^search/$', login_required(AddSongView.as_view()), name='search'),
    url(r'^(?P<pk>\d+)/removechoice/$',
        login_required(RemoveChoiceView.as_view()), name='removechoice'),
    url(r'^songlistjson/$',
        login_required(SongsJsonView.as_view()), name='songlistjson'),
    url(r'^mysonglistjson/$',
        login_required(MySongsJsonView.as_view()), name='mysonglistjson'),
    url(r'^(?P<username>\w+)/choices/$',
        login_required(ChoiceListView.as_view()), name='userchoices'),
)
