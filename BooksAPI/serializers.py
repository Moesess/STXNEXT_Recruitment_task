from rest_framework import serializers

from .models import Book, Category, Author


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['name', ]
        extra_kwargs = {'books': {'required': True}}


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name']


class BookSerializer(serializers.ModelSerializer):
    authors = AuthorSerializer(many=True)
    categories = CategorySerializer(many=True)

    class Meta:
        model = Book
        fields = ['title', 'authors', 'published_date', 'categories', 'average_rating', 'ratings_count', 'thumbnail']
        extra_kwargs = {'authors': {'required': True}}
