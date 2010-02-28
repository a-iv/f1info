# -*- coding: utf-8 -*-

from south.db import db
from django.db import models
from f1info.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'GrandPrix'
        db.create_table('f1info_grandprix', (
            ('id', orm['f1info.grandprix:id']),
            ('season', orm['f1info.grandprix:season']),
            ('name', orm['f1info.grandprix:name']),
        ))
        db.send_create_signal('f1info', ['GrandPrix'])
        
        # Adding model 'Tyre'
        db.create_table('f1info_tyre', (
            ('id', orm['f1info.tyre:id']),
            ('name', orm['f1info.tyre:name']),
        ))
        db.send_create_signal('f1info', ['Tyre'])
        
        # Adding model 'BestLap'
        db.create_table('f1info_bestlap', (
            ('id', orm['f1info.bestlap:id']),
            ('heat', orm['f1info.bestlap:heat']),
            ('result', orm['f1info.bestlap:result']),
            ('lap', orm['f1info.bestlap:lap']),
            ('time', orm['f1info.bestlap:time']),
        ))
        db.send_create_signal('f1info', ['BestLap'])
        
        # Adding model 'Result'
        db.create_table('f1info_result', (
            ('id', orm['f1info.result:id']),
            ('heat', orm['f1info.result:heat']),
            ('half_points', orm['f1info.result:half_points']),
            ('position', orm['f1info.result:position']),
            ('racer', orm['f1info.result:racer']),
            ('team', orm['f1info.result:team']),
            ('engine', orm['f1info.result:engine']),
            ('tyre', orm['f1info.result:tyre']),
            ('delta', orm['f1info.result:delta']),
            ('round', orm['f1info.result:round']),
            ('fail', orm['f1info.result:fail']),
        ))
        db.send_create_signal('f1info', ['Result'])
        
        # Adding model 'Heat'
        db.create_table('f1info_heat', (
            ('id', orm['f1info.heat:id']),
            ('grandprix', orm['f1info.heat:grandprix']),
            ('type', orm['f1info.heat:type']),
            ('date', orm['f1info.heat:date']),
            ('time', orm['f1info.heat:time']),
            ('round', orm['f1info.heat:round']),
        ))
        db.send_create_signal('f1info', ['Heat'])
        
        # Adding model 'Point'
        db.create_table('f1info_point', (
            ('id', orm['f1info.point:id']),
            ('season', orm['f1info.point:season']),
            ('place', orm['f1info.point:place']),
            ('point', orm['f1info.point:point']),
        ))
        db.send_create_signal('f1info', ['Point'])
        
        # Creating unique_together for [grandprix, type] on Heat.
        db.create_unique('f1info_heat', ['grandprix_id', 'type'])
        
        # Creating unique_together for [heat, result] on BestLap.
        db.create_unique('f1info_bestlap', ['heat_id', 'result_id'])
        
        # Creating unique_together for [season, place] on Point.
        db.create_unique('f1info_point', ['season_id', 'place'])
        
        # Creating unique_together for [season, name] on GrandPrix.
        db.create_unique('f1info_grandprix', ['season_id', 'name'])
        
        # Creating unique_together for [racer, heat] on Result.
        db.create_unique('f1info_result', ['racer_id', 'heat_id'])
        
    
    
    def backwards(self, orm):
        
        # Deleting unique_together for [racer, heat] on Result.
        db.delete_unique('f1info_result', ['racer_id', 'heat_id'])
        
        # Deleting unique_together for [season, name] on GrandPrix.
        db.delete_unique('f1info_grandprix', ['season_id', 'name'])
        
        # Deleting unique_together for [season, place] on Point.
        db.delete_unique('f1info_point', ['season_id', 'place'])
        
        # Deleting unique_together for [heat, result] on BestLap.
        db.delete_unique('f1info_bestlap', ['heat_id', 'result_id'])
        
        # Deleting unique_together for [grandprix, type] on Heat.
        db.delete_unique('f1info_heat', ['grandprix_id', 'type'])
        
        # Deleting model 'GrandPrix'
        db.delete_table('f1info_grandprix')
        
        # Deleting model 'Tyre'
        db.delete_table('f1info_tyre')
        
        # Deleting model 'BestLap'
        db.delete_table('f1info_bestlap')
        
        # Deleting model 'Result'
        db.delete_table('f1info_result')
        
        # Deleting model 'Heat'
        db.delete_table('f1info_heat')
        
        # Deleting model 'Point'
        db.delete_table('f1info_point')
        
    
    
    models = {
        'f1info.bestlap': {
            'Meta': {'unique_together': "(('heat', 'result'),)"},
            'heat': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'bests'", 'to': "orm['f1info.Heat']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lap': ('django.db.models.fields.IntegerField', [], {}),
            'result': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'bests'", 'to': "orm['f1info.Result']"}),
            'time': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '3'})
        },
        'f1info.engine': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'f1info.grandprix': {
            'Meta': {'unique_together': "(('season', 'name'),)"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'season': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'grandprix'", 'to': "orm['f1info.Season']"})
        },
        'f1info.heat': {
            'Meta': {'unique_together': "(('grandprix', 'type'),)"},
            'date': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today'}),
            'grandprix': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'heats'", 'to': "orm['f1info.GrandPrix']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'round': ('django.db.models.fields.IntegerField', [], {}),
            'time': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '3'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '1'})
        },
        'f1info.point': {
            'Meta': {'unique_together': "(('season', 'place'),)"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'place': ('django.db.models.fields.IntegerField', [], {}),
            'point': ('django.db.models.fields.IntegerField', [], {}),
            'season': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'seasons'", 'to': "orm['f1info.Season']"})
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
        'f1info.result': {
            'Meta': {'unique_together': "(('racer', 'heat'),)"},
            'delta': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '8', 'decimal_places': '3', 'blank': 'True'}),
            'engine': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'results'", 'to': "orm['f1info.Engine']"}),
            'fail': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'half_points': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'heat': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'results'", 'to': "orm['f1info.Heat']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'position': ('django.db.models.fields.IntegerField', [], {}),
            'racer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'results'", 'to': "orm['f1info.Racer']"}),
            'round': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'team': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'results'", 'to': "orm['f1info.Team']"}),
            'tyre': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'results'", 'to': "orm['f1info.Tyre']"})
        },
        'f1info.season': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'year': ('django.db.models.fields.IntegerField', [], {})
        },
        'f1info.team': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'f1info.tyre': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }
    
    complete_apps = ['f1info']
