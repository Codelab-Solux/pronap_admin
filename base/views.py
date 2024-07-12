import logging
from django.contrib import messages
from django.apps import apps
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Q
from django.db.models import Sum

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


EntityTypeForm

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
        messages.success = 'Paiement modifié'
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
        'title': 'Accueil',
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
    products = ProductStock.objects.filter(product__id = pk).order_by('-timestamp')
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
        return render(req, 'form.html', context={'curr_obj':curr_obj ,'form': form, 'form_title': 'Modifier ce stock'})


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


# ------------------------------------------------- Cart -------------------------------------------------
@login_required(login_url='login')
def cart(req):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')

    cart = Cart(req)
    cart_count = len(cart)
    cart_items = cart.get_cart_items()
    cart_total = cart.get_total_price()

    clients = Client.objects.all().order_by('-timestamp')

    if user.role.sec_level < 2:
        cashdesks = Cashdesk.objects.filter(
            store=user.profile.store).exclude(type='bank').order_by('name')
    else :
        cashdesks = Cashdesk.objects.all().exclude(type='bank').order_by('name')

    context = {
        'cart_count': cart_count,
        'cart_items': cart_items,
        'cart_total': cart_total,
        'clients': clients,
        'cashdesks': cashdesks,
    }
    return render(req, 'base/cart.html', context)


@login_required(login_url='login')
def add_to_cart(req):
    cart = Cart(req)
    if req.POST.get('action') == 'post':
        product_id = int(req.POST.get('product_id'))
        print(product_id)
        product = get_object_or_404(ProductStock, id=product_id)
        cart.add_item(product)
        cart_count = len(cart)
        res = JsonResponse({'cart_count': cart_count})
        return res


@login_required(login_url='login')
def remove_from_cart(req):
    cart = Cart(req)
    if req.POST.get('action') == 'post':
        product_id = int(req.POST.get('product_id'))
        product = get_object_or_404(ProductStock, id=product_id)
        # Save to a session
        cart.remove_item(product)
        # Use len(cart) to get the number of distinct items
        cart_count = len(cart)
        # Ensure the key matches in the AJAX call
        res = JsonResponse({'cart_count': cart_count})
        return res


@login_required(login_url='login')
def clear_item(req):
    cart = Cart(req)
    if req.POST.get('action') == 'post':
        product_id = int(req.POST.get('product_id'))
        product = get_object_or_404(ProductStock, id=product_id)
        # Save to a session
        cart.clear_item(product)
        # Use len(cart) to get the number of distinct items
        cart_count = len(cart)
        # Ensure the key matches in the AJAX call
        res = JsonResponse({'cart_count': cart_count})
        return res


@login_required(login_url='login')
def clear_cart(req):
    cart = Cart(req)
    if req.POST.get('action') == 'post':
        product_id = int(req.POST.get('product_id'))
        product = get_object_or_404(ProductStock, id=product_id)
        # Save to a session
        cart.clear_cart()
        # Use len(cart) to get the number of distinct items
        cart_count = len(cart)
        # Ensure the key matches in the AJAX call
        res = JsonResponse({'cart_count': cart_count})
        return res


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
        if client:
            new_sale = Sale(initiator=user, cashdesk=cashdesk, store = cashdesk.store, client=client, items=cart_count, total=cart_total)        
        else :
            new_sale = Sale(initiator=user, cashdesk=cashdesk, store = cashdesk.store, items=cart_count, total=cart_total)

        new_sale.save()

        new_stock_output = StockOutput(initiator=user, type='sale', description='Vente de produit(s)')

        new_stock_output.save()

        for item in cart_items:
            product_stock = item['product']
            quantity = item['quantity']
            new_sale_item = SaleItem(
                sale=new_sale,
                product_stock=product_stock,
                quantity=quantity,
            )
            new_sale_item.save()

            new_stock_output_item = StockOutputItem(
                stock_output = new_stock_output,
                product_stock=product_stock,
                quantity=quantity,
            )

            new_stock_output_item.save()

            new_quantity = product_stock.quantity - quantity
            print(f'old quantity = {product_stock.quantity}')

            product_stock.quantity  = new_quantity

            print(f'new quantity = {new_quantity}')
            product_stock.save()


        cart.clear_cart()
        # messages.success(req, 'Nouvelle vente éffectuée!')
        return redirect('sales')
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
    clients = Client.objects.all().order_by('-timestamp')
    stores = Store.objects.all().order_by('name')

    if user.role.sec_level < 2:
        products = ProductStock.objects.filter(store = user.profile.store)
        cashdesks = Cashdesk.objects.filter(
            store=user.profile.store).order_by('name')
    else :
        cashdesks = Cashdesk.objects.all().exclude(type='bank').order_by('name')
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
        "cashdesks": cashdesks,
        "products": products,
        "clients": clients,
        "objects": objects,
        'cart_count': cart_count,
        'cart_items': cart_items,
        'cart_total': cart_total,
    }
    return render(req, 'base/sales/sale_point.html', context)


