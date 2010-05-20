# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Adding field 'Team.website'
        db.add_column('f1info_team', 'website', self.gf('django.db.models.fields.CharField')(default='', max_length=200, blank=True), keep_default=False)

        # Adding field 'Engine.website'
        db.add_column('f1info_engine', 'website', self.gf('django.db.models.fields.CharField')(default='', max_length=200, blank=True), keep_default=False)

        # Adding field 'Racer.website'
        db.add_column('f1info_racer', 'website', self.gf('django.db.models.fields.CharField')(default='', max_length=200, blank=True), keep_default=False)
    
    
    def backwards(self, orm):
        
        # Deleting field 'Team.website'
        db.delete_column('f1info_team', 'website')

        # Deleting field 'Engine.website'
        db.delete_column('f1info_engine', 'website')

        # Deleting field 'Racer.website'
        db.delete_column('f1info_racer', 'website')
    
    
    models = {
        'f1info.bestlap': {
            'Meta': {'unique_together': "(('heat', 'result'),)", 'object_name': 'BestLap'},
            'heat': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'bests'", 'to': "orm['f1info.Heat']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lap': ('django.db.models.fields.IntegerField', [], {}),
            'result': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'bests'", 'to': "orm['f1info.Result']"}),
            'time': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '3'})
        },
        'f1info.country': {
            'Meta': {'object_name': 'Country'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        'f1info.engine': {
            'Meta': {'object_name': 'Engine'},
            'country': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'engines'", 'blank': 'True', 'null': 'True', 'to': "orm['f1info.Country']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '100', 'unique': 'True', 'db_index': 'True'}),
            'website': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'})
        },
        'f1info.grandprix': {
            'Meta': {'unique_together': "(('season', 'name'),)", 'object_name': 'GrandPrix'},
            'abbr': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '3', 'blank': 'True'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'grandprixs'", 'blank': 'True', 'null': 'True', 'to': "orm['f1info.Country']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'index': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'season': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'grandprixs'", 'to': "orm['f1info.Season']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '100', 'unique': 'True', 'db_index': 'True'}),
            'tracklen': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'tracks'", 'blank': 'True', 'null': 'True', 'to': "orm['f1info.TrackLen']"})
        },
        'f1info.heat': {
            'Meta': {'unique_together': "(('grandprix', 'type'),)", 'object_name': 'Heat'},
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
            'Meta': {'unique_together': "(('season', 'position'),)", 'object_name': 'Point'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'point': ('django.db.models.fields.IntegerField', [], {}),
            'position': ('django.db.models.fields.IntegerField', [], {}),
            'season': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'points'", 'to': "orm['f1info.Season']"})
        },
        'f1info.racer': {
            'Meta': {'unique_together': "(('family_name', 'first_name'),)", 'object_name': 'Racer'},
            'birthday': ('django.db.models.fields.DateField', [], {}),
            'comment': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'racers'", 'blank': 'True', 'null': 'True', 'to': "orm['f1info.Country']"}),
            'family_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '100', 'unique': 'True', 'db_index': 'True'}),
            'website': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'})
        },
        'f1info.result': {
            'Meta': {'unique_together': "(('racer', 'heat'),)", 'object_name': 'Result'},
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
            'Meta': {'object_name': 'Season'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'year': ('django.db.models.fields.IntegerField', [], {})
        },
        'f1info.team': {
            'Meta': {'object_name': 'Team'},
            'country': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'teams'", 'blank': 'True', 'null': 'True', 'to': "orm['f1info.Country']"}),
            'founder': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '100', 'unique': 'True', 'db_index': 'True'}),
            'website': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'})
        },
        'f1info.track': {
            'Meta': {'object_name': 'Track'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '100', 'unique': 'True', 'db_index': 'True'})
        },
        'f1info.tracklen': {
            'Meta': {'object_name': 'TrackLen'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'length': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'track': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['f1info.Track']", 'null': 'True'})
        },
        'f1info.tyre': {
            'Meta': {'object_name': 'Tyre'},
            'country': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'tyres'", 'blank': 'True', 'null': 'True', 'to': "orm['f1info.Country']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '100', 'unique': 'True', 'db_index': 'True'})
        }
    }
    
    complete_apps = ['f1info']
