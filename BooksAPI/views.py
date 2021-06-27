import requests

from django.http import HttpResponse
from rest_framework import viewsets, mixins

from .models import Author, Book, Category
from .serializers import BookSerializer

from BooksAPI.filtersets import BookFilterSet


class BookListView(mixins.ListModelMixin,
                   mixins.RetrieveModelMixin,
                   viewsets.GenericViewSet):
    """
    List of Books,
    can be filtered using eg. ?author="Jeff Barton", ?title="Hobbit", ?published_date="2017"
    """

    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filterset_class = BookFilterSet
    ordering_fields = ['published_date']
    # filter_backends = [django_filters.rest_framework.DjangoFilterBackend]


def get_data(request):
    response = requests.get("https://www.googleapis.com/books/v1/volumes?q=Hobbit").json()

    # For each book in response from api
    for book in response["items"]:
        book_id = str(book["id"])
        title = str(book["volumeInfo"]["title"])
        published_date = str(book["volumeInfo"]["publishedDate"])

        average_rating = float(book["volumeInfo"].get("averageRating", 0))
        ratings_count = int(book["volumeInfo"].get("ratingsCount", 0))
        thumbnail = str(book["volumeInfo"].get("imageLinks", {}).get("thumbnail", ""))

        Book.objects.update_or_create(
            book_id=book_id,
            defaults={
                'title': title,
                'published_date': published_date,
                'average_rating': average_rating,
                'ratings_count': ratings_count,
                'thumbnail': thumbnail
            }
        )

        b = Book.objects.get(book_id=book_id)

        for author in book["volumeInfo"]["authors"]:
            a, created = Author.objects.get_or_create(name=author)
            a.books.add(b)
            a.save()

        if "categories" in book["volumeInfo"]:
            for category in book["volumeInfo"]["categories"]:
                c, created = Category.objects.update_or_create(name=category)
                c.books.add(b)
                c.save()

    return HttpResponse("")
