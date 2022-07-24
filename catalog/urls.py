from django.urls import path

from .views import authors_list, books_list, index, publishers_list, stores_list

app_name = 'catalog'
urlpatterns = [
    path('', index, name="index"),
    path('books/', books_list, name='books'),
    path('authors/', authors_list, name="authors"),
    path('stores/', stores_list, name="stores"),
    path('publishers/', publishers_list, name='publishers')
]
