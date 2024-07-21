import logging
from django.contrib import messages
from django.apps import apps
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Q
from django.db.models import Sum
from django.template.loader import render_to_string

from .models import *
from .forms import *
from .views import *
from .cart import Cart

logger = logging.getLogger(__name__) 

@login_required(login_url='login')
def home(req):
    context = {
        "home": "active",
        'title': 'Accueil',
    }
    return render(req, 'base/index.html', context)



# ------------------------------------------------- Entity Types -------------------------------------------------

@login_required(login_url='login')
def create_entity_type(req):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')

    form = EntityTypeForm()
    if req.method == 'POST':
        form = EntityTypeForm(req.POST)
        if user.role.sec_level < 2:
            form.instance.store = user.profile.store
            form.instance.initiator = user
        if form.is_valid():
            form.save()
        return HttpResponse(status=204, headers={'HX-Trigger': 'db_changed'})
    else:
        return render(req, 'form.html', context={'form': form, 'form_title': 'Nouveau type'})


@login_required(login_url='login')
def edit_entity_type(req, pk):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')
    curr_obj = get_object_or_404(EntityType, id=pk)

    form = EntityTypeForm(instance=curr_obj)
    if req.method == 'POST':
        form = EntityTypeForm(req.POST,  instance=curr_obj)
        if form.is_valid():
            form.save()
        messages.success = 'Type modifié'
        return HttpResponse(status=204, headers={'HX-Trigger': 'db_changed'})
    else:
        return render(req, 'form.html', context={'curr_obj': curr_obj, 'form': form, 'form_title': 'Modifier ce type'})


def entity_types_list(req):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')


    entity_types = EntityType.objects.all().order_by('name')

    context = {
        'entity_types': entity_types,
    }
    return render(req, 'base/parameters/entity_types_list.html', context)


# ------------------------------------------------- Stores -------------------------------------------------
# stores parameters ---------------------------------------
@login_required(login_url='login')
def stores_list(req):
    stores = Store.objects.all().order_by('name')
    context = {
        'stores': stores,
    }
    return render(req, 'base/parameters/stores_list.html', context)


# stores views ---------------------------------------
@login_required(login_url='login')
def stores(req):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')
    
    personnel = CustomUser.objects.all()

    context = {
        "stores": "active",
        'title': 'Boutiques',
        'personnel': personnel,
    }
    return render(req, 'base/stores/index.html', context)


@login_required(login_url='login')
def store_details(req, pk):
    staff = CustomUser.objects.all()
    curr_obj = get_object_or_404(Store, id=pk)
    initiators = CustomUser.objects.all().order_by('last_name')
    transactions = Transaction.objects.filter(store=curr_obj).order_by('-timestamp')
    # -------------------------
    credits = transactions.filter(type='credit')
    credits_aggregate = credits.aggregate(totals=Sum('amount'))['totals'] or 0
    csh_cred = transactions.filter(type='credit', cashdesk__type='cash', cashdesk__carrier=None)
    cash_credits = csh_cred.aggregate(totals=Sum('amount'))['totals'] or 0
    mv_cred = transactions.filter(type='credit', cashdesk__type='mobile', cashdesk__carrier='moov')
    moov_credits = mv_cred.aggregate(totals=Sum('amount'))['totals'] or 0
    tm_cred = transactions.filter(type='credit', cashdesk__type='mobile', cashdesk__carrier='togocom')
    tmoney_credits =tm_cred.aggregate(totals=Sum('amount'))['totals'] or 0
    # -------------------------
    debits = transactions.filter(type='debit')
    debits_aggregate = debits.aggregate(totals=Sum('amount'))['totals'] or 0
    csh_deb = transactions.filter(type='debit', cashdesk__type='cash', cashdesk__carrier=None)
    cash_debits = csh_deb.aggregate(totals=Sum('amount'))['totals'] or 0
    mv_deb = transactions.filter(type='debit', cashdesk__type='mobile', cashdesk__carrier='moov')
    moov_debits =mv_deb.aggregate(totals=Sum('amount'))['totals'] or 0
    tm_deb= transactions.filter(type='debit', cashdesk__type='mobile', cashdesk__carrier='togocom')
    tmoney_debits = tm_deb.aggregate(totals=Sum('amount'))['totals'] or 0
    # -------------------------
    balance = credits_aggregate - debits_aggregate
    cash_balance = cash_credits - cash_debits
    moov_balance = moov_credits - moov_debits
    tmoney_balance = tmoney_credits - tmoney_debits

    context = {
        "stores": "active",
        'title': f'Boutique-{curr_obj.name}',
        'staff': staff,
        'curr_obj': curr_obj,
        'initiators': initiators,
        # --------------------
        'credits': credits,
        'cash_credits': cash_credits,
        'moov_credits': moov_credits,
        'tmoney_credits': tmoney_credits,
        'credits_aggregate': credits_aggregate,
        # --------------------
        'debits': debits,
        'cash_debits': cash_debits,
        'moov_debits': moov_debits,
        'tmoney_debits': tmoney_debits,
        'debits_aggregate': debits_aggregate,
        # --------------------
        'balance': balance,
        'cash_balance': cash_balance,
        'moov_balance': moov_balance,
        'tmoney_balance': tmoney_balance,
    }
    return render(req, 'base/stores/store_details.html', context)


@login_required(login_url='login')
def create_store(req):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')

    form = StoreForm()
    if req.method == 'POST':
        form = StoreForm(req.POST, req.FILES)
        if form.is_valid():
            form.save()
        messages.success = 'Produit créé'
        return HttpResponse(status=204, headers={'HX-Trigger': 'db_changed'})
    else:
        return render(req, 'form.html', context={'form': form, 'form_title': 'Créer un produit', })


@login_required(login_url='login')
def edit_store(req, pk):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')
    curr_obj = get_object_or_404(Store, id=pk)

    form = StoreForm(instance=curr_obj)
    if req.method == 'POST':
        form = StoreForm(req.POST, req.FILES, instance=curr_obj)
        if form.is_valid():
            form.save()
        messages.success = 'Boutique modifié'
        return HttpResponse(status=204, headers={'HX-Trigger': 'db_changed'})
    else:
        return render(req, 'form.html', context={'curr_obj':curr_obj ,'form': form, 'form_title': 'Modifier cette boutique'})


# ------------------------------------------------- Lots -------------------------------------------------

def lots_list(req):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')

    lots = Lot.objects.all().order_by('name')

    context = {
        'lots': lots,
    }
    return render(req, 'base/parameters/lots_list.html', context)


def lot_details(req, pk):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')

    curr_obj = get_object_or_404(Lot, id=pk)
    products = ProductStock.objects.filter(
        lot=curr_obj).order_by('product__name')

    context = {
        'parameters':'active',
        'title': 'Details du lots',
        'curr_obj': curr_obj,
        'products': products,
    }
    return render(req, 'base/parameters/lot_details.html', context)


@login_required(login_url='login')
def create_lot(req):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')

    form = LotForm()
    if req.method == 'POST':
        form = LotForm(req.POST)
        if user.role.sec_level < 2:
            form.instance.store = user.profile.store
            form.instance.initiator = user
        if form.is_valid():
            form.save()
        return HttpResponse(status=204, headers={'HX-Trigger': 'db_changed'})
    else:
        return render(req, 'form.html', context={'form': form, 'form_title': 'Nouveau lot'})


@login_required(login_url='login')
def edit_lot(req, pk):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')
    curr_obj = get_object_or_404(Lot, id=pk)

    form = LotForm(instance=curr_obj)
    if req.method == 'POST':
        form = LotForm(req.POST,  instance=curr_obj)
        if form.is_valid():
            form.save()
        messages.success = 'Paiement modifié'
        return HttpResponse(status=204, headers={'HX-Trigger': 'db_changed'})
    else:
        return render(req, 'form.html', context={'curr_obj': curr_obj, 'form': form, 'form_title': 'Modifier ce lot'})



# ------------------------------------------------- Products -------------------------------------------------
@login_required(login_url='login')
def products(req):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')
    
    categories = Category.objects.all().order_by('name')
    families = Family.objects.all().order_by('name')
    stores = Store.objects.all().order_by('name')
    products = Product.objects.all().order_by('name')
    context = {
        "products": "active",
        'title': 'Produits',
        'categories': categories,
        'families': families,
        'stores': stores,
        'products': products,
    }
    return render(req, 'base/products/index.html', context)

# products parameters-----------------------------
@login_required(login_url='login')
def product_details(req, pk):
    curr_obj = Product.objects.get(id=pk)
    context = {
        "products_page": "active",
        'title': 'Products',
        'curr_obj': curr_obj,
    }
    return render(req, 'base/parameters/product_details.html', context)

@login_required(login_url='login')
def create_product(req):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')

    form = ProductForm()
    if req.method == 'POST':
        form = ProductForm(req.POST)
        if form.is_valid():
            form.save()
        messages.success = 'Produit créé'
        return HttpResponse(status=204, headers={'HX-Trigger': 'db_changed'})
    else:
        return render(req, 'form.html', context={'form': form, 'form_title': 'Créer un produit', })

