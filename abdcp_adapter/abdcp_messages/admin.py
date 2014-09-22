from django.contrib import admin
from abdcp_messages.models import ABDCPMessage

# ABDCP Messages

class ABDCPMessageAdmin(admin.ModelAdmin):

    list_display = (
        'message_id', 'sender', 'recipient', 'transaction_id', 'message_type', 'created',
    )

    list_filter = ('sender', )

    search_fields = [
        'message_id',
        'transaction_id',
        'request_document',
        'response_document'
    ]

    readonly_fields = ('responded', 'created', 'updated', )

    ordering = ('created', )

admin.site.register(ABDCPMessage, ABDCPMessageAdmin)
