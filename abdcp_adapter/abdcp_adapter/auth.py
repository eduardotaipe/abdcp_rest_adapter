# -*- coding: utf-8 -*-

from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.models import Group
from abdcp_adapter import constants


def user_in_abdcp_group(user):

    ABDCP_GROUP_NAME = getattr(
        settings,
        'ABDCP_GROUP_NAME',
        constants.ABDCP_GROUP_NAME
    )

    try:
        group = Group.objects.get(name=ABDCP_GROUP_NAME)
    except Group.DoesNotExist:
        return False

    users_in_group = group.user_set.all()
    return user in users_in_group


def abdcp_check_credentials(username, password):
    user = authenticate(username=username, password=password)
    if user is None:
        return False
    else:
        return user.is_active and user_in_abdcp_group(user)