@login_required(login_url='login')
def sales(req):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')
    
    today = timezone.now().date()
    stores = Store.objects.all().order_by('name')
    cashdesks = Cashdesk.objects.all().order_by('name')
    clients = Client.objects.all().order_by('name')
    initiators = CustomUser.objects.all().order_by('last_name')

    if user.role.sec_level < 2:
        base_query = Sale.objects.filter(store=user.profile.store)
    else:
        base_query = Sale.objects.all()


    date_query = req.GET.get('date', None)
    amount_query = req.GET.get('amount', None)
    cashdesk_query = req.GET.get('cashdesk', None)
    client_query = req.GET.get('client', None)
    initiator_query = req.GET.get('initiator', None)
    store_query = req.GET.get('store', None)

    filters = Q()
    if date_query:
        filters &= Q(timestamp__date=date_query)
    if store_query:
        filters &= Q(store__id=store_query)
    if cashdesk_query:
        filters &= Q(cashdesk__id=cashdesk_query)
    if initiator_query:
        filters &= Q(initiator__id=initiator_query)
    if client_query:
        filters &= Q(client__id=client_query)
    if amount_query:
        filters &= Q(total__icontains=amount_query)

    sales = base_query.filter(filters).order_by('-timestamp')

    objects = paginate_objects(req, sales)

    context = {
        "sales": "active",
        'title': 'Ventes',
        'objects': objects,
        'stores': stores,
        'today': today,
        'cashdesks': cashdesks,
        'initiators': initiators,
        'clients': clients,
    }
    return render(req, 'base/sales/index.html', context)


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
        'title': 'sale Details',
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

    form = SaleForm(instance=curr_obj)
    if req.method == 'POST':
        form = SaleForm(req.POST, instance=curr_obj)
        if form.is_valid():
            form.save()
        return HttpResponse(status=204, headers={'HX-Trigger': 'db_changed'})
    else:
        return render(req, 'form.html', context={'curr_obj': curr_obj, 'form': form, 'form_title': 'Modifier cette vente'})


def sale_info(req, pk):
    curr_obj = get_object_or_404(Sale, id=pk)
    context = {
        'curr_obj': curr_obj,
    }
    return render(req, 'base/sales/sale_info.html', context)


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


def prod_purchase_details(req, pk):
    curr_obj = get_object_or_404(ProductPurchase, id=pk)
    purchase_items = PurchaseItem.objects.filter(purchase=curr_obj)
    amount_due = curr_obj.total - curr_obj.amount_paid

    context = {
        "purchases": "active",
        'title': "Details d'Achat",
        'curr_obj': curr_obj,
        'amount_due': amount_due,
        'purchase_items': purchase_items,
    }
    return render(req, 'base/purchases/prod_purchase_details.html', context)


def create_prod_purchase(req):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')

    form = ProductPurchaseForm()
    if req.method == 'POST':
        form = ProductPurchaseForm(req.POST)
        if form.is_valid():
            form.save()
        messages.success = 'Nouvel achat de produit ajouté'
        return HttpResponse(status=204, headers={'HX-Trigger': 'db_changed'})
    else:
        return render(req, 'form.html', context={'form': form, 'form_title': 'Nouvel achat de produit'})


