import django_filters

from BooksAPI import models


class BookFilterSet(django_filters.FilterSet):
    """
    Filtering books by,
    title, if title contains request query param
    author, if authors in request are in Book model authors.
     Also it works with multiple authors, eg. "?author=Barton&author=Fisher"
    category, same as authors
    published_data, we can find book by year, month etc.
    book_id, ITS NOT THE SAME AS MODEL DATABASE ID. Special string that every book has.

    sorting is enabled, available fields are "published_date". Usage: "?sort=-published_date"
    """
    title = django_filters.CharFilter(
        lookup_expr='contains',
    )

    author = django_filters.AllValuesMultipleFilter(
        field_name='authors__name',
        lookup_expr='contains',
    )

    category = django_filters.AllValuesMultipleFilter(
        field_name='categories__name',
        lookup_expr='contains',
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

