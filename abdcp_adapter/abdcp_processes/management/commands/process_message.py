# -*- coding: utf-8 -*-
import logging

from django.core.management.base import BaseCommand
from django.conf import settings

from abdcp_messages.models import ABDCPMessage
from abdcp_processes import ABDCPProcessor
from abdcp_processes.cp import ECPC_ABDCPProcessor
from abdcp_processes.sp import ESC_ABDCPProcessor


class Command(BaseCommand):
    def get_pending_messages(self):
        return ABDCPMessage.objects.pending_response()

    def get_processor(self,message):
        return ABDCPProcessor.processor_factory(message)

    def handle(self, *args, **options):
        logging.info("=== Begin ABDCP message process ===")
        messages = self.get_pending_messages()
        
        for message in messages:
            try:
                processor = self.get_processor(message)
                processor.process()
                logging.info("Message %s has been processed", message.message_id)
            except Exception, e:
                logging.info("Error: processing message %s %s" % (message.message_id,e))
        logging.info("=== End ABDCP message process ===")