@login_required(login_url='login')
def edit_prod_purchase(req, pk):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')

    curr_obj = get_object_or_404(ProductPurchase, id=pk)

    form = ProductPurchaseForm(instance=curr_obj, curr_obj=curr_obj)
    if req.method == 'POST':
        form = ProductPurchaseForm(req.POST, instance=curr_obj, curr_obj=curr_obj)
        if form.is_valid():
            form.save()
        return HttpResponse(status=204, headers={'HX-Trigger': 'db_changed'})
    else:
        return render(req, 'form.html', context={'curr_obj':curr_obj ,'form': form, 'form_title': 'Modifier cet achat de produit'})


def prod_purchases_list(req):
    purchases = ProductPurchase.objects.all()
    context = {
        "purchases": "active",
        'title': 'Achats',
        'purchases': purchases,
    }
    return render(req, 'base/purchases/prod_purchases_list.html', context)


# Purchase items ----------------------------------------

def purchase_info(req, pk):
    curr_obj = get_object_or_404(ProductPurchase, id=pk)
    amount_due = curr_obj.total - curr_obj.amount_paid
    context = {
        'curr_obj': curr_obj,
        'amount_due': amount_due,
    }
    return render(req, 'base/purchases/purchase_info.html', context)

def purchase_items(req, pk):
    purchase = get_object_or_404(ProductPurchase, id=pk)
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
    
    purchase = get_object_or_404(ProductPurchase, id=pk)

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

# ----------------------------------------
@login_required(login_url='login')
def create_serv_purchase(req):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')

    form = ServicePurchaseForm()
    if req.method == 'POST':
        form = ServicePurchaseForm(req.POST)
        if form.is_valid():
            form.save()
        messages.success = 'Nouvel achat de service ajouté'
        return HttpResponse(status=204, headers={'HX-Trigger': 'db_changed'})
    else:
        return render(req, 'form.html', context={'form': form, 'form_title': 'Nouvel achat de service'})


def serv_purchase_details(req, pk):
    curr_obj = get_object_or_404(ServicePurchase, id=pk)
    context = {
        "purchases": "active",
        'title': "Details d'Achat",
        'curr_obj': curr_obj,
    }
    return render(req, 'base/purchases/serv_purchase_details.html', context)


@login_required(login_url='login')
def edit_service_purchase(req, pk):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')
    
    curr_obj = get_object_or_404(ServicePurchase, id=pk)

    form = ServicePurchaseForm(instance=curr_obj)
    if req.method == 'POST':
        form = ServicePurchaseForm(req.POST, instance=curr_obj)
        if form.is_valid():
            form.save()
        return HttpResponse(status=204, headers={'HX-Trigger': 'db_changed'})
    else:
        return render(req, 'form.html', context={'curr_obj':curr_obj ,'form': form, 'form_title': 'Modifier cet achat de service'})

def serv_purchases_list(req):
    purchases = ServicePurchase.objects.all()
    context = {
        "purchases": "active",
        'title': 'Achats',
        'purchases': purchases,
    }
    return render(req, 'base/purchases/serv_purchases_list.html', context)



# ------------------------------------------------- Clients-------------------------------------------------

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
        inputs = StockInput.objects.filter(
            store=user.profile.store).order_by('-timestamp')
        outputs = StockOutput.objects.filter(
            store=user.profile.store).order_by('-timestamp')
        products = ProductStock.objects.filter(
            product__store=user.profile.store).order_by('product__name')
    else:
        inputs = StockInput.objects.all().order_by('-timestamp')
        outputs = StockOutput.objects.all().order_by('-timestamp')
        products = ProductStock.objects.all().order_by('product__name')
    
    context = {
        "inputs": inputs,
        "outputs": outputs,
        "products": products,
    }
    return render(req, 'base/stock/overview.html', context)


def store_stock(req,pk):
    inputs = StockInput.objects.filter(store__id=pk).order_by('-timestamp')
    outputs = StockOutput.objects.filter(store__id=pk).order_by('-timestamp')
    products = ProductStock.objects.filter(product__store__id=pk).order_by('product__name')
    
    context = {
        "inputs": inputs,
        "outputs": outputs,
        "products": products,
    }
    return render(req, 'base/stock/overview.html', context)

