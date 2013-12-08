from django.db import models

# Create your models here.
class SecretCode(models.Model):
    email = models.EmailField()
    secret_code = models.CharField(max_length=15)
