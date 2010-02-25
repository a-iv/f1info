# -*- coding: utf-8 -*-

from south.db import db
from django.db import models
from f1info.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'Heat'
        db.create_table('f1info_heat', (
            ('id', orm['f1info.Heat:id']),
            ('season', orm['f1info.Heat:season']),
            ('name', orm['f1info.Heat:name']),
            ('type', orm['f1info.Heat:type']),
            ('date', orm['f1info.Heat:date']),
            ('time', orm['f1info.Heat:time']),
            ('round', orm['f1info.Heat:round']),
        ))
        db.send_create_signal('f1info', ['Heat'])
        
        # Adding model 'Team'
        db.create_table('f1info_team', (
            ('id', orm['f1info.Team:id']),
            ('name', orm['f1info.Team:name']),
        ))
        db.send_create_signal('f1info', ['Team'])
        
        # Adding model 'Season'
        db.create_table('f1info_season', (
            ('id', orm['f1info.Season:id']),
            ('year', orm['f1info.Season:year']),
        ))
        db.send_create_signal('f1info', ['Season'])
        
        # Adding model 'BestRound'
        db.create_table('f1info_bestround', (
            ('id', orm['f1info.BestRound:id']),
            ('heat', orm['f1info.BestRound:heat']),
            ('result', orm['f1info.BestRound:result']),
            ('round', orm['f1info.BestRound:round']),
            ('time', orm['f1info.BestRound:time']),
        ))
        db.send_create_signal('f1info', ['BestRound'])
        
        # Adding model 'Score'
        db.create_table('f1info_score', (
            ('id', orm['f1info.Score:id']),
            ('season', orm['f1info.Score:season']),
            ('place', orm['f1info.Score:place']),
            ('score', orm['f1info.Score:score']),
        ))
        db.send_create_signal('f1info', ['Score'])
        
        # Adding model 'Result'
        db.create_table('f1info_result', (
            ('id', orm['f1info.Result:id']),
            ('racer', orm['f1info.Result:racer']),
            ('heat', orm['f1info.Result:heat']),
            ('delta', orm['f1info.Result:delta']),
            ('round', orm['f1info.Result:round']),
            ('fail', orm['f1info.Result:fail']),
        ))
        db.send_create_signal('f1info', ['Result'])
        
        # Adding model 'Engine'
        db.create_table('f1info_engine', (
            ('id', orm['f1info.Engine:id']),
            ('name', orm['f1info.Engine:name']),
        ))
        db.send_create_signal('f1info', ['Engine'])
        
        # Adding model 'Racer'
        db.create_table('f1info_racer', (
            ('id', orm['f1info.Racer:id']),
            ('family_name', orm['f1info.Racer:family_name']),
            ('first_name', orm['f1info.Racer:first_name']),
            ('nationality', orm['f1info.Racer:nationality']),
            ('birthday', orm['f1info.Racer:birthday']),
        ))
        db.send_create_signal('f1info', ['Racer'])
        
        # Creating unique_together for [season, type, name] on Heat.
        db.create_unique('f1info_heat', ['season_id', 'type', 'name'])
        
        # Creating unique_together for [family_name, first_name] on Racer.
        db.create_unique('f1info_racer', ['family_name', 'first_name'])
        
        # Creating unique_together for [season, place] on Score.
        db.create_unique('f1info_score', ['season_id', 'place'])
        
        # Creating unique_together for [heat, result] on BestRound.
        db.create_unique('f1info_bestround', ['heat_id', 'result_id'])
        
        # Creating unique_together for [racer, heat] on Result.
        db.create_unique('f1info_result', ['racer_id', 'heat_id'])
        
    
    
    def backwards(self, orm):
        
        # Deleting unique_together for [racer, heat] on Result.
        db.delete_unique('f1info_result', ['racer_id', 'heat_id'])
        
        # Deleting unique_together for [heat, result] on BestRound.
        db.delete_unique('f1info_bestround', ['heat_id', 'result_id'])
        
        # Deleting unique_together for [season, place] on Score.
        db.delete_unique('f1info_score', ['season_id', 'place'])
        
        # Deleting unique_together for [family_name, first_name] on Racer.
        db.delete_unique('f1info_racer', ['family_name', 'first_name'])
        
        # Deleting unique_together for [season, type, name] on Heat.
        db.delete_unique('f1info_heat', ['season_id', 'type', 'name'])
        
        # Deleting model 'Heat'
        db.delete_table('f1info_heat')
        
        # Deleting model 'Team'
        db.delete_table('f1info_team')
        
        # Deleting model 'Season'
        db.delete_table('f1info_season')
        
        # Deleting model 'BestRound'
        db.delete_table('f1info_bestround')
        
        # Deleting model 'Score'
        db.delete_table('f1info_score')
        
        # Deleting model 'Result'
        db.delete_table('f1info_result')
        
        # Deleting model 'Engine'
        db.delete_table('f1info_engine')
        
        # Deleting model 'Racer'
        db.delete_table('f1info_racer')
        
    
    
    models = {
        'f1info.bestround': {
            'Meta': {'unique_together': "(('heat', 'result'),)"},
            'heat': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'bests'", 'to': "orm['f1info.Heat']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'result': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'bests'", 'to': "orm['f1info.Result']"}),
            'round': ('django.db.models.fields.IntegerField', [], {}),
            'time': ('django.db.models.fields.TimeField', [], {})
        },
        'f1info.engine': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'f1info.heat': {
            'Meta': {'unique_together': "(('season', 'type', 'name'),)"},
            'date': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'round': ('django.db.models.fields.IntegerField', [], {}),
            'season': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'heats'", 'to': "orm['f1info.Season']"}),
            'time': ('django.db.models.fields.TimeField', [], {}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '1'})
        },
        'f1info.racer': {
            'Meta': {'unique_together': "(('family_name', 'first_name'),)"},
            'birthday': ('django.db.models.fields.DateField', [], {}),
            'family_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nationality': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'f1info.result': {
            'Meta': {'unique_together': "(('racer', 'heat'),)"},
            'delta': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'fail': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'heat': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'results'", 'to': "orm['f1info.Heat']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'racer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'results'", 'to': "orm['f1info.Racer']"}),
            'round': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'f1info.score': {
            'Meta': {'unique_together': "(('season', 'place'),)"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'place': ('django.db.models.fields.IntegerField', [], {}),
            'score': ('django.db.models.fields.IntegerField', [], {}),
            'season': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'seasons'", 'to': "orm['f1info.Season']"})
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
