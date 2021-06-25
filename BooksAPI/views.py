from rest_framework import viewsets

from .models import Book
from .serializers import BookSerializer


class BookListView(viewsets.ModelViewSet):
    """
    List of all Books we have in database
    """

    queryset = Book.objects.all()
    serializer_class = BookSerializer
