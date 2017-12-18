from django.contrib import auth
from django.contrib.auth import logout, authenticate
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect


def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/')


@csrf_exempt
def login(request):
    if request.POST:
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        person = authenticate(username=username, password=password)
        if person:
            auth.login(request, person)

            return HttpResponseRedirect('/')
        else:
            args = {'login_error': "Проверьте имя или пароль"}
            return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/')