@login_required(login_url='login')
def edit_product(req, pk):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')

    curr_obj = get_object_or_404(Product, id=pk)
    form = ProductForm(instance=curr_obj)

    if req.method == 'POST':
        form = ProductForm(req.POST, instance=curr_obj)
        if form.is_valid():
            form.save()
            
            return HttpResponse(status=204, headers={'HX-Trigger': 'db_changed'})
    else:
        return render(req, 'form.html', context={'curr_obj':curr_obj ,'form': form, 'form_title': 'Modifier ce produit'})

@login_required(login_url='login')
def products_list(req):
    products = Product.objects.all().order_by('name')
    context = {
        'products': products,
    }
    return render(req, 'base/parameters/products_list.html', context)

@login_required(login_url='login')
def products_grid(req):
    products = Product.objects.all().order_by('name')
    context = {
        'products': products,
    }
    return render(req, 'base/parameters/products_grid.html', context)

@login_required(login_url='login')
def filter_products(req):
    name_query = req.POST.get('name')
    brand_query = req.POST.get('brand')
    quantity_query = req.POST.get('quantity')
    category_query = req.POST.get('category')
    family_query = req.POST.get('family')
    promo_query = req.POST.get('is_promoted')
    exp_query = req.POST.get('is_expirable')

    base_query = Product.objects.all().order_by('name')

    if name_query:
        base_query = base_query.filter(name=name_query)
    if brand_query:
        base_query = base_query.filter(brand=brand_query)
    if quantity_query:
        base_query = base_query.filter(quantity=quantity_query)
    if category_query:
        base_query = base_query.filter(category__id=category_query)
    if family_query:
        base_query = base_query.filter(family__id=family_query)
    if exp_query:
        base_query = base_query.filter(is_expirable=exp_query)
    if promo_query:
        base_query = base_query.filter(is_promoted=promo_query)

    products = base_query

    context = {"products": products}

    return render(req, 'base/parameters/products_list.html', context)


# products stocks-----------------------------

@login_required(login_url='login')
def product_stocks(req):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')
    
    categories = Category.objects.all().order_by('name')
    families = Family.objects.all().order_by('name')
    stores = Store.objects.all().order_by('name')
    context = {
        "product_stocks": "active",
        'title': 'Produits en stock',
        'categories': categories,
        'families': families,
        'stores': stores,
    }
    return render(req, 'base/products/stocks.html', context)


@login_required(login_url='login')
def prod_stock_list(req):
    products = ProductStock.objects.all().order_by('product__name')
    context = {
        'products': products,
    }
    return render(req, 'base/products/prod_stock_list.html', context)


@login_required(login_url='login')
def prod_stocks(req, pk):
    products = ProductStock.objects.filter(
        product__id=pk).order_by('-timestamp')
    context = {
        'products': products,
    }
    return render(req, 'base/products/prod_stocks.html', context)


@login_required(login_url='login')
def prod_stock_details(req, pk):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')

    curr_obj = get_object_or_404(ProductStock, id=pk)
    context = {
        'curr_obj': curr_obj,
    }
    return render(req, 'base/products/prod_stock_details.html', context)


@login_required(login_url='login')
def create_prod_stock(req):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')

    form = ProductStockForm()
    if req.method == 'POST':
        form = ProductStockForm(req.POST)
        if form.is_valid():
            form.save()
        messages.success = 'Produit ajouté'
        return HttpResponse(status=204, headers={'HX-Trigger': 'db_changed'})
    else:
        return render(req, 'form.html', context={'form': form, 'form_title': 'Ajouter un stock'})


@login_required(login_url='login')
def edit_prod_stock(req, pk):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')

    curr_obj = get_object_or_404(ProductStock, id=pk)

    form = ProductStockForm(instance=curr_obj)
    if req.method == 'POST':
        form = ProductStockForm(req.POST, instance=curr_obj)
        if form.is_valid():
            form.save()

        return HttpResponse(status=204, headers={'HX-Trigger': 'db_changed'})
    else:
        return render(req, 'form.html', context={'curr_obj': curr_obj, 'form': form, 'form_title': 'Modifier ce stock'})


@login_required(login_url='login')
def filter_prod_stock(req):
    name_query = req.POST.get('name')
    brand_query = req.POST.get('brand')
    min_quantity = req.POST.get('min_quantity')
    max_quantity = req.POST.get('max_quantity')
    category_query = req.POST.get('category')
    family_query = req.POST.get('family')
    store_query = req.POST.get('store')

    base_query = ProductStock.objects.all().order_by('product__name')

    if name_query:
        base_query = base_query.filter(name=name_query)
    if brand_query:
        base_query = base_query.filter(product__brand=brand_query)
    if min_quantity:
        base_query = base_query.filter(quantity__gte=min_quantity)
    if max_quantity:
        base_query = base_query.filter(quantity__lte=max_quantity)
    if category_query:
        base_query = base_query.filter(product__category__id=category_query)
    if family_query:
        base_query = base_query.filter(product__family__id=family_query)
    if store_query:
        base_query = base_query.filter(product__store__id=store_query)

    products = base_query

    context = {"products": products}

    return render(req, 'base/products/prod_stock_list.html', context)


# ------------------------------------------------- Cart views -------------------------------------------------
@login_required(login_url='login')
def cart(req):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')

    clients = Client.objects.all().order_by('-timestamp')
    if user.role.sec_level < 2:
        cashdesks = Cashdesk.objects.filter(
            store=user.profile.store).exclude(type='bank').order_by('name')
    else:
        cashdesks = Cashdesk.objects.all().exclude(type='bank').order_by('name')

    cart = Cart(req)
    cart_count = len(cart)
    cart_items = cart.get_cart_items()
    cart_total = cart.get_total_price()

    context = {
        'cart': cart,
        'cart_count': cart_count,
        'cart_items': cart_items,
        'cart_total': cart_total,
        'clients': clients,
        'cashdesks': cashdesks,
    }
    return render(req, 'base/cart/index.html', context)


@login_required(login_url='login')
def add_to_cart(req):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')

    clients = Client.objects.all().order_by('-timestamp')
    if user.role.sec_level < 2:
        cashdesks = Cashdesk.objects.filter(
            store=user.profile.store).exclude(type='bank').order_by('name')
    else:
        cashdesks = Cashdesk.objects.all().exclude(type='bank').order_by('name')

    cart = Cart(req)
    if req.POST.get('action') == 'post':
        product_id = int(req.POST.get('product_id'))
        product = get_object_or_404(ProductStock, id=product_id)
        cart.add_item(product)
        
    cart_items = cart.get_cart_items()
    cart_total = cart.get_total_price()

    context = {
        'cart': cart,
        'cart_items': cart_items,
        'cart_total': cart_total,
        'clients': clients,
        'cashdesks': cashdesks,
    }
    return render(req, 'base/cart/index.html', context)


@login_required(login_url='login')
def remove_from_cart(req):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')

    clients = Client.objects.all().order_by('-timestamp')
    if user.role.sec_level < 2:
        cashdesks = Cashdesk.objects.filter(
            store=user.profile.store).exclude(type='bank').order_by('name')
    else:
        cashdesks = Cashdesk.objects.all().exclude(type='bank').order_by('name')

    cart = Cart(req)
    if req.POST.get('action') == 'post':
        product_id = int(req.POST.get('product_id'))
        product = get_object_or_404(ProductStock, id=product_id)
        cart.remove_item(product)
        
    cart_items = cart.get_cart_items()
    cart_total = cart.get_total_price()

    context = {
        'cart': cart,
        'cart_items': cart_items,
        'cart_total': cart_total,
        'clients': clients,
        'cashdesks': cashdesks,
    }
    return render(req, 'base/cart/index.html', context)


@login_required(login_url='login')
def clear_item(req):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')

    clients = Client.objects.all().order_by('-timestamp')
    if user.role.sec_level < 2:
        cashdesks = Cashdesk.objects.filter(
            store=user.profile.store).exclude(type='bank').order_by('name')
    else:
        cashdesks = Cashdesk.objects.all().exclude(type='bank').order_by('name')

    cart = Cart(req)
    if req.POST.get('action') == 'post':
        product_id = int(req.POST.get('product_id'))
        product = get_object_or_404(ProductStock, id=product_id)
        cart.clear_item(product)
        
    cart_items = cart.get_cart_items()
    cart_total = cart.get_total_price()

    context = {
        'cart': cart,
        'cart_items': cart_items,
        'cart_total': cart_total,
        'clients': clients,
        'cashdesks': cashdesks,
    }
    return render(req, 'base/cart/index.html', context)


@login_required(login_url='login')
def clear_cart(req):
    cart = Cart(req)
    if req.POST.get('action') == 'post':
        cart.clear_cart()
    context = {
        'cart': cart,
    }
    return render(req, 'base/cart/index.html', context)



