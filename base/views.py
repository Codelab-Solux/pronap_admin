import logging
from django.contrib import messages
from django.apps import apps
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
# from django.forms import inlineformset_factory
from django.db.models import Q

from accounts.forms import SignupForm
from .models import *
from .forms import *
from .views import *
from .cart import Cart

logger = logging.getLogger(__name__) 

@login_required(login_url='login')
def home(req):
    products = Product.objects.all()
    categories = Category.objects.all()

    context = {
        "home": "active",
        'title': 'Accueil',
        'products': products,
        'categories': categories,
    }
    return render(req, 'base/index.html', context)

@login_required(login_url='login')
def stores(req):
    personnel = CustomUser.objects.all()

    context = {
        "stores": "active",
        'title': 'Accueil',
        'personnel': personnel,
    }
    return render(req, 'base/stores.html', context)

@login_required(login_url='login')
def store_details(req, pk):
    staff = CustomUser.objects.all()
    curr_obj = get_object_or_404(Store, id=pk)
    transactions = Transaction.objects.filter(store=curr_obj).order_by('-timestamp')
    credits = transactions.filter(type='credit')
    debits = transactions.filter(type='debit')
    credits_aggregate = credits.aggregate(totals=Sum('amount'))['totals'] or 0
    debits_aggregate = debits.aggregate(totals=Sum('amount'))['totals'] or 0
    balance = credits_aggregate - debits_aggregate

    context = {
        "stores": "active",
        'title': 'Accueil',
        'staff': staff,
        'curr_obj': curr_obj,
        'credits': credits,
        'credits_aggregate': credits_aggregate,
        'debits': debits,
        'debits_aggregate': debits_aggregate,
        'balance': balance,
    }
    return render(req, 'base/store_details.html', context)


@login_required(login_url='login')
def stores_list(req):
    stores = Store.objects.all()
    context = {
        'stores': stores,
    }
    return render(req, 'base/partials/parameters/stores_list.html', context)



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
            print('created')
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
            print('created')
            form.save()
        messages.success = 'Produit créé'
        return HttpResponse(status=204, headers={'HX-Trigger': 'db_changed'})
    else:
        return render(req, 'form.html', context={'form': form, 'form_title': 'Créer un produit', })


# ------------------------------------------------- Products -------------------------------------------------
@login_required(login_url='login')
def products(req):
    categories = Category.objects.all()
    families = Family.objects.all()
    context = {
        "products": "active",
        'title': 'Produits',
        'categories': categories,
        'families': families,
    }
    return render(req, 'base/products.html', context)


@login_required(login_url='login')
def product_details(req, pk):
    curr_obj = Product.objects.get(id=pk)
    context = {
        "products_page": "active",
        'title': 'Products',
        'curr_obj': curr_obj,
    }
    return render(req, 'base/product_details.html', context)


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
            print('created')
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
        return render(req, 'form.html', context={'form': form, 'form_title': 'Modifier ce produit', 'curr_obj': curr_obj})


@login_required(login_url='login')
def products_list(req):
    products = Product.objects.all().order_by('name')
    context = {
        'products': products,
    }
    return render(req, 'base/partials/products_list.html', context)


@login_required(login_url='login')
def products_grid(req):
    products = Product.objects.all().order_by('name')
    context = {
        'products': products,
    }
    return render(req, 'base/partials/products_grid.html', context)


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

    return render(req, 'base/partials/products_list.html', context)


# ---------- products stock

@login_required(login_url='login')
def prod_stock_list(req):
    products = ProductStock.objects.all().order_by('product__name')
    context = {
        'products': products,
    }
    return render(req, 'base/partials/prod_stock_list.html', context)


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
    return render(req, 'base/partials/prod_stock_details.html', context)


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
        return render(req, 'form.html', context={'form': form, 'form_title': 'Modifier ce stock', 'curr_obj': curr_obj})


