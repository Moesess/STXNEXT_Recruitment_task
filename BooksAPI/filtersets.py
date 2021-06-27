import operator

import django_filters
from django.db.models import Q
from functools import reduce

from BooksAPI import models


class BookFilterSet(django_filters.FilterSet):
    """
    Filtering books by,
    title, if title contains request query param
    author, if authors in request are in Book model authors.
     Also it works with multiple authors, eg. "?author=Barton,Fisher"
    category, same as authors
    published_data, we can find book by year, month etc.

    sorting is enabled, available fields are "published_date". Usage: "?sort=-published_date"
    """
    title = django_filters.CharFilter(
        lookup_expr='contains',
    )

    author = django_filters.CharFilter(
        field_name='authors__name',
        lookup_expr='contains',
        method="custom_filter"
    )

    category = django_filters.CharFilter(
        field_name='categories__name',
        lookup_expr='contains',
        method="custom_filter"
    )

    published_date = django_filters.CharFilter(
        lookup_expr='contains'
    )

    sort = django_filters.OrderingFilter(
        fields=(
            'published_date',
        )
    )

    class Meta:
        model = models.Book
        fields = ('title', 'book_id', 'published_date', 'author', 'category')

    def custom_filter(self, queryset, name, value):
        """
        Custom filter method for categories
        :param queryset: original queryset
        :param name: request query param key
        :param value: request query param value
        :return: queryset filtered by this value, using custom query. Looking for every author/category in value
        """

        if value is None:
            return queryset

        value = value.split(',')
        name += "__contains"

        queryset = models.Book.objects.filter(reduce(operator.or_, (Q(**{name: x}) for x in value)))
        return queryset
