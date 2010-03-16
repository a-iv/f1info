# -*- coding: utf-8 -*-

from south.db import db
from django.db import models
from f1info.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Changing field 'Heat.slug'
        # (to signature: django.db.models.fields.SlugField(max_length=100, unique=True, db_index=True))
        db.alter_column('f1info_heat', 'slug', orm['f1info.heat:slug'])
        
        # Changing field 'Team.slug'
        # (to signature: django.db.models.fields.SlugField(max_length=100, unique=True, db_index=True))
        db.alter_column('f1info_team', 'slug', orm['f1info.team:slug'])
        
        # Changing field 'Tyre.slug'
        # (to signature: django.db.models.fields.SlugField(max_length=100, unique=True, db_index=True))
        db.alter_column('f1info_tyre', 'slug', orm['f1info.tyre:slug'])
        
        # Changing field 'GrandPrix.slug'
        # (to signature: django.db.models.fields.SlugField(max_length=100, unique=True, db_index=True))
        db.alter_column('f1info_grandprix', 'slug', orm['f1info.grandprix:slug'])
        
        # Changing field 'Engine.slug'
        # (to signature: django.db.models.fields.SlugField(max_length=100, unique=True, db_index=True))
        db.alter_column('f1info_engine', 'slug', orm['f1info.engine:slug'])
        
        # Changing field 'Racer.slug'
        # (to signature: django.db.models.fields.SlugField(max_length=100, unique=True, db_index=True))
        db.alter_column('f1info_racer', 'slug', orm['f1info.racer:slug'])
        
        # Creating unique_together for [slug] on Racer.
        db.create_unique('f1info_racer', ['slug'])
        
        # Creating unique_together for [slug] on GrandPrix.
        db.create_unique('f1info_grandprix', ['slug'])
        
        # Creating unique_together for [slug] on Team.
        db.create_unique('f1info_team', ['slug'])
        
        # Creating unique_together for [slug] on Engine.
        db.create_unique('f1info_engine', ['slug'])
        
        # Creating unique_together for [slug] on Heat.
        db.create_unique('f1info_heat', ['slug'])
        
        # Creating unique_together for [slug] on Tyre.
        db.create_unique('f1info_tyre', ['slug'])
        
    
    
    def backwards(self, orm):
        
        # Deleting unique_together for [slug] on Tyre.
        db.delete_unique('f1info_tyre', ['slug'])
        
        # Deleting unique_together for [slug] on Heat.
        db.delete_unique('f1info_heat', ['slug'])
        
        # Deleting unique_together for [slug] on Engine.
        db.delete_unique('f1info_engine', ['slug'])
        
        # Deleting unique_together for [slug] on Team.
        db.delete_unique('f1info_team', ['slug'])
        
        # Deleting unique_together for [slug] on GrandPrix.
        db.delete_unique('f1info_grandprix', ['slug'])
        
        # Deleting unique_together for [slug] on Racer.
        db.delete_unique('f1info_racer', ['slug'])
        
        # Changing field 'Heat.slug'
        # (to signature: django.db.models.fields.SlugField(max_length=100, null=True, db_index=True))
        db.alter_column('f1info_heat', 'slug', orm['f1info.heat:slug'])
        
        # Changing field 'Team.slug'
        # (to signature: django.db.models.fields.SlugField(max_length=100, null=True, db_index=True))
        db.alter_column('f1info_team', 'slug', orm['f1info.team:slug'])
        
        # Changing field 'Tyre.slug'
        # (to signature: django.db.models.fields.SlugField(max_length=100, null=True, db_index=True))
        db.alter_column('f1info_tyre', 'slug', orm['f1info.tyre:slug'])
        
        # Changing field 'GrandPrix.slug'
        # (to signature: django.db.models.fields.SlugField(max_length=100, null=True, db_index=True))
        db.alter_column('f1info_grandprix', 'slug', orm['f1info.grandprix:slug'])
        
        # Changing field 'Engine.slug'
        # (to signature: django.db.models.fields.SlugField(max_length=100, null=True, db_index=True))
        db.alter_column('f1info_engine', 'slug', orm['f1info.engine:slug'])
        
        # Changing field 'Racer.slug'
        # (to signature: django.db.models.fields.SlugField(max_length=100, null=True, db_index=True))
        db.alter_column('f1info_racer', 'slug', orm['f1info.racer:slug'])
        
    
    
    models = {
        'f1info.bestlap': {
            'Meta': {'unique_together': "(('heat', 'result'),)"},
            'heat': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'bests'", 'to': "orm['f1info.Heat']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lap': ('django.db.models.fields.IntegerField', [], {}),
            'result': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'bests'", 'to': "orm['f1info.Result']"}),
            'time': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '3'})
        },
        'f1info.country': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        'f1info.engine': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '100', 'unique': 'True', 'db_index': 'True'})
        },
        'f1info.grandprix': {
            'Meta': {'unique_together': "(('season', 'name'),)"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'index': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'season': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'grandprixs'", 'to': "orm['f1info.Season']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '100', 'unique': 'True', 'db_index': 'True'})
        },
        'f1info.heat': {
            'Meta': {'unique_together': "(('grandprix', 'type'),)"},
            'date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'grandprix': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'heats'", 'to': "orm['f1info.GrandPrix']"}),
            'half_points': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'laps': ('django.db.models.fields.IntegerField', [], {}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '100', 'unique': 'True', 'db_index': 'True'}),
            'time': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '3'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '1'})
        },
        'f1info.point': {
            'Meta': {'unique_together': "(('season', 'position'),)"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'point': ('django.db.models.fields.IntegerField', [], {}),
            'position': ('django.db.models.fields.IntegerField', [], {}),
            'season': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'points'", 'to': "orm['f1info.Season']"})
        },
        'f1info.racer': {
            'Meta': {'unique_together': "(('family_name', 'first_name'),)"},
            'birthday': ('django.db.models.fields.DateField', [], {}),
            'comment': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'racers'", 'blank': 'True', 'null': 'True', 'to': "orm['f1info.Country']"}),
            'family_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '100', 'unique': 'True', 'db_index': 'True'})
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
            'team': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'results'", 'to': "orm['f1info.Team']"}),
            'tyre': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'results'", 'to': "orm['f1info.Tyre']"})
        },
        'f1info.season': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'year': ('django.db.models.fields.IntegerField', [], {})
        },
        'f1info.team': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '100', 'unique': 'True', 'db_index': 'True'})
        },
        'f1info.tyre': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '100', 'unique': 'True', 'db_index': 'True'})
        }
    }
    
    complete_apps = ['f1info']
