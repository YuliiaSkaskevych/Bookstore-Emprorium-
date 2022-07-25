from django.shortcuts import render
from django.db.models import Count, Avg, Max

from .models import Author, Book, Publisher, Store


def index(request):
    return render(request, 'catalog/index.html')


def books_list(request):
    """List of all books with authors"""
    avg_price = Book.objects.all().aggregate(Avg('price'))
    max_price = Book.objects.all().aggregate(Max('price'))
    book_list = Book.objects.select_related('author').all()
    books = []
    for book in book_list:
        books.append({'id': book.id, 'title': book.title, 'author': book.author.surname})
    return render(request, 'catalog/books.html', {'books': books, 'avg_price': avg_price, 'max_price': max_price, })


def book_info(request, id):
    """Information about entered book: author, store, publisher"""
    book = Book.objects.select_related('author').get(id=id)
    publisher = Publisher.objects.prefetch_related('book_set__publisher').filter(book=id)
    return render(
        request,
        'catalog/book_info.html',
        {'id': book.id,
         'title': book.title,
         'pages': book.pages,
         'price': book.price,
         'pubdate': book.pubdate,
         'author': book.author.surname,
         'author_id': book.author.id,
         'publisher': publisher,
         'publisher_id': book.publisher.name
         }
    )


def authors_list(request):
    """List of all authors"""
    authors = Author.objects.all()
    count = Author.objects.all().annotate(count=Count('surname'))
    return render(request, 'catalog/authors.html', {'authors': authors, 'count': count, })


def author_info(request, id):
    """Information abut just one author"""
    author = Author.objects.get(id=id)
    book_author = Book.objects.select_related('author').filter(author_id=id)
    return render(
        request,
        'catalog/author_info.html',
        {'id': author.id,
         'name': author.name,
         'surname': author.surname,
         'country': author.country,
         'books': book_author
         }
    )


def stores_list(request):
    """List of all stores with count of books"""
    store_list = Store.objects.select_related('publisher').all()
    stores = []
    for store in store_list:
        count = Book.objects.prefetch_related('publisher__store').filter(publisher__name=store.publisher.name).annotate\
            (count=Count('title'))
        stores.append({'id': store.id, 'name': store.name, 'address': store.address, 'publisher': store.publisher.name, 'count': count})
    return render(request, 'catalog/stores.html', {'stores': stores, })


def stores_info(request, id):
    store = Store.objects.prefetch_related('publisher').get(id=id)
    books = Book.objects.prefetch_related('publisher').filter(publisher__name=store.publisher.name)
    return render(request,
                  'catalog/stores_info.html',
                  {'id': store.id,
                   'name': store.name,
                   'address': store.address,
                   'publisher': store.publisher.name,
                   'books': books
                   }
                  )


def publishers_list(request):
    """List of all publishers"""
    publisher_list = Publisher.objects.select_related('store').all()
    pub_list = []
    for publisher in publisher_list:
        pub_list.append(
            {'name': publisher.name, 'store': publisher.store.name, 'year': publisher.year, 'pk': publisher.pk})
    return render(request, 'catalog/publishers.html', {'pub_list': pub_list, })


def publisher_info(request, pk):
    """Information about one publisher"""
    publisher = Publisher.objects.get(pk=pk)
    books = Book.objects.prefetch_related('publisher').filter(publisher__name=publisher.name)
    return render(request,
                  'catalog/publisher_info.html',
                  {'id': publisher.pk,
                   'name': publisher.name,
                   'store': publisher.store,
                   'year': publisher.year,
                   'books': books
                   }
                  )
