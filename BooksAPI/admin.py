from django.contrib import admin

from .models import Author, Book, Category


# Register your models here.
class BookAdmin(admin.ModelAdmin):
    model = Book
    list_display = ('id', 'title', 'get_authors', 'published_date', 'get_categories', 'average_rating', 'ratings_count', 'thumbnail')

    def get_authors(self, obj):
        return [a.name for a in obj.authors.all()]

    def get_categories(self, obj):
        return [c.name for c in obj.categories.all()]


class AuthorAdmin(admin.ModelAdmin):
    model = Author
    list_display = ('id', 'name',)


class CategoryAdmin(admin.ModelAdmin):
    model = Category
    list_display = ('id', 'name',)


admin.site.register(Book, BookAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Category, CategoryAdmin)
