import datetime
from django.db import models
from django.urls import reverse
from datetime import date, timedelta
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from accounts.models import *
from utils import *

# ----------------------------------- Store -----------------------------------
store_types = (
    ('generic', "Generique"),
    ('pronap', "Pronap"),
)


class Store(models.Model):
    type = models.CharField(max_length=50, choices=store_types)
    manager = models.ForeignKey(
        CustomUser, blank=True, null=True, on_delete=models.SET_NULL, related_name='store_manager')
    workers = models.ManyToManyField(
        CustomUser, blank=True, related_name='store_workers')
    name = models.CharField(max_length=255, default='', null=True, blank=True)
    address = models.CharField(max_length=255, default='',)
    city = models.CharField(max_length=255, default='',)
    country = models.CharField(max_length=255, default='',)
    phone = models.CharField(max_length=255, default='',)
    description = models.CharField(max_length=500, blank=True, null=True)
    image = models.ImageField(upload_to='store/', blank=True, null=True)
    is_active = models.BooleanField(default=False)
    is_open = models.BooleanField(default=False)
    opening_time = models.TimeField(blank=True, null=True)
    closing_time = models.TimeField(blank=True, null=True)
    opening_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f'{self.name} - {self.address}'

    def get_hashid(self):
        return h_encode(self.id)

    def get_absolute_url(self):
        return reverse('store', kwargs={'pk': self.pk})


cashdesk_types = (
    ('cash', "Physique"),
    ('mobile', "Mobile"),
    ('bank', "Bancaire"),
)


class Cashdesk(models.Model):
    store = models.ForeignKey(Store, default=1, on_delete=models.CASCADE)
    type = models.CharField(max_length=50, choices=cashdesk_types)
    name = models.CharField(max_length=500)
    phone = models.CharField(max_length=500, blank=True, null=True)
    acc_number = models.CharField(max_length=500, blank=True, null=True)
    debits = models.IntegerField(default='0', blank=True, null=True)
    credits = models.IntegerField(default='0', blank=True, null=True)

    def get_balance(self):
        balance = self.credits - self.debits
        return balance

    def __str__(self):
        return f'{self.store.name} - Caisse {self.name}'

    def get_hashid(self):
        return h_encode(self.id)

    def get_absolute_url(self):
        return reverse('cashdesk', kwargs={'pk': self.pk})


transaction_types = (
    ('credit', "Encaissement"),
    ('debit', "Décaissement"),
)

audit_statuses = (
    ('pending', "En attente"),
    ('validated', "Validé"),
    ('rejected', "Rejeté"),
)



class Transaction(models.Model):
    initiator = models.ForeignKey(
        CustomUser, blank=True, null=True, on_delete=models.SET_NULL)
    store = models.ForeignKey(Store, default=1, on_delete=models.CASCADE)
    cashdesk = models.ForeignKey(
        Cashdesk, blank=True, null=True, on_delete=models.SET_NULL)
    type = models.CharField(
        max_length=50, choices=transaction_types)
    amount = models.IntegerField(default='0', blank=True, null=True)
    label = models.CharField(max_length=100, blank=True, null=True)
    description = models.CharField(max_length=500, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now=True)
    audit = models.CharField(
        max_length=50, choices=audit_statuses, default='pending')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()


    def __str__(self):
        return f'{self.initiator.last_name} - {self.store} - {self.amount}'

    def get_hashid(self):
        return h_encode(self.id)

    def get_origin(self):
        if self.content_type.model == "servicepurchase":
            obj = ServicePurchase.objects.get(id=self.object_id)
        elif self.content_type.model == "productpurchase":
            obj = ProductPurchase.objects.get(id=self.object_id)
        elif self.content_type.model == "sale":
            obj = Sale.objects.get(id=self.object_id)
        else:
            obj = None
        return obj

    def get_absolute_url(self):
        return reverse('transaction', kwargs={'pk': self.pk})


# ----------------------------------- Entities -----------------------------------


entity_types = (
    ('person', "Personne"),
    ('company', "Compagnie"),
)


