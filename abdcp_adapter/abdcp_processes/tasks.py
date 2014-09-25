import logging

from celery import shared_task

from abdcp_messages.models import ABDCPMessage
from abdcp_processes import ABDCPProcessor
from abdcp_adapter import settings

@shared_task
def process_message(message_id):
    retry = False
    try:
        logging.info("=== Begin ABDCP message process ===")
        message = ABDCPMessage.objects.get(message_id=message_id)
        result = ""
        processor = ABDCPProcessor.processor_factory(message)
        if processor is not None:
            processor.process()
            result = "Message %s (%s) has been processed" % \
                (message.message_id,message.message_type)
        else:
            result = "Message %s (%s) has NOT been processed, only stored"%\
                (message.message_id,message.message_type)
    except ABDCPMessage.DoesNotExist, e:
        result = "message id %s was not found" % message_id
    except Exception, e:
        result = "Error: processing message %s %s" % (message.message_id,e)
        retry = True
    
    logging.info(result)

    if retry:
        process_message.retry(
            [message_id] ,
            max_retries = settings.CELERY_MAX_RETRIES,
            countdown=settings.CELERY_COUNTDOWN
        )

    logging.info("=== End ABDCP message process ===")

    return result