@login_required(login_url='login')
def filter_prod_stock(req):
    name_query = req.POST.get('name')
    brand_query = req.POST.get('brand')
    min_quantity = req.POST.get('min_quantity')
    max_quantity = req.POST.get('max_quantity')
    category_query = req.POST.get('category')
    family_query = req.POST.get('family')

    base_query = ProductStock.objects.all().order_by('product__name')

    if name_query:
        base_query = base_query.filter(name=name_query)
    if min_quantity:
        base_query = base_query.filter(quantity__gte=min_quantity)
    if max_quantity:
        base_query = base_query.filter(quantity__lte=max_quantity)
    if category_query:
        base_query = base_query.filter(product__category__id=category_query)
    if family_query:
        base_query = base_query.filter(product__family__id=family_query)
    if brand_query:
        base_query = base_query.filter(product__brand=brand_query)

    products = base_query

    context = {"products": products}

    return render(req, 'base/partials/prod_stock_list.html', context)


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

    context = {
        'cart_count': cart_count,
        'cart_items': cart_items,
        'cart_total': cart_total,
        'clients': clients,
    }
    return render(req, 'base/partials/cart.html', context)


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
        if client:
            new_sale = Sale(seller=user, buyer=client, items=cart_count, total=cart_total)        
        else :
            new_sale = Sale(seller=user, items=cart_count, total=cart_total)

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

    categories = Category.objects.all()
    families = Family.objects.all()
    clients = Client.objects.all().order_by('-timestamp')

    name_query = req.GET.get('name', '')
    brand_query = req.GET.get('brand', '')
    category_query = req.GET.get('category', '')
    family_query = req.GET.get('family', '')

    filters = Q()
    if name_query:
        filters &= Q(product__name__icontains=name_query)
    if brand_query:
        filters &= Q(product__brand__icontains=brand_query)
    if category_query:
        filters &= Q(product__category__id=category_query)
    if family_query:
        filters &= Q(product__family__id=family_query)

    products = ProductStock.objects.filter(filters).order_by('product__name')

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
        "products": products,
        "clients": clients,
        "objects": objects,
        'cart_count': cart_count,
        'cart_items': cart_items,
        'cart_total': cart_total,
    }
    return render(req, 'base/sale_point.html', context)


@login_required(login_url='login')
def sales(req):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')
    
    stores = Store.objects.all()
    cashdesks = Cashdesk.objects.all()
    buyers = Client.objects.all()
    sellers = CustomUser.objects.all()

    amount_query = req.GET.get('amount', '')
    cashdesk_query = req.GET.get('cashdesk', '')
    buyer_query = req.GET.get('buyer', '')
    seller_query = req.GET.get('seller', '')
    store_query = req.GET.get('store', '')

    filters = Q()
    if store_query:
        filters &= Q(store__id=store_query)
    if cashdesk_query:
        filters &= Q(cashdesk__id=cashdesk_query)
    if seller_query:
        filters &= Q(seller__id=seller_query)
    if buyer_query:
        filters &= Q(buyer__id=buyer_query)
    if amount_query:
        filters &= Q(total__icontains=amount_query)

    sales = Sale.objects.filter(filters).order_by('-timestamp')

    objects = paginate_objects(req, sales)

    context = {
        "sales": "active",
        'title': 'Ventes',
        'objects': objects,
        'stores': stores,
        'cashdesks': cashdesks,
        'sellers': sellers,
        'buyers': buyers,
    }
    return render(req, 'base/sales.html', context)


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
    return render(req, 'base/sale_details.html', context)


@login_required(login_url='login')
def edit_sale(req, pk):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')

    curr_obj = Sale.objects.get(id=pk)
    sale_items = SaleItem.objects.filter(sale=curr_obj)
    formset = SaleFormSet(instance=curr_obj)

    if req.method == 'POST':
        print('POST req received')
        formset = SaleFormSet(req.POST, instance=curr_obj)
        if formset.is_valid():
            print('Formset validated')
            formset.save()
            messages.success(req, "Sale updated successfully!")
            return redirect('sale_details', pk=pk)
        else:
            print('Formset errors:', formset.errors)
            messages.error(req, "Form submission failed. Please correct the errors and try again.")

    context = {
        "sales": "active",
        'title': 'sale Details',
        'curr_obj': curr_obj,
        'sale_items': sale_items,
        'formset': formset,
    }
    return render(req, 'base/sale_editor.html', context)


