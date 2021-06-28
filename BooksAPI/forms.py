from django.forms import ModelForm

from BooksAPI import models


class BookForm(ModelForm):
    class Meta:
        model = models.Book
        fields = ['title', 'average_rating', 'ratings_count', 'thumbnail']

