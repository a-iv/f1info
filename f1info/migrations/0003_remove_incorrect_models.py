# -*- coding: utf-8 -*-

from south.db import db
from django.db import models
from f1info.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Deleting model 'result'
        db.delete_table('f1info_result')
        
        # Deleting model 'heat'
        db.delete_table('f1info_heat')
        
        # Deleting model 'score'
        db.delete_table('f1info_score')
        
        # Deleting model 'bestround'
        db.delete_table('f1info_bestround')
        
    
    
    def backwards(self, orm):
        
        # Adding model 'result'
        db.create_table('f1info_result', (
            ('racer', orm['f1info.bestround:racer']),
            ('round', orm['f1info.bestround:round']),
            ('heat', orm['f1info.bestround:heat']),
            ('delta', orm['f1info.bestround:delta']),
            ('fail', orm['f1info.bestround:fail']),
            ('id', orm['f1info.bestround:id']),
        ))
        db.send_create_signal('f1info', ['result'])
        
        # Adding model 'heat'
        db.create_table('f1info_heat', (
            ('name', orm['f1info.bestround:name']),
            ('season', orm['f1info.bestround:season']),
            ('round', orm['f1info.bestround:round']),
            ('time', orm['f1info.bestround:time']),
            ('date', orm['f1info.bestround:date']),
            ('type', orm['f1info.bestround:type']),
            ('id', orm['f1info.bestround:id']),
        ))
        db.send_create_signal('f1info', ['heat'])
        
        # Adding model 'score'
        db.create_table('f1info_score', (
            ('score', orm['f1info.bestround:score']),
            ('place', orm['f1info.bestround:place']),
            ('id', orm['f1info.bestround:id']),
            ('season', orm['f1info.bestround:season']),
        ))
        db.send_create_signal('f1info', ['score'])
        
        # Adding model 'bestround'
        db.create_table('f1info_bestround', (
            ('round', orm['f1info.bestround:round']),
            ('heat', orm['f1info.bestround:heat']),
            ('result', orm['f1info.bestround:result']),
            ('time', orm['f1info.bestround:time']),
            ('id', orm['f1info.bestround:id']),
        ))
        db.send_create_signal('f1info', ['bestround'])
        
    
    
    models = {
        'f1info.engine': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'f1info.racer': {
            'Meta': {'unique_together': "(('family_name', 'first_name'),)"},
            'birthday': ('django.db.models.fields.DateField', [], {}),
            'comment': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200'}),
            'family_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nationality': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'f1info.season': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'year': ('django.db.models.fields.IntegerField', [], {})
        },
        'f1info.team': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }
    
    complete_apps = ['f1info']