class Supplier(models.Model):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    domain = models.CharField(max_length=255)
    is_new = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True,  blank=True, null=True)
    type = models.CharField(max_length=50, choices=entity_types, default='company')

    def __str__(self):
        return f'{self.name} - {self.type}'

    def get_hashid(self):
        return h_encode(self.id)

    def get_absolute_url(self):
        return reverse('supplier', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        if self.is_new and self.timestamp and timezone.now() > self.timestamp + timedelta(weeks=2):
            self.is_new = False
        super(Supplier, self).save(*args, **kwargs)


sexes = (
    ('male', "Masculin"),
    ('female', 'Féminin'),
    ('neutral', 'Neutre'),
)


class Client(models.Model):
    name = models.CharField(
        max_length=255, default='', null=True, blank=True)
    sex = models.CharField(max_length=50, default='neutral', choices=sexes)
    email = models.EmailField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=255, default='', blank=True, null=True)
    address = models.CharField( max_length=255, default='', blank=True, null=True)
    timestamp = models.DateTimeField(auto_now=True)
    type = models.CharField(max_length=50, choices=entity_types, default='company')

    def __str__(self):
        return f'{self.name} - {self.sex}'

    def get_hashid(self):
        return h_encode(self.id)

    def get_absolute_url(self):
        return reverse('client', kwargs={'pk': self.pk})


# ----------------------------------- Products -----------------------------------
class Category(models.Model):
    name = models.CharField(max_length=100)
    is_featured = models.BooleanField(default=False)
    image = models.ImageField(
        upload_to='store/categories/', blank=True, null=True)

    def __str__(self):
        return self.name

    def get_hashid(self):
        return h_encode(self.id)

    def get_absolute_url(self):
        return reverse('prod_category', kwargs={'pk': self.pk})


class Family(models.Model):
    category = models.ForeignKey(
        Category, blank=True, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=255, default='', null=True, blank=True)

    def __str__(self):
        return self.name

    def get_hashid(self):
        return h_encode(self.id)

    def get_absolute_url(self):
        return reverse('prod_family', kwargs={'pk': self.pk})
    

class Lot(models.Model):
    name = models.CharField(max_length=255, default='', null=True, blank=True)
    date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name

    def get_hashid(self):
        return h_encode(self.id)

    def get_absolute_url(self):
        return reverse('prod_lot', kwargs={'pk': self.pk})


unit_types = (
    ('Kg', "Kilos"),
    ('L', "Litres"),
    ('Ut', "Unités"),
)


