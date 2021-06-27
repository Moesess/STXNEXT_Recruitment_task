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
        book_id = book["id"]
        title = book["volumeInfo"]["title"]
        published_date = str(book["volumeInfo"]["publishedDate"])

        average_rating = 0
        ratings_count = 0
        thumbnail = ""

        # checking if fields exist
        if "averageRating" in book["volumeInfo"]:
            average_rating = book["volumeInfo"]["averageRating"]

        if "ratingsCount" in book["volumeInfo"]:
            ratings_count = book["volumeInfo"]["ratingsCount"]

        if "imageLinks" in book["volumeInfo"]:
            thumbnail = book["volumeInfo"]["imageLinks"]["thumbnail"]

        Book.objects.get_or_create(
            book_id=book_id,
            title=title,
            published_date=published_date,
            average_rating=average_rating,
            ratings_count=ratings_count,
            thumbnail=thumbnail
        )

        b = Book.objects.get(book_id=book_id)

        authors = book["volumeInfo"]["authors"]
        for author in authors:
            Author.objects.get_or_create(name=author)
            a = Author.objects.get(name=author)
            a.books.add(b)
            a.save()

        if "categories" in book["volumeInfo"]:
            categories = book["volumeInfo"]["categories"]
            for category in categories:
                Category.objects.get_or_create(name=category)
                c = Category.objects.get(name=category)
                c.books.add(b)
                c.save()

    return HttpResponse("")