# --------------------------Checkout--------------------------
@login_required(login_url='login')
def checkout(req):
    user = req.user
    cart = Cart(req)
    cart_items = cart.get_cart_items()
    cart_count = len(cart)
    cart_total = cart.get_total_price()

    if cart_count > 0:
        client_id = req.POST.get('client_id')
        client = Client.objects.filter(id=client_id).first()
        cashdesk_id = req.POST.get('cashdesk_id') or 1
        cashdesk = Cashdesk.objects.filter(id=cashdesk_id).first()
        sale_payment = int(req.POST.get('sale_payment'))
        # print(f'amount paid : {sale_payment}')

        if client:
            new_sale = Sale(initiator=user, cashdesk=cashdesk, store = cashdesk.store, client=client, items=cart_count, total=cart_total)        
        else :
            new_sale = Sale(initiator=user, cashdesk=cashdesk, store = cashdesk.store, items=cart_count, total=cart_total)

        new_sale.save()

        for item in cart_items:
            product_stock = item['product']
            quantity = item['quantity']
            new_sale_item = SaleItem(
                sale=new_sale,
                product_stock=product_stock,
                quantity=quantity,
            )
            new_sale_item.save()

        # sale payment logic
        # Determine which is smaller between sale_payment and cart_total
        transaction_amount = min(sale_payment, cart_total)
        print(f'transaction amount : {transaction_amount}')

        # Create and save the transaction
        new_transaction = Transaction(
            initiator=user,
            cashdesk=cashdesk,
            store=cashdesk.store,
            type='credit',
            label='Vente de produit(s)',
            amount=transaction_amount,
            content_object = new_sale,
            object_id=new_sale.id
        )
        new_transaction.save()

        cart.clear_cart()
        # messages.success(req, 'Nouvelle vente éffectuée!')
        
        return redirect('sale_details', pk=new_sale.id)
    else:
        messages.info(req, "Access denied: Your cart is empty.")
        return HttpResponseRedirect(req.META.get('HTTP_REFERER'))



# ------------------------------------------------- Sales -------------------------------------------------
@login_required(login_url='login')
def sale_point(req):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')

    categories = Category.objects.all().order_by('name')
    families = Family.objects.all().order_by('name')
    stores = Store.objects.all().order_by('name')

    if user.role.sec_level < 2:
        products = ProductStock.objects.filter(store = user.profile.store)
    else :
        products = ProductStock.objects.all()

    name_query = req.GET.get('name', '')
    brand_query = req.GET.get('brand', '')
    category_query = req.GET.get('category', '')
    family_query = req.GET.get('family', '')
    store_query = req.GET.get('store', '')

    filters = Q()
    if name_query:
        filters &= Q(product__name__icontains=name_query)
    if brand_query:
        filters &= Q(product__brand__icontains=brand_query)
    if category_query:
        filters &= Q(product__category__id=category_query)
    if family_query:
        filters &= Q(product__family__id=family_query)
    if store_query:
        filters &= Q(product__store__id=store_query)

    products = products.filter(filters).order_by('product__name')

    objects = paginate_objects(req, products)

    #  cart stuff
    cart = Cart(req)
    cart_count = len(cart)
    cart_items = cart.get_cart_items()
    cart_total = cart.get_total_price()

    context = {
        "sale_point": "active",
        'title': 'Point de vente',
        "categories": categories,
        "families": families,
        "stores": stores,
        "products": products,
        "objects": objects,
        'cart_count': cart_count,
        'cart_items': cart_items,
        'cart_total': cart_total,
    }
    return render(req, 'base/sales/sale_point.html', context)

@login_required(login_url='login')
def sale_point_grid(req):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')

    categories = Category.objects.all().order_by('name')
    families = Family.objects.all().order_by('name')
    stores = Store.objects.all().order_by('name')
    lots = Lot.objects.all().order_by('name')

    if user.role.sec_level < 2:
        products = ProductStock.objects.filter(store = user.profile.store).order_by('product__name')
    else :
        products = ProductStock.objects.all().order_by('product__name')

    context = {
        "categories": categories,
        "families": families,
        "stores": stores,
        "lots": lots,
        "products": products
    }
    return render(req, 'base/sales/sale_point_grid.html', context)

@login_required(login_url='login')
def sales(req):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')
    stores = Store.objects.all()
    cashdesks = Cashdesk.objects.all().exclude(type='bank')
    initiators = CustomUser.objects.all()
    clients = Client.objects.all()
    today = timezone.now().date()
    # date_query = req.GET.get('date', None)
    # filters = Q()
    # if date_query:
    #     filters &= Q(timestamp__date=date_query)


    context = {
        "sales": "active",
        'title': 'Ventes',
        'stores': stores,
        'today': today,
        'cashdesks': cashdesks,
        'initiators': initiators,
        'clients': clients,
    }
    return render(req, 'base/sales/index.html', context)

@login_required(login_url='login')
def sales_table(req):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')

    if user.role.sec_level < 2:
        sales = Sale.objects.filter(store=user.profile.store).order_by('-timestamp')
    else:
        sales = Sale.objects.all().order_by('-timestamp')

    context = {
        'sales': sales,
    }
    return render(req, 'base/sales/sales_table.html', context)


@login_required(login_url='login')
def sale_details(req, pk):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')

    curr_obj = Sale.objects.get(id=pk)
    sale_items = SaleItem.objects.filter(sale=curr_obj)

    context = {
        "sales": "active",
        'title': 'Details de vente',
        'curr_obj': curr_obj,
        'sale_items': sale_items,
    }
    return render(req, 'base/sales/sale_details.html', context)


@login_required(login_url='login')
def create_sale(req):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')

    form = SaleForm()
    if req.method == 'POST':
        form = SaleForm(req.POST)
        if user.role.sec_level < 2:
            form.instance.store = user.profile.store
        if form.is_valid():
            form.save()
        return HttpResponse(status=204, headers={'HX-Trigger': 'db_changed'})
    else:
        return render(req, 'form.html', context={'form': form, 'form_title': 'Modifier cette vente'})


@login_required(login_url='login')
def edit_sale(req, pk):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')

    curr_obj = get_object_or_404(Sale, id=pk)

    form = SaleForm(instance=curr_obj, curr_obj=curr_obj)
    if req.method == 'POST':
        form = SaleForm(req.POST, instance=curr_obj, curr_obj=curr_obj)
        if form.is_valid():
            form.save()
        return HttpResponse(status=204, headers={'HX-Trigger': 'db_changed'})
    else:
        return render(req, 'form.html', context={'curr_obj': curr_obj, 'form': form, 'form_title': 'Modifier cette vente'})


def sale_info(req, pk):
    curr_obj = get_object_or_404(Sale, id=pk)
    sale_content_type = ContentType.objects.get_for_model(Sale)
    sale_items = SaleItem.objects.filter(sale=curr_obj)
    transactions = Transaction.objects.filter(
        content_type=sale_content_type, object_id=pk)
    
    is_fully_paid = False
    if curr_obj.total_paid == curr_obj.total:
        is_fully_paid = True
    context = {
        'curr_obj': curr_obj,
        'transactions': transactions,
        'sale_items': sale_items,
        'is_fully_paid': is_fully_paid,
    }
    return render(req, 'base/sales/sale_info.html', context)


@login_required(login_url='login')
def create_sale_transaction(req, pk):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')

    sale = get_object_or_404(Sale, id=pk)
    form = TransactionForm()
    sale_content_type = ContentType.objects.get_for_model(sale)

    if req.method == 'POST':
        form = TransactionForm(req.POST)
        form.instance.store = sale.store
        form.instance.content_type = sale_content_type
        form.instance.object_id = sale.id
        form.instance.cashdesk = sale.cashdesk
        form.instance.type = 'credit'
        form.instance.initiator = user

        if form.is_valid():
            print('valid')
            form.save()
            return HttpResponse(status=204, headers={'HX-Trigger': 'db_changed'})

    return render(req, 'form.html', context={'form': form, 'form_title': 'Nouveau paiement'})



def sale_items(req, pk):
    sale = get_object_or_404(Sale, id=pk)
    sale_items = SaleItem.objects.filter(sale=sale)
    context = {
        'sale_items': sale_items,
    }
    return render(req, 'base/sales/sale_items.html', context)



def create_sale_item(req, pk):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')

    sale = get_object_or_404(Sale, id=pk)

    form = SaleItemForm()
    if req.method == 'POST':
        form = SaleItemForm(req.POST)
        form.instance.sale = sale
        if form.is_valid():
            form.save()
        # messages.success = 'Nouvel achat de produit ajouté'
        return HttpResponse(status=204, headers={'HX-Trigger': 'db_changed'})
    else:
        return render(req, 'form.html', context={'form': form, 'form_title': 'Nouveau produit vendu'})



@login_required(login_url='login')
def edit_sale_item(req, pk):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')

    curr_obj = get_object_or_404(SaleItem, id=pk)

    form = SaleItemForm(instance=curr_obj)
    if req.method == 'POST':
        form = SaleItemForm(req.POST, instance=curr_obj)
        if form.is_valid():
            form.save()
        return HttpResponse(status=204, headers={'HX-Trigger': 'db_changed'})
    else:
        return render(req, 'form.html', context={'curr_obj': curr_obj, 'form': form, 'form_title': 'Modifier ce produit vendu'})