@login_required(login_url='login')
def manage_sale_item(req, pk, kp):
    sale_item = get_object_or_404(SaleItem, id=pk)
    product_stock = get_object_or_404(ProductStock, id=sale_item.product_stock.id)
    
    if kp in ['add', 'remove']:
        item_adjustment = 1 if kp == 'add' else -1
        stock_adjustment = -1 if kp == 'add' else 1
        
        # Update sale item quantity
        sale_item.quantity += item_adjustment
        sale_item.save()
        
        # Update product stock quantity
        product_stock.quantity += stock_adjustment
        product_stock.save()
    else:
        # Adjust product stock when sale item is deleted
        product_stock.quantity += sale_item.quantity
        product_stock.save()

        sale_item.delete()
        
    return HttpResponse(status=204, headers={'HX-Trigger': 'db_changed'})


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

    return render(req, 'base/partials/sales_list.html', context)


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
    return render(req, 'base/purchases.html', context)


def prod_purchase_details(req, pk):
    curr_obj = get_object_or_404(ProductPurchase, id=pk)
    purchase_items = PurchaseItem.objects.filter(purchase=curr_obj)
    formset = PurchaseFormSet(instance=curr_obj)
    amount_due = curr_obj.total - curr_obj.amount_paid

    if req.method == 'POST':
        print('POST req received')
        formset = PurchaseFormSet(req.POST, instance=curr_obj)
        if formset.is_valid():
            print('Formset validated')
            formset.save()
            messages.success(req, "Purchase updated successfully!")
            return redirect('prod_purchase_details', pk=pk)
        else:
            print('Formset errors:', formset.errors)
            messages.error(req, "Form submission failed. Please correct the errors and try again.")
    context = {
        "purchases": "active",
        'title': "Details d'Achat",
        'curr_obj': curr_obj,
        'formset': formset,
        'amount_due': amount_due,
        'purchase_items': purchase_items,
    }
    return render(req, 'base/partials/prod_purchase_details.html', context)


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
def edit_product_purchase(req, pk):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')

    curr_obj = get_object_or_404(ProductPurchase, id=pk)

    form = ProductPurchaseForm(instance=curr_obj)
    if req.method == 'POST':
        form = ProductPurchaseForm(req.POST, instance=curr_obj)
        if form.is_valid():
            form.save()
        return HttpResponse(status=204, headers={'HX-Trigger': 'db_changed'})
    else:
        return render(req, 'form.html', context={'form': form, 'form_title': 'Modifier cet achat de produit'})

def prod_purchases_list(req):
    purchases = ProductPurchase.objects.all()
    context = {
        "purchases": "active",
        'title': 'Achats',
        'purchases': purchases,
    }
    return render(req, 'base/partials/prod_purchases_list.html', context)

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
    return render(req, 'base/partials/serv_purchase_details.html', context)


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
        return render(req, 'form.html', context={'form': form, 'form_title': 'Modifier cet achat de service'})

def serv_purchases_list(req):
    purchases = ServicePurchase.objects.all()
    context = {
        "purchases": "active",
        'title': 'Achats',
        'purchases': purchases,
    }
    return render(req, 'base/partials/serv_purchases_list.html', context)

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
    return render(req, 'base/clients.html', context)


@login_required(login_url='login')
def client_details(req, pk):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')
    curr_obj = get_object_or_404(Client, id=pk)
    initiators = CustomUser.objects.all()

    purchases = Sale.objects.filter(buyer=curr_obj).order_by('-timestamp')

    context = {
        "clients": "active",
        'title': 'Clients',
        'curr_obj': curr_obj,
        'initiators': initiators,
        'purchases': purchases,
    }
    return render(req, 'base/client_details.html', context)


@login_required(login_url='login')
def client_purchases(req, pk):
    curr_obj = get_object_or_404(Client, id=pk)
    purchases = Sale.objects.filter(buyer=curr_obj)

    context = {
        'curr_obj': curr_obj,
        'purchases': purchases,
    }
    return render(req, 'base/partials/client_purchases.html', context)


