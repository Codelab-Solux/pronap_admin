import logging
from django.contrib import messages
from django.apps import apps
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
# from django.forms import inlineformset_factory
from django.db.models import Q
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
def products_stock(req):

    products = ProductStock.objects.all().order_by('product__name')

    context = {
        'products': products,
    }
    return render(req, 'base/partials/products_stock.html', context)


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
def create_product_stock(req):
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
def edit_product_stock(req, pk):
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
def filter_products_stock(req):
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

    return render(req, 'base/partials/products_stock.html', context)


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
    context = {
        'cart_count': cart_count,
        'cart_items': cart_items,
        'cart_total': cart_total,
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
        # client = Client(full_name=req.POST.get(
        #     'full_name'), sex=req.POST.get('sex'))
        # Create a new order
        # new_sale = Sale(client=client, items=cart_count, total=cart_total)
        new_sale = Sale(seller=user, items=cart_count, total=cart_total)
        new_sale.save()

        for item in cart_items:
            # if 'product_stock' not in item or 'quantity' not in item:
            #     logger.error(f'Missing keys in cart item: {item}')
            #     messages.error(
            #         req, 'Error processing your cart items. Please try again.')
            #     return HttpResponseRedirect(req.META.get('HTTP_REFERER'))

            product_stock = item['product']
            quantity = item['quantity']

            print(product_stock.product.name)
            print(quantity)



            new_sale_item = SaleItem(
                sale=new_sale,
                product_stock=product_stock,
                quantity=quantity,
            )
            new_sale_item.save()

        cart.clear_cart()
        messages.success(req, 'Nouvelle vente éffectuée!')
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
    cashdesks = Cashdesk.objects.all()
    buyers = Client.objects.all()
    sellers = CustomUser.objects.all()
    product_stocks = ProductStock.objects.all()
    sales = Sale.objects.all().order_by('-timestamp')

    objects = paginate_objects(req, sales)

    context = {
        "sales": "active",
        'title': 'Ventes',
        'objects': objects,
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
    context = {
        "sales": "active",
        'title': 'sale Details',
        'curr_obj': curr_obj,
        'sale_items': sale_items,
    }
    return render(req, 'base/edit_sale.html', context)


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
    context = {
        "purchases": "active",
        'title': "Details d'Achat",
        'curr_obj': curr_obj,
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
def edit_prod_purchase(req, pk):
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
        messages.success = 'Nouveau cliente ajouté'
        return HttpResponse(status=204, headers={'HX-Trigger': 'db_changed'})
    else:
        return render(req, 'form.html', context={'form': form, 'form_title': 'Nouveau client'})


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
    personel = CustomUser.objects.filter(is_staff=True)
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


def load_families(request):
    category_id = request.GET.get('category')
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


def input_details(req,pk):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')
    curr_obj = get_object_or_404(StockInput, id=pk)
    context = {
        "stock": "active",
        'title': "Details d'Entrée",
        'curr_obj': curr_obj,
    }
    return render(req, 'base/partials/stock/input_details.html', context)



def create_stock_input(req):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')

    if req.method == 'POST':
        form = StockInputForm(req.POST)
        form.instance.initiator=user
        # formset = ProductStockFormSet(req.POST)
        print(form.instance.initiator)
        if form.is_valid():  #and formset.is_valid():
            new_stockinput = form.save(commit=False)
            new_stockinput.initiator = user
            new_stockinput.save()
            # formset.instance = new_stockinput
            # formset.save()
            messages.success(req, 'Nouveau produits ajoutés')
            return redirect('stock')
        else:
            if not form.is_valid():
                logger.error(f"StockInputForm errors: {form.errors}")
            # if not formset.is_valid():
                # logger.error(f"ProductStockFormSet errors: {formset.errors}")
            messages.error(
                req, 'There were errors in the form. Please correct them and try again.')
    else:
        form = StockInputForm()
        # formset = ProductStockFormSet()

    context = {
        'title': 'Entrées',
        'active': 'Stock',
        'form': form,
        # # 'formset': formset,
        'form_title': 'Ajouter un nouveau produit au stock'
    }
    return render(req, 'base/partials/stock/stock_form.html', context)




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


def output_details(req,pk):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')
    curr_obj = get_object_or_404(StockOutput, id=pk)
    context = {
        "stock": "active",
        'title': "Details d'Entrée",
        'curr_obj': curr_obj,
    }
    return render(req, 'base/partials/stock/output_details.html', context)


def create_stock_output(req):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')

    if req.method == 'POST':
        form = StockOutputForm(req.POST)
        form.instance.initiator = user
        # formset = ProductStockFormSet(req.POST)
        print(form.instance.initiator)
        if form.is_valid():  #and formset.is_valid():
            new_stockinput = form.save(commit=False)
            new_stockinput.initiator = user
            new_stockinput.save()
            # formset.instance = new_stockinput
            # formset.save()
            messages.success(req, 'Nouveau produits enlevés')
            return redirect('stock')
        else:
            if not form.is_valid():
                logger.error(f"StockOutputForm errors: {form.errors}")
            # if not formset.is_valid():
                # logger.error(f"ProductStockFormSet errors: {formset.errors}")
            messages.error(
                req, 'There were errors in the form. Please correct them and try again.')
    else:
        form = StockOutputForm()
        # formset = ProductStockFormSet()

    context = {
        'title': 'Sorties',
        'active': 'Stock',
        'form': form,
        # # 'formset': formset,
        'form_title': 'Enlever un produit du stock'
    }
    return render(req, 'base/partials/stock/stock_form.html', context)


def stock_inventories(req):
    inventories = Inventory.objects.all().order_by('-date')
    context = {
        "inventories": inventories
    }
    return render(req, 'base/partials/stock/inventories.html', context)


def inventory_details(req,pk):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')
    curr_obj = get_object_or_404(Inventory, id=pk)
    context = {
        "stock": "active",
        'title': 'Inventaire',
        'curr_obj': curr_obj,
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

    if inventory and  req.method == 'POST':
        formset = InventoryFormSet(req.POST)

        if formset.is_valid():
            formset.instance.inventory = inventory
            formset.save()
            messages.success(req, "Inventory updated successfully!")
            return HttpResponse(status=204, headers={'HX-Trigger': 'db_changed'})
        else:
            messages.error(req, "Form submission failed. Please correct the errors and try again.")
            return HttpResponse(status=404, headers={'HX-Trigger': 'db_changed'})
    else:
        formset = InventoryFormSet()

    context = {
        'title': 'Products Inventory',
        'formset': formset,
        'form_title': "Ajouter un produit à cet inventaire"
    }
    return render(req, 'base/partials/stock/inventory_formset.html', context)


# ------------------------------------------------- Finances -------------------------------------------------

def finances(req):
    context = {
        "finances": "active",
        'title': 'Finances',
    }
    return render(req, 'base/finances.html', context)

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
