from django.db import models



class Admins(models.Model):
    Username = models.CharField(max_length=255, blank= False, unique=True)
    Email = models.CharField(max_length=255, blank= False, unique=True)
    Password = models.CharField(max_length=255, blank= False, unique=True)


class Storage(models.Model):
    ID = models.AutoField(unique=True, primary_key=True)
    Name = models.CharField(max_length=255, blank= False, unique=True)
    Amount = models.CharField(max_length=255, blank= False)