# Stock inputs------------------------------------------------- 
def stock_inputs(req):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')

    if user.role.sec_level < 2:
        inputs = StockInput.objects.filter(
            store=user.profile.store).order_by('-timestamp')
    else:
        inputs = StockInput.objects.all().order_by('-timestamp')

    purchases = inputs.filter(type='purchase').order_by('-timestamp')
    returns = inputs.filter(type='return').order_by('-timestamp')
    transfers = inputs.filter(type='transfer').order_by('-timestamp')
    differences = inputs.filter(type='difference').order_by('-timestamp')
    gifts = inputs.filter(type='gift').order_by('-timestamp')

    context = {
        "inputs": inputs,
        "purchases": purchases,
        "returns": returns,
        "transfers": transfers,
        "differences": differences,
        "gifts": gifts,
    }

    return render(req, 'base/stock/inputs.html', context)


def create_stock_input(req):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')

    form = StockInputForm()
    if req.method == 'POST':
        form = StockInputForm(req.POST)
        form.instance.initiator = user
        if form.is_valid():
            form.save()
        return HttpResponse(status=204, headers={'HX-Trigger': 'db_changed'})
    else:
        return render(req, 'form.html', context={'form': form, 'form_title': 'Nouvelle entrée de stock'})


def edit_stock_input(req,pk):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')
    
    curr_obj = get_object_or_404(StockInput, id=pk)

    form = StockInputForm(instance=curr_obj)
    if req.method == 'POST':
        form = StockInputForm(req.POST, instance=curr_obj)
        if form.is_valid():
            form.save()
        return HttpResponse(status=204, headers={'HX-Trigger': 'db_changed'})
    else:
        return render(req, 'form.html', context={'curr_obj': curr_obj, 'form': form, 'form_title': "Modifier cette entrée de stock"})


def stock_input_details(req,pk):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')
    curr_obj = get_object_or_404(StockInput, id=pk)
    input_items = StockInputItem.objects.filter(stock_input=curr_obj)

    context = {
        "stock": "active",
        'title': "Details d'Entrée",
        'curr_obj': curr_obj,
        'input_items': input_items,
    }
    return render(req, 'base/stock/input_details.html', context)


def stock_input_info(req, pk):
    curr_obj = get_object_or_404(StockInput, id=pk)
    context = {
        'curr_obj': curr_obj,
    }
    return render(req, 'base/stock/input_info.html', context)


def stock_input_items(req, pk):
    stock_input = get_object_or_404(StockInput, id=pk)
    items = StockInputItem.objects.filter(stock_input=stock_input)
    context = {
        'items': items,
    }
    return render(req, 'base/stock/input_items.html', context)


def create_stock_input_item(req, pk):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')

    stock_input = get_object_or_404(StockInput, id=pk)

    form = StockInputItemForm()
    if req.method == 'POST':
        form = StockInputItemForm(req.POST)
        form.instance.stock_input = stock_input
        if form.is_valid():
            form.save()
        return HttpResponse(status=204, headers={'HX-Trigger': 'db_changed'})
    else:
        return render(req, 'form.html', context={'form': form, 'form_title': 'Nouveau produit compté'})


@login_required(login_url='login')
def edit_stock_input_item(req, pk):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')
    curr_obj = get_object_or_404(StockInputItem, id=pk)

    form = StockInputItemForm(instance=curr_obj)
    if req.method == 'POST':
        form = StockInputItemForm(req.POST, instance=curr_obj)
        if form.is_valid():
            form.save()
        return HttpResponse(status=204, headers={'HX-Trigger': 'db_changed'})
    else:
        return render(req, 'form.html', context={'curr_obj': curr_obj, 'form': form, 'form_title': "Modifier le produit compté"})


# Stock outputs------------------------------------------------- 

def stock_outputs(req):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')

    if user.role.sec_level < 2:
        outputs = StockOutput.objects.filter(
            store=user.profile.store).order_by('-timestamp')
    else:
        outputs = StockOutput.objects.all().order_by('-timestamp')

    purchases = outputs.filter( type='sale').order_by('-timestamp')
    returns = outputs.filter(type='return').order_by('-timestamp')
    transfers = outputs.filter(type='transfer').order_by('-timestamp')
    differences = outputs.filter(type='difference').order_by('-timestamp')
    gifts = outputs.filter(type='gift').order_by('-timestamp')

    context = {
        "outputs": outputs,
        "purchases": purchases,
        "returns": returns,
        "transfers": transfers,
        "differences": differences,
        "gifts": gifts,
    }

    return render(req, 'base/stock/outputs.html', context)