@login_required(login_url='login')
def filter_sales(req):
    user = req.user
    # user_query = req.POST.get('user')
    min_date_query = req.POST.get('min_date')
    max_date_query = req.POST.get('max_date')
    phone_query = req.POST.get('phone')
    amount_query = req.POST.get('amount')
    items_query = req.POST.get('items')
    status_query = req.POST.get('status')

    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')

    else:
        base_query = Sale.objects.all().order_by('-timestamp')

    # if user_query:
    #     base_query = base_query.filter(user_)

    if min_date_query:
        base_query = base_query.filter(timestamp__date__gte=min_date_query)
    if max_date_query:
        base_query = base_query.filter(timestamp__date__lte=max_date_query)
    if phone_query:
        base_query = base_query.filter(phone=phone_query)
    if amount_query:
        base_query = base_query.filter(amount=amount_query)
    if items_query:
        base_query = base_query.filter(items=items_query)
    if status_query:
        base_query = base_query.filter(status=status_query)

    sales = base_query

    context = {"sales": sales}

    return render(req, 'base/sales/sales_list.html', context)



# ------------------------------------------------- Purchases -------------------------------------------------
@login_required(login_url='login')
def purchases(req):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')

    context = {
        "purchases": "active",
        'title': 'Achats',
    }
    return render(req, 'base/purchases/index.html', context)


def purchase_details(req, pk):
    curr_obj = get_object_or_404(Purchase, id=pk)
    purchase_items = PurchaseItem.objects.filter(purchase=curr_obj)
    amount_due = curr_obj.total - curr_obj.total_paid

    context = {
        "purchases": "active",
        'title': "Details d'Achat",
        'curr_obj': curr_obj,
        'amount_due': amount_due,
        'purchase_items': purchase_items,
    }
    return render(req, 'base/purchases/purchase_details.html', context)


def purchase_info(req, pk):
    curr_obj = get_object_or_404(Purchase, id=pk)
    amount_due = curr_obj.total - curr_obj.total_paid
    purchase_type = ContentType.objects.get_for_model(curr_obj.__class__)
    transactions = Transaction.objects.filter(content_type=purchase_type, object_id=pk)
    print(transactions)

    transaction_complete = False
    if curr_obj.total == curr_obj.total_paid:
        transaction_complete = True

    context = {
        'curr_obj': curr_obj,
        'amount_due': amount_due,
        'transaction_complete': transaction_complete,
        'transactions': transactions,
    }
    return render(req, 'base/purchases/purchase_info.html', context)


@login_required(login_url='login')
def create_purchase(req, pk):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')

    form = PurchaseForm()
    if req.method == 'POST':
        form = PurchaseForm(req.POST)
        if form.is_valid():
            form.instance.initiator=user
            form.instance.type=pk
            form.save()
        messages.success = 'Nouvel achat de produit ajouté'
        return HttpResponse(status=204, headers={'HX-Trigger': 'db_changed'})
    else:
        return render(req, 'form.html', context={'form': form, 'form_title': 'Nouvel achat'})


@login_required(login_url='login')
def edit_purchase(req, pk):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')

    curr_obj = get_object_or_404(Purchase, id=pk)

    form = PurchaseForm(instance=curr_obj, curr_obj=curr_obj)
    if req.method == 'POST':
        form = PurchaseForm(req.POST, instance=curr_obj, curr_obj=curr_obj)
        if form.is_valid():
            form.save()
        return HttpResponse(status=204, headers={'HX-Trigger': 'db_changed'})
    else:
        return render(req, 'form.html', context={'curr_obj':curr_obj ,'form': form, 'form_title': 'Modifier cet achat'})


@login_required(login_url='login')
def purchases_list(req, pk):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')
    
    if user.role.sec_level < 2:
        purchases = Purchase.objects.filter(
            type=pk, store=user.prfile.store).order_by('-timestamp')
    else:
        purchases = Purchase.objects.filter(type=pk).order_by('-timestamp')

    context = {
        "purchases": "active",
        'title': 'Achats',
        'purchases': purchases,
    }

    if pk == 'product':
        return render(req, 'base/purchases/purchases_list_prod.html', context)
    if pk == 'service':
        return render(req, 'base/purchases/purchases_list_serv.html', context)

# Purchase items -----------------

def purchase_items(req, pk):
    purchase = get_object_or_404(Purchase, id=pk)
    purchase_items = PurchaseItem.objects.filter(purchase=purchase)
    context = {
        'purchase_items': purchase_items,
    }
    return render(req, 'base/purchases/purchase_items.html', context)

def create_purchase_item(req, pk):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')
    
    purchase = get_object_or_404(Purchase, id=pk)

    form = PurchaseItemForm()
    if req.method == 'POST':
        form = PurchaseItemForm(req.POST)
        form.instance.purchase = purchase
        if form.is_valid():
            form.save()
        # messages.success = 'Nouvel achat de produit ajouté'
        return HttpResponse(status=204, headers={'HX-Trigger': 'db_changed'})
    else:
        return render(req, 'form.html', context={'form': form, 'form_title': 'Nouvel achat de produit'})

@login_required(login_url='login')
def edit_purchase_item(req, pk):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')

    curr_obj = get_object_or_404(PurchaseItem, id=pk)

    form = PurchaseItemForm(instance=curr_obj)
    if req.method == 'POST':
        form = PurchaseItemForm(req.POST, instance=curr_obj)
        if form.is_valid():
            form.save()
        return HttpResponse(status=204, headers={'HX-Trigger': 'db_changed'})
    else:
        return render(req, 'form.html', context={'curr_obj':curr_obj ,'form': form, 'form_title': 'Modifier cet achat de produit'})


# --------------------------------
@login_required(login_url='login')
def create_purchase_transaction(req, pk):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')

    purchase = get_object_or_404(Purchase, id=pk)

    form = TransactionForm()
    purchase_content_type = ContentType.objects.get_for_model(purchase)

    if req.method == 'POST':
        form = TransactionForm(req.POST)
        form.instance.store = purchase.store
        form.instance.cashdesk = purchase.cashdesk
        form.instance.type = 'debit'
        form.instance.content_type = purchase_content_type
        form.instance.object_id = purchase.id
        form.instance.initiator = user

        if form.is_valid():
            # print(form.instance.amount)
            form.save()
            purchase.total_paid += form.instance.amount
            purchase.save()
            return HttpResponse(status=204, headers={'HX-Trigger': 'db_changed'})

    return render(req, 'form.html', context={'form': form, 'form_title': 'Nouveau paiement'})


# ------------------------------------------------- Clients -------------------------------------------------
@login_required(login_url='login')
def clients(req):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')

    context = {
        "clients": "active",
        'title': 'Clients',
    }
    return render(req, 'base/entities/clients.html', context)


@login_required(login_url='login')
def client_details(req, pk):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')
    curr_obj = get_object_or_404(Client, id=pk)
    initiators = CustomUser.objects.all()

    purchases = Sale.objects.filter(client=curr_obj).order_by('-timestamp')

    context = {
        "clients": "active",
        'title': 'Clients',
        'curr_obj': curr_obj,
        'initiators': initiators,
        'purchases': purchases,
    }
    return render(req, 'base/entities/client_details.html', context)


@login_required(login_url='login')
def client_purchases(req, pk):
    curr_obj = get_object_or_404(Client, id=pk)
    purchases = Sale.objects.filter(client=curr_obj)

    context = {
        'curr_obj': curr_obj,
        'purchases': purchases,
    }
    return render(req, 'base/purchases/client_purchases.html', context)


@login_required(login_url='login')
def filter_client_purchases(req, pk):
    curr_obj = get_object_or_404(Client, id=pk)
    
    min_date_query = req.POST.get('min_date')
    max_date_query = req.POST.get('max_date')
    initiator_query = req.POST.get('initiator')
    min_amount = req.POST.get('min_amount')
    max_amount = req.POST.get('max_amount')

    base_query = Sale.objects.filter(client=curr_obj).order_by('-timestamp')

    if min_date_query:
        base_query = base_query.filter(timestamp__date__gte=min_date_query)
    if max_date_query:
        base_query = base_query.filter(timestamp__date__lte=max_date_query)
    if min_amount:
        base_query = base_query.filter(total__gte=min_amount)
    if max_amount:
        base_query = base_query.filter(total__lte=max_amount)
    if initiator_query:
        base_query = base_query.filter(initiator__id=initiator_query)

    purchases = base_query

    context = {"purchases": purchases}

    return render(req, 'base/entities/client_purchases.html', context)


@login_required(login_url='login')
def clients_list(req):
    clients = Client.objects.all().order_by('name')
    context = {
        'clients': clients,
    }
    return render(req, 'base/entities/clients_list.html', context)


@login_required(login_url='login')
def create_client(req):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')

    form = ClientForm()
    if req.method == 'POST':
        form = ClientForm(req.POST)
        if form.is_valid():
            form.save()
        messages.success = 'Nouveau client ajouté'
        return HttpResponse(status=204, headers={'HX-Trigger': 'db_changed'})
    else:
        return render(req, 'form.html', context={'form': form, 'form_title': 'Nouveau client'})


@login_required(login_url='login')
def edit_client(req, pk):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')
    curr_obj = get_object_or_404(Client, id=pk)
    form = ClientForm(instance=curr_obj)
    if req.method == 'POST':
        form = ClientForm(req.POST, instance=curr_obj)
        if form.is_valid():
            form.save()
        messages.success = 'Client modifié'
        return HttpResponse(status=204, headers={'HX-Trigger': 'db_changed'})
    else:
        return render(req, 'form.html', context={'curr_obj':curr_obj ,'form': form, 'form_title': 'Modifier ce client'})


