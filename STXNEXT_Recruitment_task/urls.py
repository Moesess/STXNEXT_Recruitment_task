from django.contrib import admin
from django.urls import include, path

from rest_framework.routers import DefaultRouter

from BooksAPI import views

router = DefaultRouter()
router.register(r'books', views.BookListView)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('db/', views.get_data, name="post_data")
]

