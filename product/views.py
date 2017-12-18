from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.urls import reverse

from product.models import PopularBooks, Book, Person, Rating


def index(request):
    return render_to_response(
        'home.html',
        {
            'user': request.user,
            'popular_books': PopularBooks.objects.all()
        }
    )


def book_info(request, id):
    book = get_object_or_404(Book, id=id)
    return render_to_response(
        'shop/book_info.html',
        {
            'book': book,
            'user': request.user,
        }
    )


@login_required
def list_book(request):
    return render_to_response(
        'shop/list_book.html',
        {
            'user': request.user,
            'books': Book.objects.all()
        }
    )


def interact_with_card(card, cost):
    return True


@login_required
def buy_book(request, id):
    book = get_object_or_404(Book, id=id)
    person = get_object_or_404(Person, id=auth.get_user(request).id)
    is_success = interact_with_card(person.card, book.cost)

    if is_success:
        person.purchase_book.add(book)
        person.save()
        rating = Rating.objects.get_or_create(book=book)[0]
        rating.number_of_purchases = rating.number_of_purchases + 1
        rating.save()
        return JsonResponse({'success': True})

    return JsonResponse({'success': False})


@login_required
def get_purchased_books(request):
    person = get_object_or_404(Person, id=auth.get_user(request).id)
    books = []
    for book in person.purchase_book.all():
        author = []
        for ppl in book.author.all():
            author.append({
                'name': ppl.name,
                'last_name': ppl.last_name,
            })

        books.append({
            'title': book.title,
            'description': book.description,
            'cost': book.cost,
            'author': author,
        })
    return JsonResponse({'books': books})


def get_info_book(request, id):
    book = get_object_or_404(Book, id=id)
    person = get_object_or_404(Person, id=auth.get_user(request).id)
    data = {}
    if person:
        purchase_book = person.purchase_book.filter(id=book.id)
        if purchase_book:
            data['url_for_download'] = reverse('product:buy_book', args=[purchase_book[0].id])
    data['title'] = book.title
    data['description'] = book.description
    data['cost'] = book.cost
    author = []
    for ppl in book.author.all():
        author.append({
            'name': ppl.name,
            'last_name': ppl.last_name,
        })
    data['author'] = author
    return JsonResponse(data)


def get_popular_books(request):
    books = []
    for popular in PopularBooks.objects.all():
        author = []
        for ppl in popular.book.author.all():
            author.append({
                'name': ppl.name,
                'last_name': ppl.last_name,
            })

        books.append({
            'title': popular.book.title,
            'description': popular.book.description,
            'cost': popular.book.cost,
            'author': author,
        })
    return JsonResponse({'books': books})


def get_list_books(request):
    books = []
    book_request = Book.objects.all()
    filter_author = request.GET.getlist('author')
    if filter_author:
        book_request = book_request.filter(author__last_name=filter_author[0])
    for book in book_request:
        author = []
        for ppl in book.author.all():
            author.append({
                'name': ppl.name,
                'last_name': ppl.last_name,
            })

        element = {
            'title': book.title,
            'description': book.description,
            'cost': book.cost,
            'author': author,
        }
        if auth.get_user(request).id:
            person = get_object_or_404(Person, id=auth.get_user(request).id)
            if person.purchase_book.filter(id=book.id):
                element['is_buy'] = True

        books.append(element)
    return JsonResponse({'books': books})
