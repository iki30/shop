from django.conf.urls import url

from . import views

app_name = 'product'
urlpatterns = [
    url(regex=r'^$', view=views.index, name='index'),
    url(
        regex=r'^book_info/(?P<id>[0-9]+)$',
        view=views.book_info,
        name='book_info'
    ),
    url(regex=r'^list_book/', view=views.list_book, name='list_book'),
    url(
        regex=r'^buy_book/(?P<id>[0-9]+)$',
        view=views.buy_book,
        name='buy_book'
    ),
    url(
        regex=r'^get_purchased_books/$',
        view=views.get_purchased_books,
        name='get_purchased_books'
    ),
    url(
        regex=r'^get_info_book/(?P<id>[0-9]+)$',
        view=views.get_info_book,
        name='get_info_book'
    ),
    url(
        regex=r'^get_popular_books/$',
        view=views.get_popular_books,
        name='get_popular_books'
    ),
    url(
        regex=r'^get_list_books/$',
        view=views.get_list_books,
        name='get_list_books'
    ),
]