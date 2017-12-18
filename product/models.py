from django.db import models
from django.contrib.auth.models import User, UserManager


class Author(models.Model):
    class Meta:
        verbose_name = 'Author'
        verbose_name_plural = 'Authors'

    name = models.CharField(max_length=65)
    last_name = models.CharField(max_length=65)
    image = models.ImageField(upload_to='images', null=True, blank=True)

    def __str__(self):
        return self.last_name


class Book(models.Model):
    class Meta:
        verbose_name = 'Book'
        verbose_name_plural = 'Books'

    author = models.ManyToManyField(Author)
    image = models.ImageField(upload_to='images', null=True, blank=True)
    title = models.CharField(max_length=127)
    description = models.TextField()
    cost = models.IntegerField(default=0)

    def __str__(self):
        return self.title


class Person(User):
    class Meta:
        verbose_name = 'Person'
        verbose_name_plural = 'Persons'

    number = models.CharField(max_length=65)
    purchase_book = models.ManyToManyField(Book, blank=True)
    card = models.IntegerField()

    objects = UserManager()

    def __str__(self):
        return self.username


class Rating(models.Model):
    class Meta:
        verbose_name = 'Rating'
        verbose_name_plural = 'Rating'

    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    number_of_purchases = models.IntegerField(default=0)

    def __str__(self):
        return 'Rating: ' + self.book.title


class PopularBooks(models.Model):
    class Meta:
        verbose_name = 'PopularBooks'
        verbose_name_plural = 'PopularBooks'

    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    def __str__(self):
        return self.book.title
