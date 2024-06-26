from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from base.cart import *
from base.models import *
from .forms import *
from .models import *


def loginView(req):
    if req.user.is_authenticated:
        return redirect('home')

    if req.method == 'POST':
        username = req.POST.get('username')
        password = req.POST.get('password')

        user = authenticate(req, username=username, password=password)

        if user is not None:
            login(req, user)
            if 'next' in req.POST:
                return redirect(req.POST.get('next'))

            else:
                return redirect('home')
        else:
            messages.error(req, 'Email ou Mots de passe incorrect!!!')
    context = {
        "login_page": "active",
        "title": 'Login'}
    return render(req, 'accounts/login.html', context)


@login_required(login_url='login')
def logoutUser(req):
    logout(req)
    return redirect('home')


@login_required(login_url='login')
def signupView(req):
    if req.user.is_authenticated:
        return redirect('home')

    form = SignupForm()
    if req.method == 'POST':
        form = SignupForm(req.POST)
        if form.is_valid():
            user = form.save()
            messages.success(req, "Votre compte vien d'être créé.")
            messages.add_message(
                req, messages.SUCCESS, 'Nous venons de vous envoyer un mail pour verifier votre compte')
            return redirect('login')

        # send_verification_email(req, user)

    context = {
        "signup_page":  "active",
        "title":  'signup',
        'form':  form,
    }
    return render(req, 'accounts/signup.html', context)


@login_required(login_url='login')
def users(req):
    users = CustomUser.objects.all()
    context = {
        'users': users,
    }
    return render(req, 'accounts/users.html', context)


@login_required(login_url='login')
def user_details(req, pk):
    curr_obj = get_object_or_404(CustomUser, id=pk)
    # 
    cart = Cart(req)
    cart_count = 0
    cart_count = len(cart)
    cart_items = cart.get_cart_items()
    total_price = cart.get_total_price()

    sales = Sale.objects.filter(client=curr_obj)

    context = {
        "profile_page":"active",
        "curr_obj": curr_obj,
        "cart_count": cart_count,
        "cart_items": cart_items,
        "total_price": total_price,
        "total_price": total_price,
        "sales": sales,
    }
    return render(req, 'accounts/user_details.html', context)


