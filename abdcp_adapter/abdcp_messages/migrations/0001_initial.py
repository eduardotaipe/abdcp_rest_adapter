# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ABDCPMessage'
        db.create_table(u'abdcp_messages_abdcpmessage', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('message_id', self.gf('django.db.models.fields.CharField')(unique=True, max_length=17)),
            ('sender', self.gf('django.db.models.fields.related.ForeignKey')(related_name='messages_as_sender', to=orm['operators.Operator'])),
            ('recipient', self.gf('django.db.models.fields.related.ForeignKey')(related_name='messages_as_recipient', to=orm['operators.Operator'])),
            ('transaction_id', self.gf('django.db.models.fields.CharField')(unique=True, max_length=17)),
            ('request_document', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('response_document', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('responded', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'abdcp_messages', ['ABDCPMessage'])


    def backwards(self, orm):
        # Deleting model 'ABDCPMessage'
        db.delete_table(u'abdcp_messages_abdcpmessage')


    models = {
        u'abdcp_messages.abdcpmessage': {
            'Meta': {'object_name': 'ABDCPMessage'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '17'}),
            'recipient': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'messages_as_recipient'", 'to': u"orm['operators.Operator']"}),
            'request_document': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'responded': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'response_document': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'sender': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'messages_as_sender'", 'to': u"orm['operators.Operator']"}),
            'transaction_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '17'}),
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