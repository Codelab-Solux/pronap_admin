from .models import *
from .forms import *
from django.contrib import messages
from django.apps import apps
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import path, register_converter
from .views import *
from utils import HashIdConverter

register_converter(HashIdConverter, "hashid")

urlpatterns = [
    path('', home, name='home'),
    path('products/', products, name='products'),
    path('products/create/', create_product, name='create_product'),
    path('products/list/', products_list, name='products_list'),
    path('products/grid/', products_grid, name='products_grid'),
    path('products/filter/', filter_products, name='filter_products'),
    path('products/<hashid:pk>/', product_details, name='product_details'),
    path('products/<hashid:pk>/edit/', edit_product, name='edit_product'),
    path('stock/products/', products_stock, name='products_stock'),
    path('stock/products/create/', create_product_stock, name='create_product_stock'),
    path('stock/products/filter/', filter_products_stock, name='filter_products_stock'),
    path('stock/products/<hashid:pk>/edit/',
         edit_product_stock, name='edit_product_stock'),
    path('stock/', stock, name='stock'),
    path('stock/inputs/', stock_inputs, name='stock_inputs'),
    path('stock/inputs/create/', create_stock_input, name='create_stock_input'),
    path('stock/outputs/', stock_outputs, name='stock_outputs'),
    path('stock/outputs/create/', create_stock_output, name='create_stock_output'),
    path('stock/inventories/', stock_inventories, name='stock_inventories'),
    path('stock/inventories/create/', create_inventory, name='create_inventory'),
    path('stock/overview/', stock_overview, name='stock_overview'),
    # ----------------------------------------------------------------------------
    path('cart/', cart, name='cart'),
    path('sales/pos/add_item/', add_to_cart, name='add_to_cart'),
    path('sales/pos/remove_item/', remove_from_cart, name='remove_from_cart'),
    path('sales/pos/clear_item/', clear_item, name='clear_item'),
    path('sales/pos/clear/', clear_cart, name='clear_cart'),
    path('sales/pos/checkout/', checkout, name='checkout'),
    # ----------------------------------------------------------------------------
    path('sales/', sales, name='sales'),
    path('sales/pos/', sale_point, name='sale_point'),
    path('sales/<hashid:pk>/', sale_details, name='sale_details'),
    path('sales/<hashid:pk>/edit/',edit_sale, name='edit_sale'),
    # ----------------------------------------------------------------------------
    path('purchases/', purchases, name='purchases'),
    path('purchases/product/create/', create_prod_purchase, name='create_prod_purchase'),
    path('purchases/product/list/', prod_purchases_list, name='prod_purchases_list'),
    path('purchases/service/create/', create_serv_purchase, name='create_serv_purchase'),
    path('purchases/service/list/', serv_purchases_list, name='serv_purchases_list'),
    path('purchases/service/<hashid:pk>/edit/', edit_service_purchase, name='edit_service_purchase'),
#     path('purchases/list/', purchases_list, name='purchases_list'),
#     path('purchases/filter/', filter_purchases, name='filter_purchases'),
#     path('purchases/<hashid:pk>/', purchase_details, name='purchase_details'),
#     path('purchases/<hashid:pk>/edit/', edit_purchase, name='edit_purchase'),
    # ----------------------------------------------------------------------------
    path('stock/', stock, name='stock'),
    # ----------------------------------------------------------------------------
    path('clients/', clients, name='clients'),
    path('clients/create/', create_client, name='create_client'),
    path('clients/list/', clients_list, name='clients_list'),
    # ----------------------------------------------------------------------------
    path('staff/', staff, name='staff'),
    path('staff/grid/', staff_grid, name='staff_grid'),
    path('staff/list/', staff_list, name='staff_list'),
    path('staff/<hashid:pk>/', staff_details, name='staff_details'),
    # ----------------------------------------------------------------------------
    path('suppliers/', suppliers, name='suppliers'),
    path('suppliers/create/', create_supplier, name='create_supplier'),
    path('suppliers/list/', suppliers_list, name='suppliers_list'),
    path('suppliers/<hashid:pk>/', supplier_details, name='supplier_details'),
    path('suppliers/<hashid:pk>/edit/', edit_supplier, name='edit_supplier'),
    # ----------------------------------------------------------------------------
    path('parameters/', parameters, name='parameters'),
    path('categories/list/', categories_list, name='categories_list'),
    path('categories/add/', create_category, name='create_category'),
    path('categories/<hashid:pk>/edit/', edit_category, name='edit_category'),
    # --------------------------
    path('families/load/', load_families, name='load_families'),
    path('families/list/', families_list, name='families_list'),
    path('families/add/', create_family, name='create_family'),
    path('families/<hashid:pk>/edit/',
         edit_family, name='edit_family'),
    # --------------------------
    path('finances/', finances, name='finances'),
    path('finances/reports/', reports, name='reports'),
    path('finances/treasury/', treasury, name='treasury'),
    # --------------------------
    path('base/objects/<hashid:pk>/<str:model_name>/delete/',
         delete_base_object, name='delete_base_object'),
]
