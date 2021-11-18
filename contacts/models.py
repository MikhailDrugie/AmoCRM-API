from django.db import models


class AccessToken(models.Model):
    token = models.CharField(max_length=1000)


class RefreshToken(models.Model):
    token = models.CharField(max_length=1000)


class Contact(models.Model):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
