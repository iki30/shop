import json

import requests_mock
from unittest.mock import patch, MagicMock, Mock
from django.shortcuts import redirect
from django.test import TestCase, Client

from datetime import date

from product.models import Person, Author, Book, PopularBooks


class ShopTestCase(TestCase):
    def setUp(self):
        self.card = 123
        self.number = 123
        self.cost = 123
        self.user = self.create_user('JohonTest', 'test_pass')
        self.author1 = Author.objects.create(name='FirstAuthor', last_name='Temp')
        self.author2 = Author.objects.create(name='SecondAuthor', last_name='Temp')
        self.book1 = Book.objects.create(title='Title',
                                         description='desc',
                                         cost=123)

        self.book1.author.add(self.author1)
        self.book2 = Book.objects.create(title='Title',
                                         description='desc',
                                         cost=self.cost)

        self.book2.author.add(self.author2)
        self.client = Client()
        self.client.force_login(self.user)

    def create_user(self, name, password):
        return Person.objects.create(username=name,
                                     password=password,
                                     card=self.card,
                                     number=self.number)


class PopularBooksShopTestCase(ShopTestCase):
    def setUp(self):
        super(PopularBooksShopTestCase, self).setUp()
        self.popular_book1 = PopularBooks.objects.create(book=self.book1)
        self.popular_book2 = PopularBooks.objects.create(book=self.book2)

    def test_shop(self):
        response = self.client.get(redirect('product:get_popular_books').url, content_type="application/json")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content),
                         {'books': [{'author': [{'last_name': self.author1.last_name,
                                                 'name': self.author1.name}],
                                     'cost': self.cost,
                                     'description': 'desc',
                                     'title': 'Title'},
                                    {'author': [{'last_name': self.author2.last_name, 'name': self.author2.name}],
                                     'cost': self.cost,
                                     'description': 'desc',
                                     'title': 'Title'}]}
                         )


class ListBooksShopTestCase(ShopTestCase):
    def test_shop(self):
        self.user.purchase_book.add(self.book1)
        response = self.client.get(redirect('product:get_list_books').url, content_type="application/json")
        self.assertEqual(json.loads(response.content)['books'][0]['is_buy'], True)

    def test_shop_logout(self):
        self.client.logout()
        response = self.client.get(redirect('product:get_list_books').url, content_type="application/json")
        self.assertEqual(json.loads(response.content)['books'][0].get('is_buy', None), None)


class PurchaseBooksShopTestCase(ShopTestCase):
    def test_shop(self):
        self.user.purchase_book.add(self.book1)
        self.user.purchase_book.add(self.book2)
        response = self.client.get(redirect('product:get_purchased_books').url, content_type="application/json")
        self.assertEqual(len(json.loads(response.content)['books']), 2)

    def test_shop_logout(self):
        self.client.logout()
        response = self.client.get(redirect('product:get_purchased_books').url, content_type="application/json")
        self.assertEqual(response.status_code, 302)


class InfoBookShopTestCase(ShopTestCase):
    def test_shop(self):
        self.user.purchase_book.add(self.book1)
        response1 = self.client.get(redirect('product:get_info_book', 1).url, content_type="application/json")
        self.assertEqual(json.loads(response1.content)['url_for_download'],
                         redirect('product:buy_book', 1).url)
        response2 = self.client.get(redirect('product:get_info_book', 2).url, content_type="application/json")
        self.assertEqual(json.loads(response2.content).get('url_for_download', None), None)

    def test_shop_logout(self):
        self.client.logout()
        response = self.client.get(redirect('product:get_info_book', 1).url, content_type="application/json")
        self.assertEqual(response.status_code, 404)


class BuyBookShopTestCase(ShopTestCase):
    @patch('product.views.interact_with_card')
    def test_shop(self, interact_with_card):
        interact_with_card.return_value = True
        response1 = self.client.get(redirect('product:buy_book', 1).url, content_type="application/json")
        self.assertEqual(json.loads(response1.content)['success'], True)

    @patch('product.views.interact_with_card')
    def test_shop_not_pay(self, interact_with_card):
        interact_with_card.return_value = False
        response1 = self.client.get(redirect('product:buy_book', 1).url, content_type="application/json")
        self.assertEqual(json.loads(response1.content)['success'], False)
