from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name='base.html')),
    url(r'^info$', TemplateView.as_view(template_name='info.html')),
    url(r'^map$', TemplateView.as_view(template_name='map.html')),

    # Examples:
    # url(r'^$', 'musicpoll.views.home', name='home'),
    # url(r'^musicpoll/', include('musicpoll.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    (r'^', include('auth.urls')),
    (r'^', include('musicpolls.urls')),
)
