from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'django_web.views.index'),
    url(r'^login/$', 'django_web.views.login'),
    url(r'^logout/$', 'django_web.views.logout'),
    url(r'^index/$', 'django_web.views.index'),
    url(r'webapp/', include('webapp.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
