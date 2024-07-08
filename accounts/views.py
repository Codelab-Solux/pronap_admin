from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.db.models import Sum

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


# ------------------------------------------------- Staff -------------------------------------------------

@login_required(login_url='login')
def staff(req):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')

    context = {
        "staff": "active",
        'title': 'Personnel',
    }
    return render(req, 'accounts/staff.html', context)


@login_required(login_url='login')
def staff_list(req):
    staff = CustomUser.objects.all().order_by('last_name')
    context = {
        'staff': staff,
    }
    return render(req, 'accounts/partials/staff_list.html', context)


@login_required(login_url='login')
def staff_grid(req):
    personel = CustomUser.objects.all().order_by('last_name')
    context = {
        "personel": personel,
    }
    return render(req, 'accounts/partials/staff_grid.html', context)



@login_required(login_url='login')
def staff_details(req, pk):
    user = req.user
    curr_obj = get_object_or_404(CustomUser, id=pk)
    is_self = True if user == curr_obj else False

    sales = Sale.objects.filter(initiator=curr_obj)
    sales_aggregate = sales.aggregate(totals=Sum('total'))['totals'] or 0
    transactions = Transaction.objects.filter(initiator=curr_obj)
    trans_aggregate = transactions.aggregate(totals=Sum('amount'))['totals'] or 0
    stocks = StockInput.objects.filter(initiator=curr_obj)
    # stocks_aggregate = stocks.aggregate(totals=Sum('total'))['totals'] or 0

    context = {
        "staff": "active",
        'title': 'Staff',
        'curr_obj': curr_obj,
        'is_self': is_self,
        'sales': sales,
        'sales_aggregate': sales_aggregate,
        'transactions': transactions,
        'trans_aggregate': trans_aggregate,
        'stocks': stocks,
    }
    return render(req, 'accounts/staff_details.html', context)


@login_required(login_url='login')
def create_staff(req):
    user = req.user
    if not user.role.sec_level >= 2:
        messages.info(req, "Access denied!!!")
        return redirect('home')

    form = SignupForm()
    if req.method == 'POST':
        form = SignupForm(req.POST)
        if form.is_valid():
            form.save()
        messages.success = 'Nouveau membre du personnel ajouté'
        return HttpResponse(status=204, headers={'HX-Trigger': 'db_changed'})
    else:
        return render(req, 'form.html', context={'form': form, 'form_title': 'Nouveau  membre du personnel'})


@login_required(login_url='login')
def edit_staff(req,pk):
    user = req.user
    curr_obj = get_object_or_404(CustomUser,id=pk)

    if user != curr_obj and user.role.sec_level < 2:
        messages.info(req, "Access denied!!!")
        return redirect('home')
        
    if req.method == 'POST':
        form = EditUserForm(req.POST, instance=curr_obj, user=user)
        if form.is_valid():
            form.save()
            messages.success(req, 'Membre du personnel modifié')
            return HttpResponse(status=204, headers={'HX-Trigger': 'db_changed'})
    else:
        form = EditUserForm(instance=curr_obj, user=user)
    return render(req, 'form.html', context={'curr_obj': curr_obj, 'form': form, 'form_title': 'Modifier ce membre du personnel'})
    

@login_required(login_url='login')
def edit_staff_profile(req, pk):
    user = req.user
    if user.role.sec_level < 2:
        messages.info(req, "Access denied!!!")
        return redirect('home')
        
    curr_obj = get_object_or_404(Profile, id=pk)

    form = ProfileForm(instance=curr_obj, user=user)
    if req.method == 'POST':
        form = ProfileForm(req.POST, instance=curr_obj, user=user)
        if form.is_valid():
            form.save()
        messages.success = 'Profile modifié'
        return HttpResponse(status=204, headers={'HX-Trigger': 'db_changed'})
    else:
        return render(req, 'form.html', context={'curr_obj':curr_obj ,'form': form, 'form_title': 'Modifier ce profile'})
