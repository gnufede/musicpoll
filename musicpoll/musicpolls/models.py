from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

class Song(models.Model):
    name = models.CharField(max_length=500)
    artist = models.CharField(max_length=500)
    lasturl = models.CharField(max_length=500)

    def __unicode__(self):
        return self.name + ' - ' + self.artist

class Choice(models.Model):
    user = models.ForeignKey(User)
    index = models.IntegerField(default=1,
                    validators=[MinValueValidator(1), MaxValueValidator(10)])
    song = models.ForeignKey(Song)
    date = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.user.username +' ('+str(self.index)+'): ' + str(self.song)

