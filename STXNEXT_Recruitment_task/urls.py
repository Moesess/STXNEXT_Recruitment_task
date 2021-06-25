from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from BooksAPI.views import BookListView

router = DefaultRouter()
router.register(r'books', BookListView)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]