@login_required(login_url='login')
def filter_clients(req):
    user = req.user
    sex_query = req.POST.get('sex')
    name_query = req.POST.get('name')
    type_query = req.POST.get('type')

    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')

    else:
        base_query = Client.objects.all().order_by('name')

    if sex_query:
        base_query = base_query.filter(sex=sex_query)
    if name_query:
        base_query = base_query.filter(name=name_query)
    if type_query:
        base_query = base_query.filter(type=type_query)

    clients = base_query

    context = {"clients": clients}

    return render(req, 'base/entities/clients_list.html', context)



# ------------------------------------------------- Suppliers -------------------------------------------------
@login_required(login_url='login')
def suppliers(req):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')

    context = {
        "suppliers": "active",
        'title': 'Fournisseurs',
    }
    return render(req, 'base/entities/suppliers.html', context)


@login_required(login_url='login')
def supplier_details(req, pk):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')

    curr_obj = Supplier.objects.get(id=pk)
    available_products = ProductStock.objects.filter(
        supplier=curr_obj).order_by('product__name')
    received_products = ProductStock.objects.filter(
        supplier=curr_obj).order_by('product__name')
    returned_products = ProductStock.objects.filter(
        supplier=curr_obj).order_by('product__name')
    context = {
        "suppliers": "active",
        'title': 'Fournisseur',
        'curr_obj': curr_obj,
        'available_products': available_products,
        'received_products': received_products,
        'returned_products': returned_products,
    }
    return render(req, 'base/entities/supplier_details.html', context)


@login_required(login_url='login')
def suppliers_list(req):
    suppliers = Supplier.objects.all().order_by('name')
    context = {
        'suppliers': suppliers,
    }
    return render(req, 'base/entities/suppliers_list.html', context)


@login_required(login_url='login')
def create_supplier(req):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')

    form = SupplierForm()
    if req.method == 'POST':
        form = SupplierForm(req.POST)
        if form.is_valid():
            form.save()
        messages.success = 'Nouvelle catégorie ajouté'
        return HttpResponse(status=204, headers={'HX-Trigger': 'db_changed'})
    else:
        return render(req, 'form.html', context={'form': form, 'form_title': 'Nouveau fournisseur'})


@login_required(login_url='login')
def edit_supplier(req, pk):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')

    curr_obj = get_object_or_404(Supplier, id=pk)

    form = SupplierForm(instance=curr_obj)
    if req.method == 'POST':
        form = SupplierForm(req.POST, instance=curr_obj)
        if form.is_valid():
            form.save()
            # 
        return HttpResponse(status=204, headers={'HX-Trigger': 'db_changed'})
    else:
        return render(req, 'form.html', context={'curr_obj':curr_obj ,'form': form, 'form_title': 'Modifier ce fournisseur'})


@login_required(login_url='login')
def filter_suppliers(req):
    user = req.user
    name_query = req.POST.get('name')
    phone_query = req.POST.get('phone')
    email_query = req.POST.get('email')
    type_query = req.POST.get('type')

    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')

    else:
        base_query = Supplier.objects.all().order_by('name')

    if name_query:
        base_query = base_query.filter(name=name_query)
    if phone_query:
        base_query = base_query.filter(phone=phone_query)
    if email_query:
        base_query = base_query.filter(email=email_query)
    if type_query:
        base_query = base_query.filter(type=type_query)

    suppliers = base_query

    context = {"suppliers": suppliers}

    return render(req, 'base/entities/suppliers_list.html', context)



# ------------------------------------------------- Parameters -------------------------------------------------
@login_required(login_url='login')
def parameters(req):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')

    context = {
        "parameters": "active",
        'title': 'Parameters',
    }
    return render(req, 'base/parameters/index.html', context)


@login_required(login_url='login')
def categories_list(req):
    categories = Category.objects.all().order_by('name')
    context = {
        'categories': categories,
    }
    return render(req, 'base/parameters/categories_list.html', context)


@login_required(login_url='login')
def create_category(req):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')

    form = CategoryForm()
    if req.method == 'POST':
        form = CategoryForm(req.POST)
        if form.is_valid():
            form.save()
        messages.success = 'Nouvelle catégorie ajouté'
        return HttpResponse(status=204, headers={'HX-Trigger': 'db_changed'})
    else:
        return render(req, 'form.html', context={'form': form, 'form_title': 'Nouvelle catégorie'})


@login_required(login_url='login')
def edit_category(req, pk):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')

    curr_obj = get_object_or_404(Category, id=pk)

    form = CategoryForm(instance=curr_obj)
    if req.method == 'POST':
        form = CategoryForm(req.POST, instance=curr_obj)
        if form.is_valid():
            form.save()
        
        return HttpResponse(status=204, headers={'HX-Trigger': 'db_changed'})
    else:
        return render(req, 'form.html', context={'curr_obj':curr_obj ,'form': form, 'form_title': 'Modifier cette catégorie'})


@login_required(login_url='login')
def families_list(req):
    families = Family.objects.all().order_by('name')
    context = {
        'families': families,
        'title': 'title',
    }
    return render(req, 'base/parameters/families_list.html', context)


@login_required(login_url='login')
def create_family(req):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')

    form = FamilyForm()
    if req.method == 'POST':
        form = FamilyForm(req.POST)
        if form.is_valid():
            form.save()
        messages.success = 'Nouvelle famille ajoutée'
        return HttpResponse(status=204, headers={'HX-Trigger': 'db_changed'})
    else:
        return render(req, 'form.html', context={'form': form, 'form_title': 'Nouvelle famille'})


@login_required(login_url='login')
def edit_family(req, pk):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')

    curr_obj = get_object_or_404(Family, id=pk)

    form = FamilyForm(instance=curr_obj)
    if req.method == 'POST':
        form = FamilyForm(req.POST, instance=curr_obj)
        if form.is_valid():
            form.save()
        
        return HttpResponse(status=204, headers={'HX-Trigger': 'db_changed'})
    else:
        return render(req, 'form.html', context={'curr_obj':curr_obj ,'form': form, 'form_title': 'Modifier cette famille'})


def load_families(req):
    category_id = req.GET.get('category')
    families = Family.objects.filter(category_id=category_id).all()
    return JsonResponse(list(families.values('id', 'name')), safe=False)


# ------------------------------------------------- Stock views -------------------------------------------------
def stock(req):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')
    
    context = {
        "stock": "active",
        'title': 'Stock',
    }
    return render(req, 'base/stock/index.html', context)


def stock_overview(req):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')
    
    if user.role.sec_level < 2:
        inputs = StockOperation.objects.filter(type='input',
            store=user.profile.store).order_by('-timestamp')
        outputs = StockOperation.objects.filter(type='output',
            store=user.profile.store).order_by('-timestamp')
        products = ProductStock.objects.filter(
            product__store=user.profile.store).order_by('product__name')
    else:
        inputs = StockOperation.objects.all().order_by('-timestamp')
        outputs = StockOperation.objects.all().order_by('-timestamp')
        products = ProductStock.objects.all().order_by('product__name')
    
    context = {
        "inputs": inputs,
        "outputs": outputs,
        "products": products,
    }
    return render(req, 'base/stock/overview.html', context)


def store_stock(req, pk):
    inputs = StockOperation.objects.filter(type='input',store__id=pk).order_by('-timestamp')
    outputs = StockOperation.objects.filter(type='output',store__id=pk).order_by('-timestamp')
    products = ProductStock.objects.filter(product__store__id=pk).order_by('product__name')
    
    context = {
        "inputs": inputs,
        "outputs": outputs,
        "products": products,
    }
    return render(req, 'base/stock/overview.html', context)


def stock_ops(req, pk):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')

    if user.role.sec_level < 2:
        operations = StockOperation.objects.filter(type=pk,
            store=user.profile.store).order_by('-timestamp')
    else:
        operations = StockOperation.objects.filter(type=pk).order_by('-timestamp')

    purchases = operations.filter(subtype='purchase').order_by('-timestamp')
    returns = operations.filter(subtype='return').order_by('-timestamp')
    transfers = operations.filter(subtype='transfer').order_by('-timestamp')
    differences = operations.filter(subtype='difference').order_by('-timestamp')
    gifts = operations.filter(subtype='gift').order_by('-timestamp')
    sales = operations.filter(subtype='sale').order_by('-timestamp')
    usages = operations.filter(subtype='usage').order_by('-timestamp')

    context = {
        "operations": operations,
        "purchases": purchases,
        "returns": returns,
        "transfers": transfers,
        "differences": differences,
        "gifts": gifts,
        "sales": sales,
        "usages": usages,
    }

    if pk == 'input':
        return render(req, 'base/stock/ops_input.html', context)
    if pk == 'output':
        return render(req, 'base/stock/ops_output.html', context)


def create_stock_ops(req, pk):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')

    form = StockOperationForm()
    if req.method == 'POST':
        form = StockOperationForm(req.POST)
        form.instance.initiator = user
        form.instance.type = pk
        if form.is_valid():
            form.save()
        return HttpResponse(status=204, headers={'HX-Trigger': 'db_changed'})
    else:
        if pk == 'input':
            return render(req, 'form.html', context={'form': form, 'form_title': 'Nouvelle entrée de stock'})
        if pk == 'output':
            return render(req, 'form.html', context={'form': form, 'form_title': 'Nouvelle sortie de stock'})


