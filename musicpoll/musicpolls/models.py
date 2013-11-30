from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Artist(models.Model):
    mbid = models.CharField(max_length=500)
    lasturl = models.CharField(max_length=500)
    name = models.CharField(max_length=500)

    def __unicode__(self):
        return self.name

class Album(models.Model):
    mbid = models.CharField(max_length=500)
    lasturl = models.CharField(max_length=500)
    name = models.CharField(max_length=500)
    year = models.IntegerField()
    artists = models.ManyToManyField(Artist)

    def __unicode__(self):
        return self.name +' ('+ str(self.year) +')'

class Song(models.Model):
    lastid = models.IntegerField()
    lasturl = models.CharField(max_length=500)
    mbid = models.CharField(max_length=500)
    name = models.CharField(max_length=500)
    artist = models.ForeignKey(Artist)
    album = models.ForeignKey(Album)

    def __unicode__(self):
        return self.artist.__unicode__ +' - '+ self.name

class Choice(models.Model):
    user = models.ForeignKey(User)
    song = models.ManyToManyField(Song)
    index = models.IntegerField(default=0)
    date = models.DateTimeField()

