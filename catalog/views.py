from django.shortcuts import render

from .models import Author, Book, Publisher, Store


def index(request):
    return render(request, 'catalog/index.html')


def books_list(request):
    books = Book.objects.all()
    return render(request, 'catalog/books.html', {'books': books, })


def authors_list(request):
    authors = Author.objects.all()
    return render(request, 'catalog/authors.html', {'authors': authors, })


def stores_list(request):
    stores = Store.objects.all()
    return render(request, 'catalog/stores.html', {'stores': stores, })


def publishers_list(request):
    publishers = Publisher.objects.all()
    return render(request, 'catalog/publishers.html', {'publishers': publishers, })