def stock_output_details(req,pk):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')
    curr_obj = get_object_or_404(StockOutput, id=pk)
    ouput_items = StockOutputItem.objects.filter(stock_output=curr_obj)
    context = {
        "stock": "active",
        'title': "Details de sortie",
        'curr_obj': curr_obj,
        'ouput_items': ouput_items,
    }
    return render(req, 'base/stock/output_details.html', context)


def create_stock_output(req):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')

    form = StockOutputForm()
    if req.method == 'POST':
        form = StockOutputForm(req.POST)
        form.instance.initiator = user
        if form.is_valid():
            form.save()
        return HttpResponse(status=204, headers={'HX-Trigger': 'db_changed'})
    else:
        return render(req, 'form.html', context={'form': form, 'form_title': 'Nouvelle sortie de stock'})


def edit_stock_output(req,pk):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')
    
    curr_obj = get_object_or_404(StockOutput, id=pk)

    form = StockOutputForm(instance=curr_obj)
    if req.method == 'POST':
        form = StockOutputForm(req.POST, instance=curr_obj)
        if form.is_valid():
            form.save()
        return HttpResponse(status=204, headers={'HX-Trigger': 'db_changed'})
    else:
        return render(req, 'form.html', context={'curr_obj': curr_obj, 'form': form, 'form_title': "Modifier cette sortie de stock"})


def stock_output_info(req, pk):
    curr_obj = get_object_or_404(StockOutput, id=pk)
    context = {
        'curr_obj': curr_obj,
    }
    return render(req, 'base/stock/output_info.html', context)


def stock_output_items(req, pk):
    stock_output = get_object_or_404(StockOutput, id=pk)
    items = StockOutputItem.objects.filter(stock_output=stock_output)
    context = {
        'items': items,
    }
    return render(req, 'base/stock/output_items.html', context)


def create_stock_output_item(req, pk):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')

    stock_output = get_object_or_404(StockOutput, id=pk)

    form = StockOutputItemForm()
    if req.method == 'POST':
        form = StockOutputItemForm(req.POST)
        form.instance.stock_output = stock_output
        if form.is_valid():
            form.save()
        return HttpResponse(status=204, headers={'HX-Trigger': 'db_changed'})
    else:
        return render(req, 'form.html', context={'form': form, 'form_title': 'Nouveau produit compté'})


@login_required(login_url='login')
def edit_stock_output_item(req, pk):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')
    curr_obj = get_object_or_404(StockOutputItem, id=pk)

    form = StockOutputItemForm(instance=curr_obj)
    if req.method == 'POST':
        form = StockOutputItemForm(req.POST, instance=curr_obj)
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


def edit_inventory(req,pk):    
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
    return render(req, 'base/accounting/desk_closings_list.html', context)



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
    return render(req, 'base/accounting/desk_closing_details.html', context)


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


def desk_closing_info(req, pk):
    curr_obj = get_object_or_404(CashdeskClosing, id=pk)
    context = {
        'curr_obj': curr_obj,
    }
    return render(req, 'base/accounting/closing_info.html', context)


