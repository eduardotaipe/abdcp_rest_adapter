# -*- coding: utf-8 -*-

import logging
from django.core.management.base import BaseCommand
from django.conf import settings

from abdcp_messages.models import ABDCPMessage
from abdcp_processes import ABDCPProcessor


class Command(BaseCommand):
    def handle(self, *args, **options):
        messages = ABDCPMessage.objects.all()
        if messages.count()>0:
            logging.info(
                    "=== Iniciando Proceso de mensajes recibidos del ABDCP ==="
                )

            for m in messages:
                p = ABDCPProcessor.processor_factory(m)
                p.process()
                
            logging.info(
                    "=== Fin de proceso mensajes recibidos del ABDCP ==="
                )