def edit_stock_ops(req, pk):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')
    
    curr_obj = get_object_or_404(StockOperation, id=pk)

    form = StockOperationForm(instance=curr_obj)
    if req.method == 'POST':
        form = StockOperationForm(req.POST, instance=curr_obj)
        if form.is_valid():
            form.save()
        return HttpResponse(status=204, headers={'HX-Trigger': 'db_changed'})
    else:
        # if pk == 'input':
        #     return render(req, 'form.html', context={'curr_obj': curr_obj, 'form': form, 'form_title': 'Modifier cette entrée de stock'})
        # if pk == 'output':
        #     return render(req, 'form.html', context={'curr_obj': curr_obj, 'form': form, 'form_title': 'Modifier cette sortie de stock'})
        return render(req, 'form.html', context={'curr_obj': curr_obj, 'form': form, 'form_title': 'Modifier cette operation de stock'})


def stock_ops_details(req, pk):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')
    curr_obj = get_object_or_404(StockOperation, id=pk)
    items = StockOperationItem.objects.filter(stock_operation=curr_obj)

    context = {
        "stock": "active",
        'title': "Details de l'Opération",
        'curr_obj': curr_obj,
        'items': items,
    }
    return render(req, 'base/stock/ops_details.html', context)


def stock_ops_info(req, pk):
    curr_obj = get_object_or_404(StockOperation, id=pk)
    context = {
        'curr_obj': curr_obj,
    }
    return render(req, 'base/stock/ops_info.html', context)


def stock_ops_items(req, pk):
    stock_operation = get_object_or_404(StockOperation, id=pk)
    items = StockOperationItem.objects.filter(stock_operation=stock_operation)
    context = {
        'items': items,
    }
    return render(req, 'base/stock/ops_items.html', context)


def create_stock_ops_item(req, pk):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')

    stock_operation = get_object_or_404(StockOperation, id=pk)

    form = StockOperationItemForm()
    if req.method == 'POST':
        form = StockOperationItemForm(req.POST)
        form.instance.stock_operation = stock_operation
        if form.is_valid():
            form.save()
        return HttpResponse(status=204, headers={'HX-Trigger': 'db_changed'})
    else:
        return render(req, 'form.html', context={'form': form, 'form_title': 'Nouveau produit compté'})


@login_required(login_url='login')
def edit_stock_ops_item(req, pk):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')
    curr_obj = get_object_or_404(StockOperationItem, id=pk)

    form = StockOperationItemForm(instance=curr_obj)
    if req.method == 'POST':
        form = StockOperationItemForm(req.POST, instance=curr_obj)
        if form.is_valid():
            form.save()
        return HttpResponse(status=204, headers={'HX-Trigger': 'db_changed'})
    else:
        return render(req, 'form.html', context={'curr_obj': curr_obj, 'form': form, 'form_title': "Modifier le produit compté"})


# ------------------------------------------------- Stock inventories -------------------------------------------------
def inventories(req):
    inventories = Inventory.objects.all().order_by('-date')
    context = {
        "inventories": inventories,
    }
    return render(req, 'base/stock/inventories.html', context)


def inventory_details(req, pk):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')

    curr_obj = get_object_or_404(Inventory, id=pk)
    items = InventoryItem.objects.filter(
        inventory=curr_obj).order_by('product_stock__product__name')

    if req.method == 'POST':
        comment = req.POST.get('comment')
        for obj in items:
            qty_found = req.POST.get(f'qty_found_{obj.id}') or 0
            qty_found = int(qty_found)
            difference = qty_found - obj.quantity_expected
            InventoryItem.objects.update_or_create(
                inventory=curr_obj,
                product_stock=obj.product_stock,
                defaults={
                    'quantity_found': qty_found,
                    'difference': difference,
                    'comment': comment,
                }
            )
        return redirect('inventory_details', pk=pk)

    context = {
        "stock": "active",
        'title': "Details d'inventaire",
        "curr_obj": curr_obj,
        "items": items,
    }
    return render(req, 'base/stock/inventory_details.html', context)


@login_required(login_url='login')
def create_inventory(req):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')
    
    if user.role.sec_level < 2:
        store = user.profile.store or None
    else:
        store = None

    new_inventory = Inventory(
        store=store,
        initiator=user,
    )
    new_inventory.save()

    return redirect('inventory_details', pk=new_inventory.id)


def edit_inventory(req, pk):    
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')
    curr_obj = get_object_or_404(Inventory, id=pk)

    form = InventoryForm(instance=curr_obj, user=user)
    if req.method == 'POST':
        form = InventoryForm(req.POST, instance=curr_obj, user=user)
        if form.is_valid():
            form.save()
        return HttpResponse(status=204, headers={'HX-Trigger': 'db_changed'})
    else:
        return render(req, 'form.html', context={'curr_obj': curr_obj, 'form': form, 'form_title': "Modifier cet inventaire"})


def correct_inventory(req, pk):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')
    
    curr_obj = get_object_or_404(Inventory, id=pk)

    difference = curr_obj.quantity_found - curr_obj.quantity_expected

    if difference != 0:
        if difference > 0:
            type = 'input',
        if difference < 0:
            type = 'output',

        # Create StockOperation for excess inventory
        stock_operation, created = StockOperation.objects.get_or_create(
            initiator=curr_obj.initiator,
            store=curr_obj.store,
            type=type,
            subtype='difference',
            description=f"Difference d'inventaire {curr_obj.inventory.id}"
        )
        StockOperationItem.objects.create(
            stock_operation=stock_operation,
            product_stock=curr_obj.product_stock,
            quantity=abs(difference)
        )
        stock_operation.calculate_total()

    curr_obj.save()

    return redirect('inventory_details', pk=curr_obj.id)


# ------------------------------------------------- Cashdesk Closing -------------------------------------------------
def desk_closings_list(req, pk):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')
    
    curr_obj = get_object_or_404(Cashdesk, id=pk)
    desk_closings = CashdeskClosing.objects.filter(
        cashdesk=curr_obj).order_by('-timestamp')

    context = {
        "finances": "active",
        'desk_closings': desk_closings,
        'curr_obj': curr_obj,
    }
    return render(req, 'base/closings/desk_closings_list.html', context)



def desk_closing_details(req, pk):
    curr_obj = get_object_or_404(CashdeskClosing, id=pk)
    closing_receipts = ClosingCashReceipt.objects.filter(cashdesk_closing=curr_obj).order_by('-cash_receipt__value')

    if req.method == 'POST':
        for obj in closing_receipts:
            count = req.POST.get(f'count_{obj.id}') or 0
            if count:
                count = int(count)
                total_amount = obj.cash_receipt.value * count

                # Update individual instance attributes
                obj.count = count
                obj.total_amount = total_amount
                obj.save()
                
        comment = req.POST.get('comment')
        if comment:
            curr_obj.comment = comment
            curr_obj.save()

        return redirect('desk_closing_details', pk=pk)

    context = {
        "finances": "active",
        'title': "Details d'Achat",
        'curr_obj': curr_obj,
        'closing_receipts': closing_receipts,
    }
    return render(req, 'base/closings/desk_closing_details.html', context)


@login_required(login_url='login')
def create_closing_receipt(req, pk):
    cashdesk_closing = get_object_or_404(CashdeskClosing, id=pk)
    if req.method == 'POST':
        form = ClosingCashReceiptForm(req.POST)
        form.instance.cashdesk_closing = cashdesk_closing
        if form.is_valid():
            daily_cash_receipt = form.save(commit=False)
            daily_cash_receipt.user = req.user
            daily_cash_receipt.save()
            return redirect('daily_cash_receipt_list')
    else:
        form = ClosingCashReceiptForm()
    return render(req, 'create_closing_receipt.html', {'form': form})


@login_required(login_url='login')
def create_desk_closing(req, pk):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')

    cashdesk = get_object_or_404(Cashdesk, id=pk)
    new_closing = CashdeskClosing(
        cashdesk=cashdesk,
        initiator=user,
        supervisor=None, 
        # balance_expected=cashdesk.balance  # Ensure balance_expected is properly set
    )
    new_closing.save()  # Save the new CashdeskClosing object to the database

    cash_receipts = CashReceipt.objects.all()
    for obj in cash_receipts:
        new_receipt = ClosingCashReceipt(
            cashdesk_closing = new_closing,
            cash_receipt=obj,
        )
        new_receipt.save()

    return redirect('desk_closing_details', pk=new_closing.id)


@login_required(login_url='login')
def edit_desk_closing(req, pk):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')
    
    curr_obj = get_object_or_404(CashdeskClosing, id=pk)

    form = CashdeskClosingForm(instance=curr_obj, user=user)
    if req.method == 'POST':
        form = CashdeskClosingForm(req.POST, instance=curr_obj, user=user)
        if form.is_valid():
            print('valid')
            form.save()

        return HttpResponse(status=204, headers={'HX-Trigger': 'db_changed'})
    else:
        return render(req, 'form.html', context={'curr_obj': curr_obj, 'form': form, 'form_title': "Modifier l'arrêté de caisse"})


