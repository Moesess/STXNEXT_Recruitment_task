import requests

from django.http import HttpResponse

from rest_framework import viewsets, mixins

from BooksAPI.models import Author, Book, Category
from BooksAPI.serializers import BookSerializer
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


def get_data(request):
    try:
        response = requests.get(
            f"https://www.googleapis.com/books/v1/volumes?q={request.POST['q']}").json()

        authors = []
        books = []
        ubooks = []
        categories = []

        # For each book in response from api
        for book in response["items"]:
            book_id = str(book["id"])
            title = str(book["volumeInfo"]["title"])
            published_date = str(book["volumeInfo"].get("publishedDate", ""))

            average_rating = float(book["volumeInfo"].get("averageRating", 0))
            ratings_count = int(book["volumeInfo"].get("ratingsCount", 0))
            thumbnail = str(book["volumeInfo"].get("imageLinks", {}).get("thumbnail", ""))

            b, created = Book.objects.update_or_create(
                book_id=book_id,
                defaults={
                    'title': title,
                    'published_date': published_date,
                    'average_rating': average_rating,
                    'ratings_count': ratings_count,
                    'thumbnail': thumbnail
                }
            )

            if created:
                books.append(b)
            else:
                ubooks.append(b)

            for author in book["volumeInfo"]["authors"]:
                a, created = Author.objects.get_or_create(name=author)
                a.books.add(b)
                a.save()

                if created:
                    authors.append(a)

            if "categories" in book["volumeInfo"]:
                for category in book["volumeInfo"]["categories"]:
                    c, created = Category.objects.get_or_create(name=category)
                    c.books.add(b)
                    c.save()

                    if created:
                        categories.append(c)

        res = f"Books created: {len(books)} {[str(x) for x in books]}:\n" \
              f"Authors created: {len(authors)}: {[str(x) for x in authors]}\n" \
              f"Categories created: {len(categories)}: {[str(x) for x in categories]}\n" \
              f"Books updated: {len(ubooks)} {[str(x) for x in ubooks]}:\n"

        return HttpResponse(res)

    except requests.exceptions.RequestException as err:
        raise SystemExit(err)
