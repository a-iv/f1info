# -*- coding: utf-8 -*-

from south.db import db
from django.db import models
from f1info.models import *

class Migration:

    def forwards(self, orm):
        for result in Result.objects.all():
            result.save()

    def backwards(self, orm):
        "Write your backwards migration here"


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
            '_points_count': ('django.db.models.fields.FloatField', [], {'default': '0'}),
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