def correct_desk_closing(request, pk):
    user = request.user
    if not user.is_staff:
        messages.info(request, "Access denied!!!")
        return redirect('home')

    curr_obj = get_object_or_404(CashdeskClosing, id=pk)

    # The original comparison checks the same attribute; it should compare balance_expected to balance_found.
    if curr_obj.balance_found < curr_obj.balance_expected:
        difference = curr_obj.balance_expected - curr_obj.balance_found
        new_transaction = Transaction(
            initiator=user,
            store=curr_obj.cashdesk.store,
            cashdesk=curr_obj.cashdesk,
            amount=abs(difference),
            type = 'credit',
            label="Correction positive d'arrêté"
        )
        new_transaction.save()

        wallet = Wallet.objects.get(user=curr_obj.initiator)
        wallet.balance += difference
        wallet.save()


        print('cashdesk defficit corrected')

    elif curr_obj.balance_found > curr_obj.balance_expected:
        difference = curr_obj.balance_expected - curr_obj.balance_found
        new_transaction = Transaction(
            initiator=user,
            store=curr_obj.cashdesk.store,
            cashdesk=curr_obj.cashdesk,
            amount=abs(difference),
            type = 'debit',
            label="Correction negative d'arrêté"
        )
        new_transaction.save()


        print('cashdesk surplus corrected')

    return redirect('desk_closing_details', pk=curr_obj.id)


def desk_closing_info(req, pk):
    curr_obj = get_object_or_404(CashdeskClosing, id=pk)
    context = {
        'curr_obj': curr_obj,
    }
    return render(req, 'base/closings/closing_info.html', context)




# ------------------------------------------------- Finances views -------------------------------------------------

def finances(req):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')
    
    store = None
    if not user.is_superuser:
        store = get_object_or_404(Store, id=user.profile.store.id)
        transactions = Transaction.objects.filter(store=store).order_by('-timestamp')
        credits = transactions.filter(type='credit')
        debits = transactions.filter(type='debit')
        desks = Cashdesk.objects.filter(store=store)
        cash_desks = desks.filter(type='cash')
        mobile_desks = desks.filter(type='mobile')
        bank_desks = desks.filter(type='bank')
        
    else:
        desks = Cashdesk.objects.all()
        transactions = Transaction.objects.all().order_by('-timestamp')
        credits = transactions.filter(type='credit')
        debits = transactions.filter(type='debit')
        cash_desks = desks.filter(type='cash')
        mobile_desks = desks.filter(type='mobile')
        bank_desks = desks.filter(type='bank')

    cash_balance = cash_desks.aggregate(totals=Sum('balance'))['totals'] or 0
    mobile_balance =  mobile_desks.aggregate(totals=Sum('balance'))['totals'] or 0
    bank_balance = bank_desks.aggregate(totals=Sum('balance'))['totals'] or 0

    credits_aggregate = desks.aggregate(totals=Sum('credits'))['totals'] or 0
    credit_trans_aggregate = credits.aggregate(totals=Sum('amount'))['totals'] or 0
    debits_aggregate = desks.aggregate(totals=Sum('debits'))['totals'] or 0
    debit_trans_aggregate = debits.aggregate(totals=Sum('amount'))['totals'] or 0
    total_balance = credits_aggregate - debits_aggregate

    initiators = CustomUser.objects.all().order_by('last_name')
    stores = Store.objects.all().order_by('name')

    context = {
        "finances": "active",
        'title': 'Finances',
        'transactions': transactions,
        'credits': credits,
        'credits_aggregate': credits_aggregate,
        'credit_trans_aggregate': credit_trans_aggregate,
        'debits': debits,
        'debits_aggregate': debits_aggregate,
        'debit_trans_aggregate': debit_trans_aggregate,
        'store': store,
        'stores': stores,
        'cash_desks': cash_desks,
        'cash_balance': cash_balance,
        'mobile_desks': mobile_desks,
        'mobile_balance': mobile_balance,
        'bank_desks': bank_desks,
        'bank_balance': bank_balance,
        'initiators': initiators,
        'total_balance': total_balance,
    }
    return render(req, 'base/finances/index.html', context)


def credits_list(req):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')
    if user.role.sec_level < 2:
        credits = Transaction.objects.filter(store=user.profile.store, type='credit').order_by('-timestamp')
    else:
        credits = Transaction.objects.filter(type='credit').order_by('-timestamp')

    credits_aggregate = credits.aggregate(totals=Sum('amount'))['totals'] or 0
    context = {
        'credits': credits,
        'credits_aggregate': credits_aggregate,
    }
    return render(req, 'base/finances/credits_list.html', context)


def debits_list(req):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')
    if user.role.sec_level < 2:
        debits = Transaction.objects.filter(store=user.profile.store, type='debit').order_by('-timestamp')
    else:
        debits = Transaction.objects.filter(type='debit').order_by('-timestamp')
    
    debits_aggregate = debits.aggregate(totals=Sum('amount'))['totals'] or 0
    context = {
        'debits': debits,
        'debits_aggregate': debits_aggregate,
    }
    return render(req, 'base/finances/debits_list.html', context)


def reports(req):
    context = {
        "finances": "active",
        'title': 'Tresorerie',
    }
    return render(req, 'base/reports.html', context)


def treasury(req):
    context = {
        "finances": "active",
        'title': 'Tresorerie',
    }
    return render(req, 'base/treasury.html', context)

# Cashdesks -------------------------------------------------
def cashdesks_list(req):
    user = req.user
    if user.role.sec_level <= 2:
        cashdesks = Cashdesk.objects.filter(store=user.profile.store).order_by('name')
    else:
        cashdesks = Cashdesk.objects.all().order_by('name')

    context = {
        'cashdesks': cashdesks,
    }
    return render(req, 'base/parameters/cashdesks_list.html', context)


@login_required(login_url='login')
def create_cashdesk(req):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')

    form = CashdeskForm()
    if req.method == 'POST':
        form = CashdeskForm(req.POST)
        if form.is_valid():
            form.save()
        return HttpResponse(status=204, headers={'HX-Trigger': 'db_changed'})
    else:
        return render(req, 'form.html', context={'form': form, 'form_title': 'Nouvelle caisse'})


@login_required(login_url='login')
def edit_cashdesk(req, pk):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')
    curr_obj = get_object_or_404(Cashdesk, id=pk)
    form = CashdeskForm(instance=curr_obj)
    if req.method == 'POST':
        form = CashdeskForm(req.POST,instance=curr_obj)
        if form.is_valid():
            form.save()
        return HttpResponse(status=204, headers={'HX-Trigger': 'db_changed'})
    else:
        return render(req, 'form.html', context={'curr_obj':curr_obj ,'form': form, 'form_title': 'Modifier cette caisse'})


@login_required(login_url='login')
def cashdesk_details(req, pk):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')
    curr_obj = get_object_or_404(Cashdesk, id=pk)
    initiators = CustomUser.objects.all()
    transactions = Transaction.objects.filter(cashdesk=curr_obj)
    debits = transactions.filter(type='debit')
    debits_aggregate = debits.aggregate(totals=Sum('amount'))['totals'] or 0
    # debits_aggregate = curr_obj.debits
    credits = transactions.filter(type='credit')
    credits_aggregate = credits.aggregate(totals=Sum('amount'))['totals'] or 0
    # credits_aggregate = curr_obj.credits
    balance = credits_aggregate - debits_aggregate
    rel_cashdesks = Cashdesk.objects.filter(store=curr_obj.store).exclude(id=pk)
    context = {
        "finances": "active",
        'title': 'Details de caisse',
        'initiators': initiators,
        'curr_obj': curr_obj,
        'transactions': transactions,
        'debits': debits ,
        'debits_aggregate': debits_aggregate,
        'credits': credits,
        'credits_aggregate': credits_aggregate,
        'balance': balance,
        'rel_cashdesks': rel_cashdesks,
    }
    return render(req, 'base/finances/cashdesk_details.html', context)

# Transactions -------------------------------------------------

def transactions_list(req):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')

    if not user.is_superuser:
        transactions = Transaction.objects.filter(store=user.profile.store).order_by('-timestamp')
    else:
        transactions = Transaction.objects.all().order_by('-timestamp')
        
    context = {
        'transactions': transactions,
    }
    return render(req, 'base/finances/transactions_list.html', context)


@login_required(login_url='login')
def transaction_details(req, pk):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')
    curr_obj = get_object_or_404(Transaction, id=pk)
    context = {
        "finances": "active",
        'title': 'Details de transaction',
        'curr_obj': curr_obj,
    }
    return render(req, 'base/finances/transaction_details.html', context)


@login_required(login_url='login')
def filter_transactions(req):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')
    
    min_date_query = req.POST.get('min_date')
    max_date_query = req.POST.get('max_date')
    store_query = req.POST.get('store')
    initiator_query = req.POST.get('initiator')
    type_query = req.POST.get('type')
    min_amount = req.POST.get('min_amount')
    max_amount = req.POST.get('max_amount')

    if not user.is_superuser:
        base_query = Transaction.objects.filter(store=user.profile.store).order_by('-timestamp')
    else:
        base_query = Transaction.objects.all().order_by('-timestamp')

    if min_date_query:
        base_query = base_query.filter(timestamp__date__gte=min_date_query)
    if max_date_query:
        base_query = base_query.filter(timestamp__date__lte=max_date_query)
    if store_query:
        base_query = base_query.filter(store__id=store_query)
    if initiator_query:
        base_query = base_query.filter(initiator__id=initiator_query)
    if type_query:
        base_query = base_query.filter(type=type_query)
    if min_amount:
        base_query = base_query.filter(amount__gte=min_amount)
    if max_amount:
        base_query = base_query.filter(amount__lte=max_amount)

    transactions = base_query

    context = {"transactions": transactions}

    return render(req, 'base/finances/transactions_list.html', context)


