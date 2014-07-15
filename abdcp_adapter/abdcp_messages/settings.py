# -*- coding: utf-8 -*-

import os

from django.conf import settings
from abdcp_messages import constants

ABDCP_MESSAGE_XSD_FILENAME = getattr(
    settings,
    'ABDCP_MESSAGE_XSD_FILENAME',
    constants.ABDCP_MESSAGE_XSD_FILENAME
)

ABDCP_MESSAGE_XSD_DIR = getattr(
    settings,
    'ABDCP_MESSAGE_XSD_FILENAME',
    constants.ABDCP_MESSAGE_XSD_DIRPATH % {'DATA_DIR': settings.DATA_DIR}
)

ABDCP_MESSAGE_XSD_FILEPATH = getattr(
    settings,
    'ABDCP_MESSAGE_XSD_FILEPATH',
    os.path.join(
        ABDCP_MESSAGE_XSD_DIR, 
        ABDCP_MESSAGE_XSD_FILENAME
    )
)
