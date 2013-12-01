# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Album'
        db.delete_table('musicpolls_album')

        # Removing M2M table for field artists on 'Album'
        db.delete_table(db.shorten_name('musicpolls_album_artists'))

        # Deleting model 'Artist'
        db.delete_table('musicpolls_artist')

        # Deleting field 'Song.mbid'
        db.delete_column('musicpolls_song', 'mbid')

        # Deleting field 'Song.lastid'
        db.delete_column('musicpolls_song', 'lastid')

        # Deleting field 'Song.album'
        db.delete_column('musicpolls_song', 'album_id')


        # Renaming column for 'Song.artist' to match new field type.
        db.rename_column('musicpolls_song', 'artist_id', 'artist')
        # Changing field 'Song.artist'
        db.alter_column('musicpolls_song', 'artist', self.gf('django.db.models.fields.CharField')(max_length=500))
        # Removing index on 'Song', fields ['artist']
        db.delete_index('musicpolls_song', ['artist_id'])


    def backwards(self, orm):
        # Adding index on 'Song', fields ['artist']
        db.create_index('musicpolls_song', ['artist_id'])

        # Adding model 'Album'
        db.create_table('musicpolls_album', (
            ('mbid', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('year', self.gf('django.db.models.fields.IntegerField')()),
            ('lasturl', self.gf('django.db.models.fields.CharField')(max_length=500)),
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

        # Adding model 'Artist'
        db.create_table('musicpolls_artist', (
            ('mbid', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('lasturl', self.gf('django.db.models.fields.CharField')(max_length=500)),
        ))
        db.send_create_signal('musicpolls', ['Artist'])


        # User chose to not deal with backwards NULL issues for 'Song.mbid'
        #raise RuntimeError("Cannot reverse this migration. 'Song.mbid' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'Song.mbid'
        db.add_column('musicpolls_song', 'mbid',
                      self.gf('django.db.models.fields.CharField')(max_length=500),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'Song.lastid'
        #raise RuntimeError("Cannot reverse this migration. 'Song.lastid' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'Song.lastid'
        db.add_column('musicpolls_song', 'lastid',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Song.album'
        db.add_column('musicpolls_song', 'album',
                      self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['musicpolls.Album'], blank=True),
                      keep_default=False)


        # Renaming column for 'Song.artist' to match new field type.
        db.rename_column('musicpolls_song', 'artist', 'artist_id')
        # Changing field 'Song.artist'
        db.alter_column('musicpolls_song', 'artist_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['musicpolls.Artist']))

    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'unique': 'True'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'blank': 'True', 'to': "orm['auth.Permission']"})
        },
        'auth.permission': {
            'Meta': {'object_name': 'Permission', 'unique_together': "(('content_type', 'codename'),)", 'ordering': "('content_type__app_label', 'content_type__model', 'codename')"},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'user_set'", 'to': "orm['auth.Group']", 'blank': 'True', 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'user_set'", 'to': "orm['auth.Permission']", 'blank': 'True', 'symmetrical': 'False'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '30', 'unique': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'db_table': "'django_content_type'", 'object_name': 'ContentType', 'unique_together': "(('app_label', 'model'),)", 'ordering': "('name',)"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'musicpolls.choice': {
            'Meta': {'object_name': 'Choice'},
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'index': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'song': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['musicpolls.Song']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'musicpolls.song': {
            'Meta': {'object_name': 'Song'},
            'artist': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lasturl': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        }
    }

    complete_apps = ['musicpolls']
