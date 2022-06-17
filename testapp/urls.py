from django.urls import re_path
from .views import create_topic, subscription, publish_event, listener


urlpatterns = [
    re_path(r'^create/topic/$', create_topic),
    re_path(r'^subscribe/(?P<topic>[\w-]+)/$', subscription),
    re_path(r'^publish/(?P<params>[\w-]+)/$', publish_event),
    re_path(r'^event$', listener)
]
