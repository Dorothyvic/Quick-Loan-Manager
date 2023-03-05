import uuid

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect

from .emails import send_email
from .forms import CustomersForm
from .models import User, Customers


def index(request):
    if request.user.is_authenticated:
        customers_count = Customers.objects.count()
        context = {'customers_count': customers_count}
        return render(request, 'loan/index.html', context)
    else:
        return redirect("login")


def login1(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return redirect('index')
            else:
                return HttpResponse("Disabled Account")
        else:
            return HttpResponse("Username or password is incorrect")
    else:
        context = {}
        return render(request, 'loan/login.html', context)


def logout_user(request):
    logout(request)
    return redirect('login')


def send_reset(request):
    if request.method == "POST":
        email = request.POST['email']
        token = uuid.uuid4()

        try:
            user = User.objects.get(email=email)
            user.reset_token = token
            user.save()
        except:
            return HttpResponse("Email does not exist")

        link = "http://127.0.0.1:8000/reset_password/%s/%s/" % (user.id, token)
        message = "Dear %s, \n Your password reset link is %s." % (email.split("@")[0], link)
        send_email(message, email, email.split("@")[0], "Password reset Link")
        return redirect('login')
    else:
        return render(request, "loan/send_reset.html")


def new_password(request, pk, token):
    try:
        user = User.objects.get(id=pk)
    except:
        return HttpResponse("Invalid URL")

    if user.reset_token == token:
        if request.method == "POST":
            password1 = request.POST['password1']
            password2 = request.POST['password2']

            if not password1 == password2:
                return HttpResponse("Passwords do not match")

            user.set_password(password2)

            user.reset_token = None
            user.save()

            logout(request)
            return redirect("index")

        else:
            return render(request, "loan/new_password.html", {"user_id": pk, "token": token})
    else:
        return HttpResponse("Invalid URL")


def register(request):
    if request.method == 'POST':
        name = request.POST['name']
        gender = request.POST['gender']
        phone = request.POST['phone']
        email = request.POST['email']
        place_of_work = request.POST['work']
        next_of_kin = request.POST['kin']

        email_check = Customers.objects.filter(email=email)
        if email_check.count() > 0:
            messages.error(request, "Email already exists")
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))

        phone_check = Customers.objects.filter(phone=phone)
        if phone_check.count() > 0:
            messages.error(request, "Phone number already exists")
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))

        Customers.objects.create(name=name, gender=gender, phone=phone,
                                 email=email, place_of_work=place_of_work, next_of_kin=next_of_kin)

        messages.success(request, "Customer successfully added")
        return redirect('customers')
        # return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
    else:
        context = {}
        return render(request, 'loan/create_customer.html', context)


def customers(request):
    customers = Customers.objects.all()
    context = {'customers': customers}
    return render(request, 'loan/customers.html', context)


def update_customer(request, pk):
    customer = Customers.objects.get(id=pk)
    if request.method == 'POST':
        name = request.POST['name']
        gender = request.POST['gender']
        phone = request.POST['phone']
        email = request.POST['email']
        place_of_work = request.POST['work']
        next_of_kin = request.POST['kin']

        customer.name = name
        customer.gender = gender
        customer.phone = phone
        customer.email = email
        customer.place_of_work = place_of_work
        customer.next_of_kin = next_of_kin
        customer.save()

        messages.success(request, "Customer successfully updated")
        return redirect('customers')

    else:
        context = {'customer': customer}
        return render(request, 'loan/update_customer.html', context)


def delete_customer(request, pk):
    customer = Customers.objects.get(id=pk)
    if request.method == 'POST':
        customer.delete()
        return redirect('customers')
    context = {'customer': customer}
    return render(request, 'loan/delete_customer.html', context)