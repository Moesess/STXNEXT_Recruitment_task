from django.views.generic import View
from rest_framework import viewsets, mixins
from rest_framework.views import APIView

from .models import Book
from .serializers import BookSerializer


class BookListView(mixins.ListModelMixin,
                   viewsets.GenericViewSet):
    """
    List of all Books we have in database
    """

    queryset = Book.objects.all()
    serializer_class = BookSerializer


#class LoadView(View):
