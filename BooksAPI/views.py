import requests

from django.http import HttpResponse
from rest_framework import viewsets, mixins

from .models import Author, Book, Category
from .serializers import BookSerializer


class BookListView(mixins.ListModelMixin,
                   viewsets.GenericViewSet):
    """
    List of all Books we have in database
    """

    queryset = Book.objects.all()
    serializer_class = BookSerializer


def get_data(request):
    response = requests.get("https://www.googleapis.com/books/v1/volumes?q=Hobbit").json()
    # For each book in response from api
    for book in response["items"]:
        book_id = book["id"]
        title = book["volumeInfo"]["title"]
        published_date = str(book["volumeInfo"]["publishedDate"])
        pd = published_date.split("-")

        # handling different data formats
        if len(pd) == 1:
            published_date = f'{pd[0]}-01-01'
        elif len(pd) == 2:
            published_date = f'{pd[0]}-{pd[1]}-01'
        else:
            published_date = f'{pd[0]}-{pd[1]}-{pd[2]}'

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
