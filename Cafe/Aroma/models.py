from django.db import models



class Admins(models.Model):
    Username = models.CharField(max_length=255, blank= False, unique=True, primary_key=True)
    Email = models.EmailField(max_length=255, blank= False, unique=True)
    Password = models.CharField(max_length=255, blank= False, unique=True)


class Storage(models.Model):
    id = models.AutoField(unique=True, primary_key=True)
    Name = models.CharField(max_length=255, blank= False, unique=True)
    Amount = models.CharField(max_length=255, blank= False)

class Users(models.Model):
    Username = models.CharField(max_length=255, blank= False, unique=True, primary_key=True)
    Full_name = models.CharField(max_length=255, blank= False)
    Email = models.EmailField(max_length=255, blank= False, unique=True)
    Password = models.CharField(max_length=255, blank=False, unique=True, default= 000000)
    Phone_Number = models.IntegerField(max_length=11)
class Product(models.Model):
    VERTICAL_CHOICES = [
        ('Shake', 'Shake'),
        ('Cake', 'Cake'),
        ('Cookie', 'Cookie'),
    ]
    id = models.AutoField(unique=True, primary_key=True)
    Name = models.CharField(unique=True, max_length=255)
    Sugar = models.IntegerField(max_length=10)
    Coffee = models.IntegerField(max_length=10)
    Flour = models.IntegerField(max_length=10)
    Chocolate = models.IntegerField(max_length=10)
    Price = models.IntegerField(max_length=10)
    Vertical = models.CharField(max_length=10, choices=VERTICAL_CHOICES)

class Orders(models.Model):

    OrderID = models.AutoField(unique=True, primary_key=True)
    Username = models.ManyToManyField(Users, related_name='Orders')
    Products = models.ManyToManyField(Product, related_name= 'Orders')
    Purchase_amount = models.IntegerField(max_length=10)
    Type = models.CharField(max_length=10)
