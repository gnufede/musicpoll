# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Artist'
        db.create_table('musicpolls_artist', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('mbid', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('lasturl', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=500)),
        ))
        db.send_create_signal('musicpolls', ['Artist'])

        # Adding model 'Album'
        db.create_table('musicpolls_album', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('mbid', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('lasturl', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('year', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('musicpolls', ['Album'])

        # Adding M2M table for field artists on 'Album'
        m2m_table_name = db.shorten_name('musicpolls_album_artists')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('album', models.ForeignKey(orm['musicpolls.album'], null=False)),
            ('artist', models.ForeignKey(orm['musicpolls.artist'], null=False))
        ))
        db.create_unique(m2m_table_name, ['album_id', 'artist_id'])

        # Adding model 'Song'
        db.create_table('musicpolls_song', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('lastid', self.gf('django.db.models.fields.IntegerField')()),
            ('lasturl', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('mbid', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('artist', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['musicpolls.Artist'])),
        ))
        db.send_create_signal('musicpolls', ['Song'])

        # Adding model 'Choice'
        db.create_table('musicpolls_choice', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('index', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('date', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('musicpolls', ['Choice'])

        # Adding M2M table for field song on 'Choice'
        m2m_table_name = db.shorten_name('musicpolls_choice_song')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('choice', models.ForeignKey(orm['musicpolls.choice'], null=False)),
            ('song', models.ForeignKey(orm['musicpolls.song'], null=False))
        ))
        db.create_unique(m2m_table_name, ['choice_id', 'song_id'])


    def backwards(self, orm):
        # Deleting model 'Artist'
        db.delete_table('musicpolls_artist')

        # Deleting model 'Album'
        db.delete_table('musicpolls_album')

        # Removing M2M table for field artists on 'Album'
        db.delete_table(db.shorten_name('musicpolls_album_artists'))

        # Deleting model 'Song'
        db.delete_table('musicpolls_song')

        # Deleting model 'Choice'
        db.delete_table('musicpolls_choice')

        # Removing M2M table for field song on 'Choice'
        db.delete_table(db.shorten_name('musicpolls_choice_song'))


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'to': "orm['auth.Permission']", 'symmetrical': 'False'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'blank': 'True', 'max_length': '75'}),
            'first_name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '30'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'user_set'", 'blank': 'True', 'to': "orm['auth.Group']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '30'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'user_set'", 'blank': 'True', 'to': "orm['auth.Permission']", 'symmetrical': 'False'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'db_table': "'django_content_type'", 'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType'},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'musicpolls.album': {
            'Meta': {'object_name': 'Album'},
            'artists': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['musicpolls.Artist']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lasturl': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'mbid': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'year': ('django.db.models.fields.IntegerField', [], {})
        },
        'musicpolls.artist': {
            'Meta': {'object_name': 'Artist'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lasturl': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'mbid': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        },
        'musicpolls.choice': {
            'Meta': {'object_name': 'Choice'},
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'index': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'song': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['musicpolls.Song']", 'symmetrical': 'False'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'musicpolls.song': {
            'Meta': {'object_name': 'Song'},
            'artist': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['musicpolls.Artist']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lastid': ('django.db.models.fields.IntegerField', [], {}),
            'lasturl': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'mbid': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        }
    }

    complete_apps = ['musicpolls']
