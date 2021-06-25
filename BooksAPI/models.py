from django.db import models


# Create your models here.
class Book(models.Model):
    title = models.CharField()
    published_date = models.DateField()
    average_rating = models.DecimalField(max_digits=5, decimal_places=2)
    ratings_count = models.DecimalField(max_digits=10, decimal_places=0)
    thumbnail = models.URLField()


class Author(models.Model):
    name = models.CharField()
    surname = models.CharField()
    books = models.ManyToManyField(Book)


class Category(models.Model):
    name = models.CharField()
    books = models.ManyToManyField(Book)

