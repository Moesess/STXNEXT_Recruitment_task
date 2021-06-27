from __future__ import unicode_literals

from django.db import models


class Book(models.Model):
    """
    Simple Book model, author and category is joined via ManyToMany Field in their own ModelClasses
    """
    book_id = models.CharField(max_length=255, unique=True)
    title = models.CharField(max_length=255)
    published_date = models.CharField(max_length=10)
    average_rating = models.DecimalField(max_digits=5, decimal_places=2)
    ratings_count = models.DecimalField(max_digits=10, decimal_places=0)
    thumbnail = models.URLField()

    class Meta:
        verbose_name = "Book"
        verbose_name_plural = "Books"

    def __str__(self):
        return self.title


class Author(models.Model):
    """
    Simple Author Model, joins to the Book
    """
    name = models.CharField(max_length=255)
    books = models.ManyToManyField(Book, related_name='authors', blank=True)

    class Meta:
        verbose_name = "Author"
        verbose_name_plural = "Authors"

    def __str__(self):
        return self.name


class Category(models.Model):
    """
    Simple Category Model, joins to the Book
    """
    name = models.CharField(max_length=255)
    books = models.ManyToManyField(Book, related_name='categories', blank=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