class Product(models.Model):
    store = models.ForeignKey(Store, default=1, on_delete=models.CASCADE)
    name = models.CharField(max_length=256)
    brand = models.CharField(max_length=256, default='Générique')
    category = models.ForeignKey(
        Category, blank=True, null=True, on_delete=models.SET_NULL)
    family = models.ForeignKey(
        Family, blank=True, null=True, on_delete=models.SET_NULL)
    unit = models.CharField(max_length=50, choices=unit_types)
    description = models.CharField(max_length=500, blank=True, null=True)
    is_favorite = models.BooleanField(default=False)
    is_new = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    image = models.ImageField(
        upload_to='store/products/', blank=True, null=True)

    def __str__(self):
        return f'{self.name} - {self.unit}'

    def get_hashid(self):
        return h_encode(self.id)

    def get_absolute_url(self):
        return reverse('product', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        if self.is_new and self.timestamp and timezone.now() > self.timestamp + timedelta(weeks=2):
            self.is_new = False
        super(Product, self).save(*args, **kwargs)


class ProductStock(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    supplier = models.ForeignKey(
        Supplier, default=1, blank=True, null=True, on_delete=models.SET_NULL)
    lot = models.IntegerField(default=0, blank=True, null=True)
    quantity = models.IntegerField(default=0, blank=True, null=True)
    price = models.IntegerField(default=0, blank=True, null=True)
    promo_price = models.IntegerField(default=0, blank=True, null=True)
    is_promoted = models.BooleanField(default=False)
    observation = models.CharField(max_length=500, blank=True, null=True)
    production_date = models.DateField(null=True, blank=True)
    expiration_date = models.DateField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return f'{self.product.name} - {self.quantity}'

    def get_hashid(self):
        return h_encode(self.id)

    def get_absolute_url(self):
        return reverse('product_stock', kwargs={'pk': self.pk})

# ----------------------------------- Sales -----------------------------------

class Sale(models.Model):
    store = models.ForeignKey(Store, default=1, on_delete=models.CASCADE)
    buyer = models.ForeignKey(Client, default=1, on_delete=models.CASCADE)
    seller = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product_stocks = models.ManyToManyField(ProductStock, through='SaleItem')
    cashdesk = models.ForeignKey(Cashdesk, default=1, blank=True, null=True, on_delete=models.SET_NULL)
    audit = models.CharField(max_length=50, choices=audit_statuses, default='pending')
    items = models.IntegerField(default=0)
    total = models.IntegerField(default=0)
    discount = models.IntegerField(default=0, blank=True, null=True)
    observation = models.CharField(max_length=500, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Vente : {self.total} - Caisse : {self.cashdesk}'

    def calculate_total(self):
        self.total = sum(item.get_total for item in self.saleitem_set.all())
        self.items = self.saleitem_set.count()
        self.save()

    def get_hashid(self):
        return h_encode(self.id)


class SaleItem(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.SET_NULL, null=True)
    product_stock = models.ForeignKey(ProductStock, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField(default=0)

    @property
    def get_total(self):
        total = self.product_stock.price * self.quantity
        return total

    def __str__(self):
        return f'Vente de {self.quantity} {self.product_stock.product.unit} de {self.product_stock.product.name}'

    def get_hashid(self):
        return h_encode(self.id)


# ----------------------------------- Purchases -----------------------------------

purchase_payment_options = (
    ('bank', "Banque"),
    ('cash', "Espèce"),
    ('mobil', "Mobile"),
)

purchase_payment_statuses = (
    ('unpaid', "Impayé"),
    ('partly_paid', "Payé en partie"),
    ('paid', "Payé en totalité"),
)


class ProductPurchase(models.Model):
    store = models.ForeignKey(Store, default=1, on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, default=1, blank=True, null=True, on_delete=models.SET_NULL)
    cashdesk = models.ForeignKey(Cashdesk, default=1, blank=True, null=True, on_delete=models.SET_NULL)
    product_stocks = models.ManyToManyField(ProductStock, through='PurchaseItem')
    audit = models.CharField(max_length=50, choices=audit_statuses, default='pending')
    payment_option = models.CharField(max_length=50, choices=purchase_payment_options, default='cash')
    payment_status = models.CharField(max_length=50, choices=purchase_payment_statuses, default='unpaid')
    label = models.CharField(max_length=200, default='Achat de produit(s)', blank=True, null=True)
    total = models.IntegerField(default=0)
    amount_paid = models.IntegerField(default=0, blank=True, null=True)
    observation = models.CharField(max_length=500, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Achat : {self.total} - Caisse : {self.cashdesk}'

    def calculate_total(self):
        self.total = sum(item.get_total for item in self.purchaseitem_set.all())
        self.save()

    def get_hashid(self):
        return h_encode(self.id)


class PurchaseItem(models.Model):
    purchase = models.ForeignKey(ProductPurchase, on_delete=models.SET_NULL, null=True)
    product_stock = models.ForeignKey(ProductStock, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField(default=0)

    @property
    def get_total(self):
        total = self.product_stock.price * self.quantity
        return total

    def __str__(self):
        return f'Achat de {self.quantity} {self.product_stock.product.unit} de {self.product_stock.product.name}'

    def get_hashid(self):
        return h_encode(self.id)


class ServicePurchase(models.Model):
    store = models.ForeignKey(Store, default=1, on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, default=1, blank=True, null=True, on_delete=models.SET_NULL)
    cashdesk = models.ForeignKey(Cashdesk, default=1, blank=True, null=True, on_delete=models.SET_NULL)
    audit = models.CharField(max_length=50, choices=audit_statuses, default='pending')
    payment_option = models.CharField(max_length=50, choices=purchase_payment_options, default='cash')
    payment_status = models.CharField(max_length=50, choices=purchase_payment_statuses, default='unpaid')
    label = models.CharField(max_length=200, default='Achat de service(s)', blank=True, null=True)
    description = models.CharField(max_length=200, blank=True, null=True)
    total = models.PositiveIntegerField(default=0)
    amount_paid = models.IntegerField(default=0, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Achat de service(s) {self.label} : {self.total} - Caisse : {self.cashdesk}'

    def get_hashid(self):
        return h_encode(self.id)


# ----------------------------------- Stock -----------------------------------
stock_input_types = (
    ('purchase', "Achat"),
    ('return', "Retour"),
    ('transfer', "Transfer"),
    ('difference', "Difference d’inventaire"),
    ('gift', "Cadeau"),
)


class StockInput(models.Model):
    initiator = models.ForeignKey(
        CustomUser, on_delete=models.SET_NULL, blank=True, null=True)
    type = models.CharField(
        max_length=50, choices=stock_input_types, default='purchase')
    product_stocks = models.ManyToManyField(
        ProductStock, through='StockInputItem')
    description = models.CharField(max_length=200, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.initiator} - {self.type} - {self.description}'

    def get_hashid(self):
        return h_encode(self.id)
    


class StockInputItem(models.Model):
    stock_input = models.ForeignKey(StockInput, on_delete=models.CASCADE)
    product_stock = models.ForeignKey(ProductStock, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'Entrée de {self.quantity} {self.product_stock.product.unit} de {self.product_stock.product.name}'

    def get_hashid(self):
        return h_encode(self.id)


stock_output_types = (
    ('sale', "Vente"),
    ('usage', "Utilisation interne"),
    ('transfer', "Transfer"),
    ('difference', "Difference d’inventaire"),
    ('gift', "Don"),
)


class StockOutput(models.Model):
    initiator = models.ForeignKey(
        CustomUser, on_delete=models.SET_NULL, blank=True, null=True)
    type = models.CharField(
        max_length=50, choices=stock_output_types, default='sale')
    product_stocks = models.ManyToManyField(
        ProductStock, through='StockOutputItem')
    description = models.CharField(max_length=500, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.initiator} - {self.type} - {self.description}'

    def get_hashid(self):
        return h_encode(self.id)
    

class StockOutputItem(models.Model):
    stock_output = models.ForeignKey(StockOutput, on_delete=models.CASCADE)
    product_stock = models.ForeignKey(ProductStock, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'Sortie de {self.quantity} {self.product_stock.product.unit} de {self.product_stock.product.name}'

    def get_hashid(self):
        return h_encode(self.id)


# ----------------------------------- Inventory -----------------------------------
class Inventory(models.Model):
    date = models.DateField(default=datetime.date.today)
    initiator = models.ForeignKey(
        CustomUser,  on_delete=models.SET_NULL, blank=True, null=True, related_name='initiator')
    supervisor = models.ForeignKey(
        CustomUser, on_delete=models.SET_NULL, blank=True, null=True, related_name='supervisor')
    is_valid = models.BooleanField(default=False)
  

    def __str__(self):
        return f'{self.initiator.last_name} - {self.date}'

    def get_hashid(self):
        return h_encode(self.id)
    

class InventoryItem(models.Model):
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    product_stock = models.ForeignKey(
        ProductStock, on_delete=models.SET_NULL, blank=True, null=True)
    quantity_expected = models.PositiveIntegerField(default=0)
    quantity_found = models.PositiveIntegerField(default=0)
    comment = models.CharField(max_length=500, blank=True, null=True)

    @property
    def get_difference(self):
        difference = self.quantity_expected - self.quantity_found
        return difference
  
    def __str__(self):
        return f'{self.product_stock.product.name} - {self.get_difference}'

    def get_hashid(self):
        return h_encode(self.id)
