# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url
from abdcp_messages.api import resources

urlpatterns = patterns('',
    url(
        r'^create_message$',
        resources.ABDCPMessageCreation.as_view(),
        name='restful_message_creation_endpoint'
    )
)
