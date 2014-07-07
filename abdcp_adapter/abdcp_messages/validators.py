# -*- coding: utf-8 -*-

import re
from django.core.exceptions import ValidationError
from abdcp_messages import strings

def validate_message_id(value):
    if not bool(re.match(r'^[0-9]{17}$', value)):
        raise ValidationError(
            strings.MESSAGE_ID_VALIDATION_ERROR % {'message_id': value}
        )


def validate_transaction_id(value):
    if not bool(re.match(r'^[0-9]{17}$', value)):
        raise ValidationError(
            strings.TRANSACTION_ID_VALIDATION_ERROR % {'transaction_id': value}
        )


def validate_sender_code(value):
    if not bool(re.match(r'^[0-9]{2}$', value)):
        raise ValidationError(
            strings.SENDER_CODE_VALIDATION_ERROR % {'code': value}
        )


def validate_recipient_code(value):
    if not bool(re.match(r'^[0-9]{2}$', value)):
        raise ValidationError(
            strings.RECIPIENT_CODE_VALIDATION_ERROR % {'code': value}
        )


def validate_stated_creation_date(value):
    if not bool(re.match(r'^[0-9]{14}$', value)):
        raise ValidationError(
            strings.STATED_CREATION_DATE_VALIDATION_ERROR % {'date': value}
        )
