from django.conf.urls import patterns, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('webapp.views',  # Examples:
    url('check/(?P<check_id>\d+)/$','check'),
    url('check_dir_api/$','check_dir_api'),
    url('check_file_api/$','check_file_api'),
    url('purge_api/$','purge_api'),
    url('history/$','history'),
    url('history_api/$','history_api'),
)