@login_required(login_url='login')
def filter_client_purchases(req, pk):
    curr_obj = get_object_or_404(Client, id=pk)
    
    min_date_query = req.POST.get('min_date')
    max_date_query = req.POST.get('max_date')
    initiator_query = req.POST.get('initiator')
    min_amount = req.POST.get('min_amount')
    max_amount = req.POST.get('max_amount')

    base_query = Sale.objects.filter(buyer=curr_obj).order_by('-timestamp')

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

    return render(req, 'base/partials/client_purchases.html', context)


@login_required(login_url='login')
def clients_list(req):
    clients = Client.objects.all()
    context = {
        'clients': clients,
    }
    return render(req, 'base/partials/clients_list.html', context)


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
        messages.success = 'Nouveau cliente ajouté'
        return HttpResponse(status=204, headers={'HX-Trigger': 'db_changed'})
    else:
        return render(req, 'form.html', context={'form': form, 'form_title': 'Nouveau client'})


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

    return render(req, 'base/partials/clients_list.html', context)


# ------------------------------------------------- Staff -------------------------------------------------
@login_required(login_url='login')
def staff_list(req):
    staff = CustomUser.objects.filter(is_staff=True)
    context = {
        'staff': staff,
    }
    return render(req, 'accounts/partials/staff_list.html', context)


@login_required(login_url='login')
def staff_grid(req):
    personel = CustomUser.objects.all().order_by('last_name')
    context = {
        "staff": "active",
        'title': 'Personnel',
        "personel": personel,
    }
    return render(req, 'base/partials/staff_grid.html', context)


@login_required(login_url='login')
def staff(req):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')

    context = {
        "staff": "active",
        'title': 'Staff',
    }
    return render(req, 'base/staff.html', context)


@login_required(login_url='login')
def staff_details(req, pk):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')

    curr_obj = CustomUser.objects.get(id=pk)
    context = {
        "staff": "active",
        'title': 'Staff',
        'curr_obj': curr_obj,
    }
    return render(req, 'base/staff_details.html', context)


@login_required(login_url='login')
def create_staff(req):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')

    form = SignupForm()
    if req.method == 'POST':
        form = SignupForm(req.POST)
        if form.is_valid():
            form.save()
        messages.success = 'Nouveau personel ajouté'
        return HttpResponse(status=204, headers={'HX-Trigger': 'db_changed'})
    else:
        return render(req, 'form.html', context={'form': form, 'form_title': 'Nouveau client'})


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
    return render(req, 'base/suppliers.html', context)


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
    return render(req, 'base/supplier_details.html', context)


@login_required(login_url='login')
def suppliers_list(req):
    suppliers = Supplier.objects.all().order_by('name')
    context = {
        'suppliers': suppliers,
    }
    return render(req, 'base/partials/suppliers_list.html', context)


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
        return render(req, 'form.html', context={'form': form, 'form_title': 'Modifier ce fournisseur', 'curr_obj': curr_obj})





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

    return render(req, 'base/partials/suppliers_list.html', context)


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
    return render(req, 'base/parameters.html', context)


@login_required(login_url='login')
def categories_list(req):
    categories = Category.objects.all().order_by('name')
    context = {
        'categories': categories,
    }
    return render(req, 'base/partials/categories_list.html', context)


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
        return render(req, 'form.html', context={'form': form, 'form_title': 'Modifier cette catégorie', 'curr_obj': curr_obj})


@login_required(login_url='login')
def families_list(req):
    families = Family.objects.all().order_by('name')
    context = {
        'families': families,
        'title': 'title',
    }
    return render(req, 'base/partials/families_list.html', context)


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
        return render(req, 'form.html', context={'form': form, 'form_title': 'Modifier cette famille', 'curr_obj': curr_obj})


def load_families(req):
    category_id = req.GET.get('category')
    families = Family.objects.filter(category_id=category_id).all()
    return JsonResponse(list(families.values('id', 'name')), safe=False)


# ------------------------------------------------- Stock views -------------------------------------------------
def stock(req):
    context = {
        "stock": "active",
        'title': 'Stock',
    }
    return render(req, 'base/stock.html', context)


