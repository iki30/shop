from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from product.models import PopularBooks
from .models import Author, Book, Person
from .forms import PersonCreationForm, PersonChangeForm


class PersonAdmin(UserAdmin):
    form = PersonChangeForm
    add_form = PersonCreationForm

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'number', 'purchase_book', 'card')}
         ),
    )


admin.site.register(Person, PersonAdmin)
admin.site.register(Author)
admin.site.register(Book)
admin.site.register(PopularBooks)
