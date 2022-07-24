from django.contrib import admin

from .models import Author, Book, Publisher, Store


class AuthorInlineModelAdmin(admin.TabularInline):
    model = Author


class BookInlineModelAdmin(admin.TabularInline):
    model = Book


class PublisherInlineModelAdmin(admin.TabularInline):
    model = Publisher


@admin.register(Author)
class AuthorModelAdmin(admin.ModelAdmin):
    list_display = ["name", "surname", "country"]
    fields = ['name', 'surname', "country"]
    search_fields = ["surname"]
    date_hierarchy = "surname"
    inlines = [AuthorInlineModelAdmin, BookInlineModelAdmin]


@admin.register(Book)
class BookModelAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'author', 'publisher']
    fields = ['title', 'price', 'author', 'publisher', ('price', 'pages', 'pubdate')]
    raw_id_fields = ['author', ]
    date_hierarchy = "pubdate"
    list_filter = ['price', 'pubdate']
    filter_vertical = ["pages"]
    search_fields = ["author", "title"]
    inlines = [AuthorInlineModelAdmin, PublisherInlineModelAdmin]


@admin.register(Store)
class StoreModelAdmin(admin.ModelAdmin):
    list_display = ["name", "address"]
    fields = ['name', 'address']
    search_fields = ["name", "address"]
    date_hierarchy = "name"
    inlines = [PublisherInlineModelAdmin, BookInlineModelAdmin]
    filter_horizontal = ["address"]
