from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Song(models.Model):
    lasturl = models.CharField(max_length=500)
    name = models.CharField(max_length=500)
    artist = models.CharField(max_length=500)

    def __unicode__(self):
        return self.artist +' - '+ self.name

class Choice(models.Model):
    user = models.ForeignKey(User)
    song = models.ForeignKey(Song)
    index = models.IntegerField(default=0)
    date = models.DateTimeField()
