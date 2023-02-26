from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.shortcuts import render, redirect


def index(request):
    context = {}
    return render(request, 'loan/index.html', context)


def login1(request):

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('index')
            else:
                return HttpResponse("Disabled Account")
        else:
            return HttpResponse("Username or password is incorrect")
    context = {}
    return render(request, 'loan/login.html', context)


def logout_user(request):
    logout(request)
    return redirect('login')