# -*- coding: utf-8 -*-

import logging
from django.core.management.base import BaseCommand
from django.conf import settings

from abdcp_messages.models import ABDCPMessage
from abdcp_processes import ABDCPProcessor
from requests_portability.client import PortabilityClientError


class Command(BaseCommand):
    def get_pending_messages(self):
        return ABDCPMessage.objects.pending_response()

    def get_processor(self,message):
        return ABDCPProcessor.processor_factory(message)

    def handle(self, *args, **options):
        logging.info("=== Iniciando Proceso de mensajes ABDCP ===")
        messages = self.get_pending_messages()

        for message in messages:
            try:
                processor = self.get_processor(message)
                # processor.load_number_information()
            except Exception, e:
                logging.info("Error al procesar el mensaje" 
                    + message.message_id)
            # print processsor.generate_response()
            # processor.process()
        logging.info("=== Fin Proceso de mensajes ABDCP ===")