def stock_overview(req):
    inputs = StockInput.objects.all().order_by('-timestamp')
    outputs = StockOutput.objects.all().order_by('-timestamp')
    products = ProductStock.objects.all().order_by('product__name')
    
    context = {
        "inputs": inputs,
        "outputs": outputs,
        "products": products,
    }
    return render(req, 'base/partials/stock/overview.html', context)


def stock_inputs(req):
    inputs = StockInput.objects.all().order_by('-timestamp')
    purchases = StockInput.objects.filter(type='purchase').order_by('-timestamp')
    returns = StockInput.objects.filter(type='return').order_by('-timestamp')
    transfers = StockInput.objects.filter(type='transfer').order_by('-timestamp')
    differences = StockInput.objects.filter(type='difference').order_by('-timestamp')
    gifts = StockInput.objects.filter(type='gift').order_by('-timestamp')

    context = {
        "inputs": inputs,
        "purchases": purchases,
        "returns": returns,
        "transfers": transfers,
        "differences": differences,
        "gifts": gifts,
    }

    return render(req, 'base/partials/stock/inputs.html', context)


def stock_input_details(req,pk):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')
    curr_obj = get_object_or_404(StockInput, id=pk)
    input_items = StockInputItem.objects.filter(stock_input=curr_obj)
    formset = StockInputFormSet(instance=curr_obj)

    if req.method == 'POST':
        print('POST req received')
        formset = StockInputFormSet(req.POST, instance=curr_obj)
        if formset.is_valid():
            print('Formset validated')
            formset.save()
            messages.success(req, "StockInput updated successfully!")
            return redirect('stock_input_details', pk=pk)
        else:
            print('Formset errors:', formset.errors)
            messages.error(req, "Form submission failed. Please correct the errors and try again.")

    context = {
        "stock": "active",
        'title': "Details d'Entrée",
        'curr_obj': curr_obj,
        'formset': formset,
        'input_items': input_items,
    }
    return render(req, 'base/partials/stock/input_details.html', context)



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



def stock_outputs(req):
    outputs = StockOutput.objects.all().order_by('-timestamp')
    purchases = StockOutput.objects.filter( type='sale').order_by('-timestamp')
    returns = StockOutput.objects.filter(type='return').order_by('-timestamp')
    transfers = StockOutput.objects.filter(type='transfer').order_by('-timestamp')
    differences = StockOutput.objects.filter(type='difference').order_by('-timestamp')
    gifts = StockOutput.objects.filter(type='gift').order_by('-timestamp')

    context = {
        "outputs": outputs,
        "purchases": purchases,
        "returns": returns,
        "transfers": transfers,
        "differences": differences,
        "gifts": gifts,
    }

    return render(req, 'base/partials/stock/outputs.html', context)


def stock_output_details(req,pk):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')
    curr_obj = get_object_or_404(StockOutput, id=pk)
    ouput_items = StockOutputItem.objects.filter(stock_output=curr_obj)
    formset = StockOutputFormSet(instance=curr_obj)

    if req.method == 'POST':
        print('POST req received')
        formset = StockOutputFormSet(req.POST, instance=curr_obj)
        if formset.is_valid():
            print('Formset validated')
            formset.save()
            messages.success(req, "StockOutput updated successfully!")
            return redirect('stock_output_details', pk=pk)
        else:
            print('Formset errors:', formset.errors)
            messages.error(req, "Form submission failed. Please correct the errors and try again.")
    context = {
        "stock": "active",
        'title': "Details de sortie",
        'curr_obj': curr_obj,
        'formset': formset,
        'ouput_items': ouput_items,
    }
    return render(req, 'base/partials/stock/output_details.html', context)


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


def stock_inventories(req):
    inventories = Inventory.objects.all().order_by('-date')
    context = {
        "inventories": inventories
    }
    return render(req, 'base/partials/stock/inventories.html', context)