@login_required(login_url='login')
def create_transaction(req):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')

    form = TransactionForm()
    if req.method == 'POST':
        form = TransactionForm(req.POST)
        if user.role.sec_level < 2:
            form.instance.store = user.profile.store
            form.instance.initiator = user
        if form.is_valid():
            form.save()
        return HttpResponse(status=204, headers={'HX-Trigger': 'db_changed'})
    else:
        return render(req, 'form.html', context={'form': form, 'form_title': 'Nouveau paiement'})

@login_required(login_url='login')
def create_desk_transaction(req,pk):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')
    
    desk = get_object_or_404(Cashdesk, id=pk)

    form = TransactionForm(desk=desk)
    if req.method == 'POST':
        form = TransactionForm(req.POST, desk=desk)
        form.instance.store = desk.store
        form.instance.cashdesk = desk
        form.instance.initiator = user
        if form.is_valid():
            form.save()
        return HttpResponse(status=204, headers={'HX-Trigger': 'db_changed'})
    else:
        return render(req, 'form.html', context={'form': form, 'form_title': 'Nouveau paiement'})


@login_required(login_url='login')
def edit_transaction(req, pk):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')
    curr_obj = get_object_or_404(Transaction, id=pk)

    form = TransactionForm(instance=curr_obj)
    if req.method == 'POST':
        form = TransactionForm(req.POST,  instance=curr_obj)
        if form.is_valid():
            form.save()
        messages.success = 'Paiement modifié'
        return HttpResponse(status=204, headers={'HX-Trigger': 'db_changed'})
    else:
        return render(req, 'form.html', context={'curr_obj': curr_obj, 'form': form, 'form_title': 'Modifier ce paiement'})


def transactions_list(req):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')

    if not user.is_superuser:
        transactions = Transaction.objects.filter(
            store=user.profile.store).order_by('-timestamp')
    else:
        transactions = Transaction.objects.all().order_by('-timestamp')

    context = {
        'transactions': transactions,
    }
    return render(req, 'base/finances/transactions_list.html', context)


def store_transactions(req, pk):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')
    
    transactions = Transaction.objects.filter(store_id=pk).order_by('-timestamp')

    context = {
        'transactions': transactions,
    }
    return render(req, 'base/finances/transactions_list.html', context)


def desk_transactions(req, pk):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')

    transactions = Transaction.objects.filter(cashdesk_id=pk).order_by('-timestamp')
        
    context = {
        'transactions': transactions,
    }
    return render(req, 'base/finances/transactions_list.html', context)


@login_required(login_url='login')
def transaction_details(req, pk):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')

    curr_obj = get_object_or_404(Transaction, id=pk)

    context = {
        'curr_obj': curr_obj,
    }
    return render(req, 'base/finances/transaction_details.html', context)


# Credits and Debits -------------------------------------------------

@login_required(login_url='login')
def create_credit(req):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')

    form = TransactionForm()
    if req.method == 'POST':
        form = TransactionForm(req.POST)
        form.instance.type = 'credit'
        form.instance.initiator = user
        if user.role.sec_level < 2:
            form.instance.store = user.profile.store
        if form.is_valid():
            form.save()
        return HttpResponse(status=204, headers={'HX-Trigger': 'db_changed'})
    else:
        return render(req, 'form.html', context={'form': form, 'form_title': 'Nouvel encaissement'})


@login_required(login_url='login')
def create_debit(req):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')

    form = TransactionForm()
    if req.method == 'POST':
        form = TransactionForm(req.POST)
        form.instance.type = 'debit'
        form.instance.initiator = user
        if user.role.sec_level < 2:
            form.instance.store = user.profile.store
        if form.is_valid():
            form.save()
        return HttpResponse(status=204, headers={'HX-Trigger': 'db_changed'})
    else:
        return render(req, 'form.html', context={'form': form, 'form_title': 'Nouveau décaissement'})



# ------------------------------------------------- Debts -------------------------------------------------

def debts_list(req):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')

    if not user.is_superuser:
        debts = Debt.objects.filter(
            store=user.profile.store).order_by('-timestamp')
    else:
        debts = Debt.objects.all().order_by('-timestamp')

    context = {
        'debts': debts,
    }
    return render(req, 'base/finances/debts_list.html', context)

def store_debts(req, pk):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')
    
    debts = Debt.objects.filter(store_id=pk).order_by('-timestamp')

    context = {
        'debts': debts,
    }
    return render(req, 'base/finances/debts_list.html', context)


@login_required(login_url='login')
def debt_details(req, pk):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')

    curr_obj = get_object_or_404(Debt, id=pk)

    context = {
        'curr_obj': curr_obj,
    }
    return render(req, 'base/finances/debt_details.html', context)


@login_required(login_url='login')
def create_debt(req):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')

    form = DebtForm()
    if req.method == 'POST':
        form = DebtForm(req.POST)
        if user.role.sec_level < 2:
            form.instance.store = user.profile.store
        if form.is_valid():
            form.save()
        return HttpResponse(status=204, headers={'HX-Trigger': 'db_changed'})
    else:
        return render(req, 'form.html', context={'form': form, 'form_title': 'Nouvelle dette'})


@login_required(login_url='login')
def edit_debt(req, pk):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')
    curr_obj = get_object_or_404(Debt, id=pk)

    form = DebtForm(instance=curr_obj)
    if req.method == 'POST':
        form = DebtForm(req.POST,  instance=curr_obj)
        if form.is_valid():
            form.save()
        messages.success = 'Paiement modifié'
        return HttpResponse(status=204, headers={'HX-Trigger': 'db_changed'})
    else:
        return render(req, 'form.html', context={'curr_obj': curr_obj, 'form': form, 'form_title': 'Modifier cette dette'})


# ------------------------------------------------- Receivables -------------------------------------------------

def receivables_list(req):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')

    if not user.is_superuser:
        receivables = Receivable.objects.filter(
            store=user.profile.store).order_by('-timestamp')
    else:
        receivables = Receivable.objects.all().order_by('-timestamp')

    context = {
        'receivables': receivables,
    }
    return render(req, 'base/finances/receivables_list.html', context)


def store_receivables(req, pk):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')
    store = get_object_or_404(Store, id=pk)
    
    receivables = Receivable.objects.filter(
        sale__store=store).order_by('-timestamp')

    context = {
        'receivables': receivables,
    }
    return render(req, 'base/finances/receivables_list.html', context)


@login_required(login_url='login')
def receivable_details(req, pk):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')
    
    curr_obj = get_object_or_404(Receivable, id=pk)

    context = {
        'curr_obj': curr_obj,
    }
    return render(req, 'base/finances/receivable_details.html', context)


@login_required(login_url='login')
def create_receivable(req):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')

    form = ReceivableForm()
    if req.method == 'POST':
        form = ReceivableForm(req.POST)
        if user.role.sec_level < 2:
            form.instance.store = user.profile.store
        if form.is_valid():
            form.save()
        return HttpResponse(status=204, headers={'HX-Trigger': 'db_changed'})
    else:
        return render(req, 'form.html', context={'form': form, 'form_title': 'Nouvelle créance'})


@login_required(login_url='login')
def edit_receivable(req, pk):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')
    curr_obj = get_object_or_404(Receivable, id=pk)

    form = ReceivableForm(instance=curr_obj)
    if req.method == 'POST':
        form = ReceivableForm(req.POST,  instance=curr_obj)
        if form.is_valid():
            form.save()
        messages.success = 'Paiement modifié'
        return HttpResponse(status=204, headers={'HX-Trigger': 'db_changed'})
    else:
        return render(req, 'form.html', context={'curr_obj': curr_obj, 'form': form, 'form_title': 'Modifier cette créance'})


# ------------------------------------------------- Delete and 404 routes -------------------------------------------------
@require_http_methods(['DELETE'])
@login_required(login_url='login')
def delete_base_object(req, pk, model_name):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')

    try:
        # Get the model class from the model name
        ModelClass = apps.get_model('base', model_name)
    except LookupError:
        return HttpResponse(status=404)  # Model not found

    # Fetch the object to be deleted
    obj = get_object_or_404(ModelClass, pk=pk)

    # Check user's permission and show snackabr
    if req.user.role.sec_level < 3:
        # Send a custom HTMX trigger
        response = HttpResponse(status=403, headers={'HX-Trigger': 'access-denied'})
        return response

    # Delete the object
    obj.delete()

    # Return a success response
    return HttpResponse(status=204, headers={'HX-Trigger': 'db_changed'})


def not_found(req, exception):
    context = {
        "not_found_page": "active",
        "title": 'Page 404',

    }
    return render(req, 'not_found.html', context)
