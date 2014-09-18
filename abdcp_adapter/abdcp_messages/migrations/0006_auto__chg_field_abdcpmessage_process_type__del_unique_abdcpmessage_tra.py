# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'ABDCPMessage', fields ['transaction_id']
        db.delete_unique(u'abdcp_messages_abdcpmessage', ['transaction_id'])


        # Changing field 'ABDCPMessage.process_type'
        db.alter_column(u'abdcp_messages_abdcpmessage', 'process_type', self.gf('django.db.models.fields.CharField')(max_length=2, null=True))

    def backwards(self, orm):

        # Changing field 'ABDCPMessage.process_type'
        db.alter_column(u'abdcp_messages_abdcpmessage', 'process_type', self.gf('django.db.models.fields.TextField')(max_length=2, null=True))
        # Adding unique constraint on 'ABDCPMessage', fields ['transaction_id']
        db.create_unique(u'abdcp_messages_abdcpmessage', ['transaction_id'])


    models = {
        u'abdcp_messages.abdcpmessage': {
            'Meta': {'object_name': 'ABDCPMessage'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'delivered': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '17'}),
            'message_type': ('django.db.models.fields.TextField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'process_type': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'recipient': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'messages_as_recipient'", 'to': u"orm['operators.Operator']"}),
            'request_document': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'responded': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'response_document': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'sender': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'messages_as_sender'", 'to': u"orm['operators.Operator']"}),
            'stated_creation': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'transaction_id': ('django.db.models.fields.CharField', [], {'max_length': '17'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'operators.operator': {
            'Meta': {'object_name': 'Operator'},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'uri': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['abdcp_messages']