@login_required(login_url='login')
def inventory_details(req, pk):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')
    
    curr_obj = get_object_or_404(Inventory, id=pk)
    inventory_items = InventoryItem.objects.filter(inventory=curr_obj)
    formset = InventoryFormSet(instance=curr_obj)

    if req.method == 'POST':
        print('POST req received')
        formset = InventoryFormSet(req.POST, instance=curr_obj)
        if formset.is_valid():
            print('Formset validated')
            formset.save()
            messages.success(req, "Inventory updated successfully!")
            return redirect('inventory_details', pk=pk)
        else:
            print('Formset errors:', formset.errors)
            messages.error(req, "Form submission failed. Please correct the errors and try again.")

    context = {
        "stock": "active",
        'title': 'Inventaire',
        'curr_obj': curr_obj,
        'inventory_items': inventory_items,
        'formset': formset,
    }
    return render(req, 'base/partials/stock/inventory_details.html', context)


@login_required(login_url='login')
def create_inventory(req):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')

    form = InventoryForm()
    if req.method == 'POST':
        form = InventoryForm(req.POST)
        if form.is_valid():
            form.save()
        return HttpResponse(status=204, headers={'HX-Trigger': 'db_changed'})
    else:
        return render(req, 'form.html', context={'form': form, 'form_title': 'Nouvelle inventaire'})


@login_required(login_url='login')
def edit_inventory(req,pk):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')
    curr_obj = get_object_or_404(Inventory, id=pk)

    form = InventoryForm(instance=curr_obj)
    if req.method == 'POST':
        form = InventoryForm(req.POST, instance=curr_obj)
        if form.is_valid():
            form.save()
        return HttpResponse(status=204, headers={'HX-Trigger': 'db_changed'})
    else:
        return render(req, 'form.html', context={'form': form, 'form_title': "Modifier l'inventaire", 'curr_obj':curr_obj})


@login_required(login_url='login')
def populate_inventory(req, pk):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')
    
    inventory = get_object_or_404(Inventory, id=pk)

    if req.method == 'POST':
        formset = InventoryFormSet(req.POST, instance=inventory)
        if formset.is_valid():
            formset.save()
            messages.success(req, "Inventory updated successfully!")
            return HttpResponse(status=204, headers={'HX-Trigger': 'db_changed'})
        else:
            messages.error(req, "Form submission failed. Please correct the errors and try again.")
    else:
        formset = InventoryFormSet(instance=inventory)

    context = {
        'title': 'Products Inventory',
        'formset': formset,
        'form_title': "Ajouter un produit à cet inventaire"
    }
    return render(req, 'base/partials/stock/inventory_formset.html', context)

# ------------------------------------------------- Finances -------------------------------------------------

def finances(req):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')
    if not user.is_superuser:
        store = get_object_or_404(Store, id=user.profile.store.id)
        transactions = Transaction.objects.filter(store=store).order_by('-timestamp')
        credits = transactions.filter(type='credit')
        debits = transactions.filter(type='debit')
    else:
        store = Store.objects.all().order_by('name')
        transactions = Transaction.objects.all().order_by('-timestamp')
        credits = transactions.filter(type='credit')
        debits = transactions.filter(type='debit')

    credits_aggregate = credits.aggregate(totals=Sum('amount'))['totals'] or 0
    debits_aggregate = debits.aggregate(totals=Sum('amount'))['totals'] or 0
    balance = credits_aggregate - debits_aggregate

    context = {
        "finances": "active",
        'title': 'Finances',
        'transactions': transactions,
        'credits': credits,
        'credits_aggregate': credits_aggregate,
        'debits': debits,
        'store': store,
        'debits_aggregate': debits_aggregate,
        'balance': balance,
    }
    return render(req, 'base/finances/index.html', context)


def credits_list(req):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')
    if not user.is_superuser:
        store = get_object_or_404(Store, id=user.profile.store.id)
        credits = Transaction.objects.filter(store=store, type='credit').order_by('-timestamp')
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
    if not user.is_superuser:
        store = get_object_or_404(Store, id=user.profile.store.id)
        debits = Transaction.objects.filter(store=store, type='debit').order_by('-timestamp')
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
    cashdesks = Cashdesk.objects.all()
    context = {
        'cashdesks': cashdesks,
    }
    return render(req, 'base/partials/parameters/cashdesks_list.html', context)


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
        return render(req, 'form.html', context={'form': form, 'form_title': 'Modifier cette caisse'})

from django.db.models import Sum

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
def edit_transaction(req,pk):
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
