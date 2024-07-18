import datetime
from django.db import models
from django.urls import reverse
from datetime import date, timedelta
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from accounts.models import *
from utils import *

# ----------------------------------- Entities -----------------------------------


class EntityType(models.Model):
    name = models.CharField(
        max_length=255, default='', null=True, blank=True)
    description = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return f'{self.name}'

    def get_hashid(self):
        return h_encode(self.id)

    @property
    def model_name(self):
        return self.__class__.__name__

    def get_absolute_url(self):
        return reverse('entity_details', kwargs={'pk': self.pk})


class Supplier(models.Model):
    name = models.CharField(max_length=255)
    phone = models.CharField(
        unique=True, max_length=255, blank=True, null=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    address = models.CharField(max_length=255)
    domain = models.CharField(max_length=255)
    is_new = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True,  blank=True, null=True)
    type = models.ForeignKey(EntityType, blank=True,
                             null=True, on_delete=models.SET_NULL)
    description = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return f'{self.name} - {self.phone}'

    def get_hashid(self):
        return h_encode(self.id)

    @property
    def model_name(self):
        return self.__class__.__name__

    def get_absolute_url(self):
        return reverse('supplier_details', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        if self.is_new and self.timestamp and timezone.now() > self.timestamp + timedelta(weeks=2):
            self.is_new = False
        super(Supplier, self).save(*args, **kwargs)


class Client(models.Model):
    name = models.CharField(
        max_length=255, default='', null=True, blank=True)
    phone = models.CharField(
        unique=True, max_length=255, blank=True, null=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now=True)
    type = models.ForeignKey(EntityType, blank=True,
                             null=True, on_delete=models.SET_NULL)
    description = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return f'{self.name} - {self.phone}'

    def get_hashid(self):
        return h_encode(self.id)

    @property
    def model_name(self):
        return self.__class__.__name__

    def get_absolute_url(self):
        return reverse('client_details', kwargs={'pk': self.pk})


# ----------------------------------- Store -----------------------------------

store_types = (
    ('generic', "Generique"),
    ('pronap', "Pronap"),
)


class Store(models.Model):
    type = models.CharField(max_length=50, choices=store_types)
    manager = models.ForeignKey(
        CustomUser, blank=True, null=True, on_delete=models.SET_NULL, related_name='store_manager')
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

    @property
    def model_name(self):
        return self.__class__.__name__

    def get_absolute_url(self):
        return reverse('store_details', kwargs={'pk': self.pk})


# ----------------------------------- Finances -----------------------------------

cashdesk_types = (
    ('cash', "Physique"),
    ('mobile', "Mobile"),
    ('bank', "Bancaire"),
)

carrier_types = (
    ('moov', "Moov Africa"),
    ('togocom', "Togocom"),
)


class Cashdesk(models.Model):
    store = models.ForeignKey(
        Store, blank=True, null=True, on_delete=models.SET_NULL)
    type = models.CharField(max_length=50, choices=cashdesk_types)
    carrier = models.CharField(
        max_length=50, choices=carrier_types, blank=True, null=True)
    name = models.CharField(max_length=500)
    phone = models.CharField(max_length=500, blank=True, null=True)
    acc_number = models.CharField(max_length=500, blank=True, null=True)
    debits = models.PositiveIntegerField(default=0, blank=True, null=True)
    credits = models.PositiveIntegerField(default=0, blank=True, null=True)
    balance = models.IntegerField(default=0, blank=True, null=True)

    def calculate_balance(self):
        return abs(self.credits - self.debits)

    def save(self, *args, **kwargs):
        self.balance = self.calculate_balance()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Caisse {self.name}'

    def get_hashid(self):
        return h_encode(self.id)

    @property
    def model_name(self):
        return self.__class__.__name__

    def get_absolute_url(self):
        return reverse('cashdesk_details', kwargs={'pk': self.pk})


class CashdeskClosing(models.Model):
    initiator = models.ForeignKey(
        CustomUser, on_delete=models.SET_NULL, blank=True, null=True, related_name='cashdesk_initiator')
    supervisor = models.ForeignKey(
        CustomUser, on_delete=models.SET_NULL, blank=True, null=True, related_name='cashdesk_supervisor')
    cashdesk = models.ForeignKey(Cashdesk, on_delete=models.CASCADE)
    balance_expected = models.BigIntegerField(default=0, blank=True, null=True)
    balance_found = models.BigIntegerField(default=0, blank=True, null=True)
    difference = models.BigIntegerField(default=0)
    comment = models.CharField(max_length=500, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.pk is None:
            # First save to get the primary key assigned
            super().save(*args, **kwargs)

        self.balance_expected = self.cashdesk.balance  # Use balance from Cashdesk
        self.balance_found = sum(
            item.total_amount for item in self.closingcashreceipt_set.all())
        self.difference = abs(self.balance_expected - self.balance_found)

        # Save again to update balance_found and difference
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.cashdesk.name} - (écart : {self.difference} Cfa)'

    def get_hashid(self):
        return h_encode(self.id)

    @property
    def model_name(self):
        return self.__class__.__name__


cash_receipt_types = (
    ('notes', "Billets"),
    ('coins', "Pièces"),
)


class CashReceipt(models.Model):
    name = models.CharField(max_length=255)
    value = models.PositiveIntegerField()
    type = models.CharField(max_length=50, choices=cash_receipt_types)

    def __str__(self):
        return f'{self.name} - {self.type}'

    def get_hashid(self):
        return h_encode(self.id)

    @property
    def model_name(self):
        return self.__class__.__name__

    def get_absolute_url(self):
        return reverse('cash_receipt', kwargs={'pk': self.pk})


class ClosingCashReceipt(models.Model):
    cashdesk_closing = models.ForeignKey(
        CashdeskClosing, on_delete=models.CASCADE)
    cash_receipt = models.ForeignKey(CashReceipt, on_delete=models.CASCADE)
    count = models.PositiveIntegerField(default=0)
    total_amount = models.PositiveIntegerField(default=0)
    timestamp = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.total_amount = self.cash_receipt.value * self.count
        super().save(*args, **kwargs)
        self.update_cashdesk_closing()

    def update_cashdesk_closing(self):
        cashdesk_closing = self.cashdesk_closing
        cashdesk_closing.balance_found = sum(
            item.total_amount for item in cashdesk_closing.closingcashreceipt_set.all())
        cashdesk_closing.save()

    def delete(self, *args, **kwargs):
        cashdesk_closing = self.cashdesk_closing
        super().delete(*args, **kwargs)
        cashdesk_closing.balance_found = sum(
            item.total_amount for item in cashdesk_closing.closingcashreceipt_set.all())
        cashdesk_closing.save()

    def __str__(self):
        return f'{self.count} - {self.cash_receipt}'

    def get_hashid(self):
        return h_encode(self.id)

    @property
    def model_name(self):
        return self.__class__.__name__


class Payment(models.Model):
    initiator = models.ForeignKey(
        CustomUser, blank=True, null=True, on_delete=models.SET_NULL)
    store = models.ForeignKey(Store, default=1, on_delete=models.CASCADE)
    cashdesk = models.ForeignKey(
        Cashdesk, blank=True, null=True, on_delete=models.SET_NULL)
    amount = models.PositiveIntegerField(default='0', blank=True, null=True)
    label = models.CharField(max_length=100, blank=True, null=True)
    description = models.CharField(max_length=500, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now=True)
    content_type = models.ForeignKey(
        ContentType, blank=True, null=True, on_delete=models.SET_NULL)
    object_id = models.PositiveIntegerField(blank=True, null=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return f'{self.initiator} - {self.amount} CFA'

    def get_hashid(self):
        return h_encode(self.id)

    @property
    def model_name(self):
        return self.__class__.__name__

    def get_absolute_url(self):
        return reverse('payment_details', kwargs={'pk': self.pk})


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
    payment = models.ForeignKey(Payment, default=1, on_delete=models.CASCADE)
    type = models.CharField(max_length=50, choices=transaction_types)
    amount = models.PositiveIntegerField(default='0', blank=True, null=True)
    label = models.CharField(max_length=100, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now=True)
    audit = models.CharField(
        max_length=50, choices=audit_statuses, default='pending')

    def __str__(self):
        return f'{self.payment.store} - {self.amount}'

    def get_hashid(self):
        return h_encode(self.id)

    @property
    def model_name(self):
        return self.__class__.__name__


    def get_absolute_url(self):
        return reverse('transaction_details', kwargs={'pk': self.pk})


class Receivable(models.Model):
    sale = models.ForeignKey('Sale', on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    amount = models.IntegerField(default=0)
    label = models.CharField(max_length=100, blank=True, null=True)
    due_date = models.DateField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    content_type = models.ForeignKey(
        ContentType, blank=True, null=True, on_delete=models.SET_NULL)
    object_id = models.PositiveIntegerField(blank=True, null=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    is_fully_paid = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.client} owes {self.amount}'

    def get_hashid(self):
        return h_encode(self.id)

    @property
    def model_name(self):
        return self.__class__.__name__

    def get_absolute_url(self):
        return reverse('receivable_details', kwargs={'pk': self.pk})


class Debt(models.Model):
    initiator = models.ForeignKey(
        CustomUser, blank=True, null=True, on_delete=models.SET_NULL)
    store = models.ForeignKey(Store, default=1, on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    amount = models.IntegerField(default=0)
    label = models.CharField(max_length=100, blank=True, null=True)
    description = models.CharField(max_length=500, blank=True, null=True)
    due_date = models.DateField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    content_type = models.ForeignKey(
        ContentType, blank=True, null=True, on_delete=models.SET_NULL)
    object_id = models.PositiveIntegerField(blank=True, null=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    is_fully_paid = models.BooleanField(default=False)

    def __str__(self):
        return f'Owes {self.supplier} {self.amount}'

    def get_hashid(self):
        return h_encode(self.id)

    @property
    def model_name(self):
        return self.__class__.__name__

    def get_absolute_url(self):
        return reverse('debt_details', kwargs={'pk': self.pk})


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

    @property
    def model_name(self):
        return self.__class__.__name__

    def get_absolute_url(self):
        return reverse('prod_category_details', kwargs={'pk': self.pk})


class Family(models.Model):
    category = models.ForeignKey(
        Category, blank=True, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=255, default='', null=True, blank=True)

    def __str__(self):
        return self.name

    def get_hashid(self):
        return h_encode(self.id)

    @property
    def model_name(self):
        return self.__class__.__name__

    def get_absolute_url(self):
        return reverse('prod_family_details', kwargs={'pk': self.pk})


class Lot(models.Model):
    store = models.ForeignKey(
        Store, blank=True, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=255, default='', null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Lot {self.name} - {self.store.name}'

    def get_hashid(self):
        return h_encode(self.id)

    @property
    def model_name(self):
        return self.__class__.__name__

    def get_absolute_url(self):
        return reverse('prod_lot_details', kwargs={'pk': self.pk})


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

    @property
    def model_name(self):
        return self.__class__.__name__

    def get_absolute_url(self):
        return reverse('product_details', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        if self.is_new and self.timestamp and timezone.now() > self.timestamp + timedelta(weeks=2):
            self.is_new = False
        super(Product, self).save(*args, **kwargs)


class ProductStock(models.Model):
    lot = models.ForeignKey(
        Lot, blank=True, null=True, on_delete=models.SET_NULL)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    supplier = models.ForeignKey(
        Supplier, default=1, blank=True, null=True, on_delete=models.SET_NULL)
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

    @property
    def model_name(self):
        return self.__class__.__name__

    def get_absolute_url(self):
        return reverse('product_stock_details', kwargs={'pk': self.pk})


# ----------------------------------- Sales -----------------------------------
payment_options = (
    ('bank', "Banque"),
    ('cash', "Espèce"),
    ('mobil', "Mobile"),
)

payment_statuses = (
    ('unpaid', "Impayé"),
    ('partly_paid', "Payé en partie"),
    ('paid', "Payé en totalité"),
)

class Sale(models.Model):
    store = models.ForeignKey(
        Store, default=1, blank=True, null=True, on_delete=models.SET_NULL)
    initiator = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, default=1, on_delete=models.CASCADE)
    product_stocks = models.ManyToManyField(ProductStock, through='SaleItem')
    cashdesk = models.ForeignKey(
        Cashdesk, default=1, blank=True, null=True, on_delete=models.SET_NULL)
    audit = models.CharField(
        max_length=50, choices=audit_statuses, default='pending')
    items = models.IntegerField(default=0)
    total = models.IntegerField(default=0)
    total_paid = models.IntegerField(default=0)
    discount = models.IntegerField(default=0, blank=True, null=True)
    observation = models.CharField(max_length=500, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Vente : {self.total} - Caisse : {self.cashdesk}'

    @property
    def total_due(self):
        return self.total - self.total_paid

    def calculate_total(self):
        self.total = sum(item.get_total for item in self.saleitem_set.all())
        self.items = self.saleitem_set.count()
        self.save()

    def get_hashid(self):
        return h_encode(self.id)

    @property
    def model_name(self):
        return self.__class__.__name__


class SaleItem(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.SET_NULL, null=True)
    product_stock = models.ForeignKey(
        ProductStock, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField(default=0)

    @property
    def get_total(self):
        total = self.product_stock.price * self.quantity
        return total

    def __str__(self):
        return f'Vente de {self.quantity} {self.product_stock.product.unit} de {self.product_stock.product.name}'

    def get_hashid(self):
        return h_encode(self.id)

    @property
    def model_name(self):
        return self.__class__.__name__


# ----------------------------------- Purchases -----------------------------------
purchase_types = (
    ('product', "Produit"),
    ('service', "Service"),
)


class Purchase(models.Model):
    initiator = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    store = models.ForeignKey(Store, default=1, on_delete=models.CASCADE)
    supplier = models.ForeignKey(
        Supplier, default=1, blank=True, null=True, on_delete=models.SET_NULL)
    cashdesk = models.ForeignKey(
        Cashdesk, default=1, blank=True, null=True, on_delete=models.SET_NULL)
    type = models.CharField(
        max_length=10, choices=purchase_types, default='product')
    product_stocks = models.ManyToManyField(
        ProductStock, through='PurchaseItem', blank=True)
    audit = models.CharField(
        max_length=50, choices=audit_statuses, default='pending')
    payment_option = models.CharField(
        max_length=50, choices=payment_options, default='cash')
    payment_status = models.CharField(
        max_length=50, choices=payment_statuses, default='unpaid')
    label = models.CharField(
        max_length=200, default='Achat', blank=True, null=True)
    total = models.IntegerField(default=0)
    amount = models.IntegerField(default=0, blank=True, null=True)
    description = models.CharField(max_length=500, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Achat : {self.label} - Total : {self.total} - Caisse : {self.cashdesk}'

    def calculate_total(self):
        self.total = sum(
            item.get_total for item in self.purchaseitem_set.all())
        self.save()

    def get_hashid(self):
        return h_encode(self.id)

    @property
    def model_name(self):
        return self.__class__.__name__


class PurchaseItem(models.Model):
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE)
    product_stock = models.ForeignKey(
        ProductStock, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=0)
    price = models.PositiveIntegerField(default=0)

    @property
    def get_total(self):
        total = self.price * self.quantity
        return total

    def __str__(self):
        if self.product_stock:
            return f'Achat de {self.quantity} {self.product_stock.product.unit} de {self.product_stock.product.name}'
        return f'Achat de service - {self.purchase.label}'

    def get_hashid(self):
        return h_encode(self.id)

    @property
    def model_name(self):
        return self.__class__.__name__

# ----------------------------------- Stock -----------------------------------
operation_types = (
    ('input', "Entrée"),
    ('output', "Sortie"),
)

operation_subtypes = (
    ('purchase', "Achat"),
    ('return', "Retour"),
    ('transfer', "Transfer"),
    ('difference', "Difference d’inventaire"),
    ('gift', "Cadeau/Don"),
    ('sale', "Vente"),
    ('usage', "Utilisation interne"),
)


class StockOperation(models.Model):
    store = models.ForeignKey(
        Store, on_delete=models.SET_NULL, blank=True, null=True)
    initiator = models.ForeignKey(
        CustomUser, on_delete=models.SET_NULL, blank=True, null=True)
    type = models.CharField(
        max_length=10, choices=operation_types, default='input')
    subtype = models.CharField(max_length=50, choices=operation_subtypes)
    product_stocks = models.ManyToManyField(
        ProductStock, through='StockOperationItem')
    items = models.IntegerField(default=0)
    total = models.IntegerField(default=0)
    description = models.CharField(max_length=500, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.initiator} - {self.type} - {self.subtype} - {self.description}'

    def calculate_total(self):
        self.total = sum(
            item.get_total for item in self.stockoperationitem_set.all())
        self.items = self.stockoperationitem_set.count()
        self.save()

    def get_hashid(self):
        return h_encode(self.id)

    @property
    def model_name(self):
        return self.__class__.__name__


class StockOperationItem(models.Model):
    stock_operation = models.ForeignKey(
        StockOperation, on_delete=models.SET_NULL, blank=True, null=True)
    product_stock = models.ForeignKey(ProductStock, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)

    @property
    def get_total(self):
        total = self.product_stock.price * self.quantity
        return total

    def __str__(self):
        return f'{self.stock_operation.operation_type.capitalize()} de {self.quantity} {self.product_stock.product.unit} de {self.product_stock.product.name}'

    def get_hashid(self):
        return h_encode(self.id)

    @property
    def model_name(self):
        return self.__class__.__name__

# ----------------------------------- Inventory -----------------------------------

class Inventory(models.Model):
    store = models.ForeignKey(
        Store, on_delete=models.SET_NULL, blank=True, null=True)
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

    @property
    def model_name(self):
        return self.__class__.__name__


class InventoryItem(models.Model):
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    product_stock = models.ForeignKey(
        ProductStock, on_delete=models.CASCADE)
    quantity_expected = models.PositiveIntegerField(default=0)
    quantity_found = models.PositiveIntegerField(default=0)
    difference = models.IntegerField(default=0)
    comment = models.CharField(max_length=500, blank=True, null=True)

    def save(self, *args, **kwargs):
        # Use quantity from ProductStock
        self.quantity_expected = self.product_stock.quantity
        self.difference = self.quantity_found - self.quantity_expected
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.product_stock.product.name} - {self.difference}'

    def get_hashid(self):
        return h_encode(self.id)

    @property
    def model_name(self):
        return self.__class__.__name__