# ------------------------------------------------- Finances -------------------------------------------------

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
        transactions = Transaction.objects.all().order_by('-timestamp')
        credits = transactions.filter(type='credit')
        debits = transactions.filter(type='debit')
        desks = Cashdesk.objects.all()
        cash_desks = desks.filter(type='cash')
        mobile_desks = desks.filter(type='mobile')
        bank_desks = desks.filter(type='bank')

    cash_balance = cash_desks.aggregate(totals=Sum('balance'))['totals'] or 0
    mobile_balance =  mobile_desks.aggregate(totals=Sum('balance'))['totals'] or 0
    bank_balance = bank_desks.aggregate(totals=Sum('balance'))['totals'] or 0

    credits_aggregate = credits.aggregate(totals=Sum('amount'))['totals'] or 0
    debits_aggregate = debits.aggregate(totals=Sum('amount'))['totals'] or 0
    balance = credits_aggregate - debits_aggregate

    initiators = CustomUser.objects.all().order_by('last_name')
    stores = Store.objects.all().order_by('name')

    context = {
        "finances": "active",
        'title': 'Finances',
        'transactions': transactions,
        'credits': credits,
        'credits_aggregate': credits_aggregate,
        'debits': debits,
        'store': store,
        'stores': stores,
        'cash_desks': cash_desks,
        'cash_balance': cash_balance,
        'mobile_desks': mobile_desks,
        'mobile_balance': mobile_balance,
        'bank_desks': bank_desks,
        'bank_balance': bank_balance,
        'initiators': initiators,
        'debits_aggregate': debits_aggregate,
        'balance': balance,
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
def edit_cashdesk(req,pk):
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
    credits = transactions.filter(type='credit')
    credits_aggregate = credits.aggregate(totals=Sum('amount'))['totals'] or 0
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

def store_transactions(req, pk):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')

    if not user.is_superuser:
        transactions = Transaction.objects.filter(store=user.profile.store).order_by('-timestamp')
    else:
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
def transaction_details(req,pk):
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
def transaction_editor(req,pk):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')
    curr_obj = get_object_or_404(Transaction, id=pk)
    context = {
        "finances": "active",
        'title': 'Modification de transaction',
        'curr_obj': curr_obj,
    }
    return render(req, 'base/finances/transactions_editor.html', context)


@login_required(login_url='login')
def create_transaction(req, pk):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')
    
    cashdesk = get_object_or_404(Cashdesk, id=pk)
    
    form = TransactionForm(cashdesk=cashdesk)
    if req.method == 'POST':
        form = TransactionForm(req.POST, cashdesk=cashdesk)
        form.instance.cashdesk = cashdesk
        form.instance.store = cashdesk.store
        if user.role.sec_level < 2:
            form.instance.initiator = user
            form.instance.store = user.profile.store
        if form.is_valid():
            form.save()
        return HttpResponse(status=204, headers={'HX-Trigger': 'db_changed'})
    else:
        return render(req, 'form.html', context={'form': form, 'form_title': 'Nouvelle transaction'})
    


@login_required(login_url='login')
def edit_transaction(req, pk):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')
    curr_obj = get_object_or_404(Transaction, id=pk)

    form = TransactionForm(instance=curr_obj)
    if req.method == 'POST':
        form = TransactionForm(req.POST, req.FILES, instance=curr_obj)
        if form.is_valid():
            form.save()
        messages.success = 'Transactione modifiée'
        return HttpResponse(status=204, headers={'HX-Trigger': 'db_changed'})
    else:
        return render(req, 'form.html', context={'curr_obj':curr_obj ,'form': form, 'form_title': 'Modifier cette transaction'})


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
    

@login_required(login_url='login')
def create_payment(req):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')

    form = PaymentForm()
    if req.method == 'POST':
        form = PaymentForm(req.POST)
        if user.role.sec_level < 2:
            form.instance.store = user.profile.store
            form.instance.initiator = user
        if form.is_valid():
            form.save()
        return HttpResponse(status=204, headers={'HX-Trigger': 'db_changed'})
    else:
        return render(req, 'form.html', context={'form': form, 'form_title': 'Nouveau paiement'})


@login_required(login_url='login')
def edit_payment(req, pk):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')
    curr_obj = get_object_or_404(Payment, id=pk)

    form = PaymentForm(instance=curr_obj)
    if req.method == 'POST':
        form = PaymentForm(req.POST,  instance=curr_obj)
        if form.is_valid():
            form.save()
        messages.success = 'Paiement modifié'
        return HttpResponse(status=204, headers={'HX-Trigger': 'db_changed'})
    else:
        return render(req, 'form.html', context={'curr_obj': curr_obj, 'form': form, 'form_title': 'Modifier ce paiement'})


def payments_list(req):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')

    if not user.is_superuser:
        payments = Payment.objects.filter(
            store=user.profile.store).order_by('-timestamp')
    else:
        payments = Payment.objects.all().order_by('-timestamp')

    context = {
        'payments': payments,
    }
    return render(req, 'base/finances/payments_list.html', context)


@login_required(login_url='login')
def payment_details(req, pk):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')

    curr_obj = get_object_or_404(Payment, id=pk)

    context = {
        'curr_obj': curr_obj,
    }
    return render(req, 'base/finances/payment_details.html', context)


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
