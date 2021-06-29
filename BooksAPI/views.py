import requests

from django.http import HttpResponse

from rest_framework import viewsets, mixins

from BooksAPI.models import Author, Book, Category
from BooksAPI.serializers import BookSerializer
from BooksAPI.filtersets import BookFilterSet
from BooksAPI.forms import BookForm


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


def get_data(request):
    # Checking for connection
    try:
        response = requests.get(
            f"https://www.googleapis.com/books/v1/volumes?q={request.POST['q']}")
        response.raise_for_status()
        response = response.json()

    except requests.exceptions.RequestException as err:
        return HttpResponse(err)

    authors = []
    books = []
    updated_books = []
    categories = []

    # For each book in response from api
    for book in response["items"]:
        book_id = book["id"]
        title = book["volumeInfo"]["title"]
        published_date = book["volumeInfo"]["publishedDate"]

        average_rating = book["volumeInfo"].get("averageRating", 0)
        ratings_count = book["volumeInfo"].get("ratingsCount", 0)
        thumbnail = book["volumeInfo"].get("imageLinks", {}).get("thumbnail", "")

        # Validating data using custom form
        bform = BookForm(data={
            'title': title,
            'published_date': published_date,
            'average_rating': average_rating,
            'ratings_count': ratings_count,
            'thumbnail': thumbnail
        })

        if bform.is_valid():
            b, created = Book.objects.update_or_create(
                book_id=book_id,
                defaults={
                    'title': bform.cleaned_data['title'],
                    'published_date': bform.cleaned_data['published_date'],
                    'average_rating': bform.cleaned_data['average_rating'],
                    'ratings_count': bform.cleaned_data['ratings_count'],
                    'thumbnail': bform.cleaned_data['thumbnail']
                }
            )

            if created:
                books.append(b)
            else:
                updated_books.append(b)

            for author in book["volumeInfo"]["authors"]:
                a, created = Author.objects.get_or_create(name=author)
                a.books.add(b)
                a.save()

                if created:
                    authors.append(a)

            for category in book["volumeInfo"].get("categories", ""):
                c, created = Category.objects.get_or_create(name=category)
                c.books.add(b)
                c.save()

                if created:
                    categories.append(c)

    # Custom information
    res = f"<pre>Books created: {len(books)}: {[str(x) for x in books]}\n" \
          f"Authors created: {len(authors)}: {[str(x) for x in authors]}\n" \
          f"Categories created: {len(categories)}: {[str(x) for x in categories]}\n" \
          f"Books updated: {len(updated_books)}: {[str(x) for x in updated_books]}</pre>"

    return HttpResponse(res)
