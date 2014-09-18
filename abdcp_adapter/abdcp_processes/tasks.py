import logging

from abdcp_messages.models import ABDCPMessage
from abdcp_processes import ABDCPProcessor
from abdcp_processes.cp import ECPC_ABDCPProcessor
from abdcp_processes.sp import ESC_ABDCPProcessor

from celery import shared_task


@shared_task
def process_message(message_id):
    logging.info("=== Begin ABDCP message process ===")
    message = ABDCPMessage.objects.get(message_id=message_id)
    try:
        processor = ABDCPProcessor.processor_factory(message)
        processor.process()
        logging.info("Message %s has been processed", message.message_id)
    except Exception, e:
        logging.info("Error: processing message %s %s" % (message.message_id,e))
    logging.info("=== End ABDCP message process ===")


@shared_task
def send_email(data):
    pass

