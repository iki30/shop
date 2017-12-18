from django.contrib.auth.forms import UserCreationForm, UserChangeForm, ReadOnlyPasswordHashField

from .models import Person


class PersonCreationForm(UserCreationForm):
    class Meta:
        model = Person
        fields = ('username', 'password', 'number',)

    def save(self, commit=True):
        user = super(PersonCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class PersonChangeForm(UserChangeForm):
    password = ReadOnlyPasswordHashField(label=("Password"),
                                         help_text=("Raw passwords are not stored, so there is no way to see "
                                                    "this user's password, but you can change the password "
                                                    "using <a href=\"password/\">this form</a>."))

    def save(self, commit=True):
        user = super(PersonChangeForm, self).save(commit=False)
        user.password = self.cleaned_data["password"]

        if commit:
            user.save()
        return user
