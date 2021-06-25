from __future__ import unicode_literals

from django.db import models


# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=255)
    published_date = models.DateField()
    average_rating = models.DecimalField(max_digits=5, decimal_places=2)
    ratings_count = models.DecimalField(max_digits=10, decimal_places=0)
    thumbnail = models.URLField()

    class Meta:
        verbose_name = "Book"
        verbose_name_plural = "Books"

    def __str__(self):
        return self.title


class Author(models.Model):
    name = models.CharField(max_length=255)
    books = models.ManyToManyField(Book, related_name='authors')

    class Meta:
        verbose_name = "Author"
        verbose_name_plural = "Authors"

    def __str__(self):
        return f'{self.name}'


class Category(models.Model):
    name = models.CharField(max_length=255)
    books = models.ManyToManyField(Book, related_name='categories')

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

