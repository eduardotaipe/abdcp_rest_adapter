from django.contrib import admin
from operators.models import Operator

# Operators

class OperatorAdmin(admin.ModelAdmin):

    list_display = (
        'id', 'name', 'code', 'uri', 'created','updated',
    )

    ordering = ('created', )

admin.site.register(Operator, OperatorAdmin)
