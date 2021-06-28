from django.forms import ModelForm

from BooksAPI import models


class BookForm(ModelForm):
    """
    Book form, used for validating data in get_data function
    """
    class Meta:
        model = models.Book
        fields = ['title', 'average_rating', 'ratings_count', 'thumbnail']

