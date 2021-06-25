from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from BooksAPI import views

urlpatterns = [
    path('books/', views.BookListView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
