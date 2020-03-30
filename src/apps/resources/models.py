from django.db import models

class Contact(models.Model):
    name = models.CharField(max_length=30)
    password = models.CharField(max_length=128)
