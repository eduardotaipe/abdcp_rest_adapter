# -*- coding: utf-8 -*-

from django.db import models
from abdcp_messages import strings
from abdcp_messages import constants
from operators.models import Operator

# ABDCP Messages

class ABDCPMessage(models.Model):

    message_id = models.CharField(
        verbose_name=strings.ABDCP_MESSAGE_MESSAGE_ID,
        max_length=constants.ABDCP_MESSAGE_ID_LENGTH,
        unique=True
    )

    sender = models.ForeignKey(Operator,
        verbose_name=strings.ABDCP_MESSAGE_SENDER,
        related_name='messages_as_sender'
    )

    recipient = models.ForeignKey(Operator,
        verbose_name=strings.ABDCP_MESSAGE_RECIPIENT,
        related_name='messages_as_recipient'
    )

    transaction_id = models.CharField(
        verbose_name=strings.ABDCP_MESSAGE_TRANSACTION_ID,
        max_length=constants.ABDCP_TRANSACTION_ID_LENGTH,
        unique=True
    )

    request_document = models.TextField(
        verbose_name=strings.ABDCP_MESSAGE_REQUEST_DOCUMENT,
        blank=True,
        null=True
    )

    response_document = models.TextField(
        verbose_name=strings.ABDCP_MESSAGE_RESPONSE_DOCUMENT,
        blank=True,
        null=True
    )
    
    process_type = models.TextField(
        verbose_name=strings.ABDCP_MESSAGE_PROCESS_TYPE,
        choices=constants.ABDCP_PROCESS_CHOICES,
        max_length=2,
        blank=True,
        null=True
    )

    message_type = models.TextField(
        verbose_name=strings.ABDCP_MESSAGE_MESSAGE_TYPE,
        choices=constants.ABDCP_MESSAGE_TYPE_CHOICES,
        max_length=16,
        blank=True,
        null=True
    )

    stated_creation = models.DateTimeField(
        verbose_name=strings.ABDCP_MESSAGE_STATED_CREATION,
        blank=True,
        null=True
    )

    created = models.DateTimeField(
        verbose_name=strings.ABDCP_MESSAGE_CREATED,
        auto_now_add=True
    )

    responded = models.DateTimeField(
        verbose_name=strings.ABDCP_MESSAGE_RESPONDED,
        null=True
    )

    updated = models.DateTimeField(
        verbose_name=strings.ABDCP_MESSAGE_UPDATED,
        auto_now=True
    )

    class Meta:
        verbose_name = strings.ABDCP_MESSAGE_MODEL_NAME
        verbose_name_plural = strings.ABDCP_MESSAGE_MODEL_NAME_PLURAL

    def __unicode__(self):
        return self.message_id

    @classmethod
    def is_duplicated(cls, message_id):
        return ABDCPMessage.objects.filter(message_id=message_id).exists()
