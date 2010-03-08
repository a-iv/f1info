# -*- coding: utf-8 -*-

from south.db import db
from django.db import models
from f1info.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Deleting unique_together for [season, place] on point.
        db.delete_unique('f1info_point', ['season_id', 'place'])
        
        # Adding field 'Result.laps'
        db.add_column('f1info_result', 'laps', orm['f1info.result:laps'])
        
        # Adding field 'Heat.laps'
        db.add_column('f1info_heat', 'laps', orm['f1info.heat:laps'])
        
        # Adding field 'Point.position'
        db.add_column('f1info_point', 'position', orm['f1info.point:position'])
        
        # Changing field 'Heat.round'
        # (to signature: django.db.models.fields.IntegerField(null=True))
        db.alter_column('f1info_heat', 'round', orm['f1info.heat:round'])
        
        # Changing field 'Point.place'
        # (to signature: django.db.models.fields.IntegerField(null=True))
        db.alter_column('f1info_point', 'place', orm['f1info.point:place'])
        
        # Creating unique_together for [season, position] on Point.
        db.create_unique('f1info_point', ['season_id', 'position'])
        
    
    
    def backwards(self, orm):
        
        # Deleting unique_together for [season, position] on Point.
        db.delete_unique('f1info_point', ['season_id', 'position'])
        
        # Deleting field 'Result.laps'
        db.delete_column('f1info_result', 'laps')
        
        # Deleting field 'Heat.laps'
        db.delete_column('f1info_heat', 'laps')
        
        # Deleting field 'Point.position'
        db.delete_column('f1info_point', 'position')
        
        # Changing field 'Heat.round'
        # (to signature: django.db.models.fields.IntegerField())
        db.alter_column('f1info_heat', 'round', orm['f1info.heat:round'])
        
        # Changing field 'Point.place'
        # (to signature: django.db.models.fields.IntegerField())
        db.alter_column('f1info_point', 'place', orm['f1info.point:place'])
        
        # Creating unique_together for [season, place] on point.
        db.create_unique('f1info_point', ['season_id', 'place'])
        
    
    
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
            'season': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'grandprixs'", 'to': "orm['f1info.Season']"})
        },
        'f1info.heat': {
            'Meta': {'unique_together': "(('grandprix', 'type'),)"},
            'date': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today'}),
            'grandprix': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'heats'", 'to': "orm['f1info.GrandPrix']"}),
            'half_points': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'laps': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'round': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'time': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '3'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '1'})
        },
        'f1info.point': {
            'Meta': {'unique_together': "(('season', 'position'),)"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'place': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'point': ('django.db.models.fields.IntegerField', [], {}),
            'position': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'season': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'points'", 'to': "orm['f1info.Season']"})
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
            'fail': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'blank': 'True'}),
            'heat': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'results'", 'to': "orm['f1info.Heat']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'laps': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
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
