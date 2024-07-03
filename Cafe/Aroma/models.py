from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone


class Admins(models.Model):
    Username = models.CharField(max_length=255, blank= False, unique=True, primary_key=True)
    Email = models.EmailField(max_length=255, blank= False, unique=True)
    Password = models.CharField(max_length=255, blank= False, unique=True)


class Users(models.Model):
    Username = models.CharField(max_length=255, blank= False, unique=True, primary_key=True)
    Full_name = models.CharField(max_length=255, blank= False)
    Email = models.EmailField(max_length=255, blank= False, unique=True)
    Password = models.CharField(max_length=255, blank=False, unique=True, default= 000000)
    Phone_Number = models.IntegerField(max_length=11)


class Storage(models.Model):
    id = models.AutoField(unique=True, primary_key=True)
    date = models.DateTimeField(default=timezone.now)
    sugar = models.FloatField(blank=False, default=0)
    flour = models.FloatField(blank=False, default=0)
    coffee = models.FloatField(blank=False, default=0)
    chocolate = models.FloatField(blank=False, default=0)

    def update_inventory(self, product, quantity):
        self.sugar -= product.Sugar * quantity
        self.flour -= product.Flour * quantity
        self.coffee -= product.Coffee * quantity
        self.chocolate -= product.Chocolate * quantity

    def revert_inventory(self, product, quantity):
        self.sugar += product.Sugar * quantity
        self.flour += product.Flour * quantity
        self.coffee += product.Coffee * quantity
        self.chocolate += product.Chocolate * quantity


class Product(models.Model):
    VERTICAL_CHOICES = [
        ('Cold Drink', 'Cold Drink'),
        ('Cake', 'Cake'),
        ('Hot Drink', 'Hot Drink'),
        ('Food', 'Food')
    ]
    id = models.AutoField(unique=True, primary_key=True)
    Name = models.CharField(unique=True, max_length=255)
    Sugar = models.FloatField()
    Coffee = models.FloatField()
    Flour = models.FloatField()
    Chocolate = models.FloatField()
    Price = models.FloatField()
    Vertical = models.CharField(max_length=10, choices=VERTICAL_CHOICES)
    image_url = models.URLField(max_length=200, blank=False, default='')

    def __str__(self):
        return self.Name



class Orders(models.Model):
    CHOICES = [
        (1, 'Take Away'),
        (2, 'In Person'),
             ]
    OrderID = models.AutoField(unique=True, primary_key=True)
    Username = models.ManyToManyField(Users, related_name='Orders')
    Products = models.ManyToManyField(Product, related_name= 'Orders')
    Purchase_amount = models.IntegerField(max_length=10)
    Type = models.IntegerField(choices=CHOICES)
    created_at = models.DateTimeField(default=timezone.now)


    
    def save(self, *args, **kwargs):
        super(Orders, self).save(*args, **kwargs)
        self.update_inventory()

    def update_inventory(self):
        for product in self.Products.all():
            try:
                storage = Storage.objects.latest('id')  # Assuming you have the latest storage entry
                if (storage.sugar >= product.Sugar * self.Purchase_amount and
                    storage.coffee >= product.Coffee * self.Purchase_amount and
                    storage.flour >= product.Flour * self.Purchase_amount and
                    storage.chocolate >= product.Chocolate * self.Purchase_amount):
                    
                    # Reduce inventory
                    storage.sugar -= product.Sugar * self.Purchase_amount
                    storage.coffee -= product.Coffee * self.Purchase_amount
                    storage.flour -= product.Flour * self.Purchase_amount
                    storage.chocolate -= product.Chocolate * self.Purchase_amount
                    storage.save()
                else:
                    # Raise an error or handle insufficient stock situation
                    raise ValidationError("Insufficient stock for product: {}".format(product.Name))
            except Storage.DoesNotExist:
                raise ValidationError("Storage does not exist. Please initialize storage.")

    def __str__(self):
        return f"Order {self.OrderID}"

