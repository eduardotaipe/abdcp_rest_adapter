# -*- coding: utf-8 -*-
import logging

from suds.client import Client

from django.core.management.base import BaseCommand
from django.conf import settings

from abdcp_messages.models import ABDCPMessage
from abdcp_processes import ABDCPProcessor


class Command(BaseCommand):
    def get_pending_delivery(self):
        return ABDCPMessage.objects.pending_delivery()

    def handle(self, *args, **options):
        logging.info("=== Begin ABDCP message process ===")
        messages = self.get_pending_delivery()
        url = settings.ABDCP_ENDPOINT
        
        for message in messages:
            try:
                logging.info("Message %s has been processed", message.message_id)
                message.mark_delivered()
            except Exception, e:
                logging.info("Error: processing message "
                    + message.message_id )
        logging.info("=== End ABDCP message process ===")
