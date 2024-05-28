from django.db import models

# Create your models here.
class User(models.Model):
    username=models.CharField(max_length=20)
    email=models.CharField(max_length=50)
    password=models.CharField(max_length=25)

class Product_Item(models.Model):
    username=models.CharField(max_length=20)
    card_num=models.IntegerField()
    count=models.IntegerField()

class Feedback_Item(models.Model):
    username=models.CharField(max_length=20)
    header=models.TextField()
    description=models.TextField()
    rating=models.IntegerField()
    date=models.TextField()
class Custom_Item_I(models.Model):
    username=models.CharField(max_length=20)
    game_genre=models.TextField()
    all_cost=models.IntegerField()
    count=models.IntegerField()
    scale_game=models.IntegerField()
    style_graphics=models.TextField()
    mechanics=models.IntegerField()
    type_graphics=models.TextField()