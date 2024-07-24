from .models import *
from django import forms
from django.forms import ModelForm
from django.forms import inlineformset_factory


class TimeInput(forms.TimeInput):
    input_type = 'time'


class DateInput(forms.DateInput):
    input_type = 'date'


# ------------------------------------------ Entity forms ------------------------------------------------------
class EntityTypeForm(forms.ModelForm):
    class Meta:
        model = EntityType
        fields = '__all__'

        labels = {
            'name': 'Nom',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': "mb-2 px-3 py-2 rounded border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-green-400 w-full"}),
            'description': forms.Textarea(attrs={"rows": "5", 'class': "mb-2 px-4 py-2 rounded border focus:border-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),

        }

class LotForm(forms.ModelForm):
    class Meta:
        model = Lot
        fields = '__all__'
        exclude=('timestamp',)

        labels = {
            'name': 'Nom',
            'store': 'Boutique',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': "mb-2 px-3 py-2 rounded border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-green-400 w-full"}),
            'store': forms.Select(attrs={'class': "mb-2 px-3 py-2 rounded border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-green-400 w-full"}),
        }

class UnitForm(forms.ModelForm):
    class Meta:
        model = Unit
        fields = '__all__'

        labels = {
            'name': 'Nom',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': "mb-2 px-3 py-2 rounded border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-green-400 w-full"}),
            'abbreviation': forms.TextInput(attrs={'class': "mb-2 px-3 py-2 rounded border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-green-400 w-full"}),
        }


class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = '__all__'
        exclude = ('is_new',)

        labels = {
            'name': 'Nom',
            'phone': 'Telephone',
            'address': 'Adresse',
            'domain': 'Secteur',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': "mb-2 px-3 py-2 rounded border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-green-400 w-full"}),
            'phone': forms.TextInput(attrs={'class': "mb-2 px-3 py-2 rounded border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-green-400 w-full"}),
            'address': forms.TextInput(attrs={'class': "mb-2 px-3 py-2 rounded border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-green-400 w-full"}),
            'email': forms.EmailInput(attrs={'class': "mb-2 px-3 py-2 rounded border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-green-400 w-full"}),
            'type': forms.Select(attrs={'class': "mb-1 px-3 py-2 rounded border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),
            'domain': forms.TextInput(attrs={'class': "mb-2 px-3 py-2 rounded border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-green-400 w-full"}),
            'description': forms.Textarea(attrs={"rows": "5", 'class': "mb-2 px-4 py-2 rounded border focus:border-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),

        }


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = '__all__'

        labels = {
            'name': 'Nom',
            'type': 'Type',
            'sex': 'Sexe',
            'phone': 'Telephone',
            'address': 'Adresse',
            'domain': 'Secteur',
        }
        widgets = {
            'type': forms.Select(attrs={'class': "mb-1 px-3 py-2 rounded border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),
            'name': forms.TextInput(attrs={'class': "mb-2 px-3 py-2 rounded border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-green-400 w-full"}),
            'phone': forms.TextInput(attrs={'class': "mb-2 px-3 py-2 rounded border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-green-400 w-full"}),
            'address': forms.TextInput(attrs={'class': "mb-2 px-3 py-2 rounded border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-green-400 w-full"}),
            'email': forms.EmailInput(attrs={'class': "mb-2 px-3 py-2 rounded border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-green-400 w-full"}),
            'sex': forms.Select(attrs={'class': "mb-1 px-3 py-2 rounded border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),
            'domain': forms.TextInput(attrs={'class': "mb-2 px-3 py-2 rounded border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-green-400 w-full"}),
            'description': forms.Textarea(attrs={"rows": "5", 'class': "mb-2 px-4 py-2 rounded border focus:border-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),

        }



# ------------------------------------------ Store forms ------------------------------------------------------
class StoreForm(forms.ModelForm):
    class Meta:
        model = Store
        fields = '__all__'
        exclude = ('workers', 'country', 'description',
                   'is_active', 'is_open', 'opening_date')

        labels = {
            'manager': 'Gérant',
            'phone': 'Telephone',
            'name': 'Nom',
            'address': 'Adresse',
            'city': 'Ville',
            'opening_time': "Heure d'ouverture",
            'opening_time': "Heure de fermeture",
        }
        widgets = {
            'type': forms.Select(attrs={'class': "input_selector mb-1 px-3 py-2 rounded border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),
            'manager': forms.Select(attrs={'class': "input_selector mb-1 px-3 py-2 rounded border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),
            'name': forms.TextInput(attrs={'class': "mb-2 px-3 py-2 rounded border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-green-400 w-full"}),
            'phone': forms.TextInput(attrs={'class': "mb-2 px-3 py-2 rounded border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-green-400 w-full"}),
            'address': forms.TextInput(attrs={'class': "mb-2 px-3 py-2 rounded border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-green-400 w-full"}),
            'email': forms.EmailInput(attrs={'class': "mb-2 px-3 py-2 rounded border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-green-400 w-full"}),
            'city': forms.TextInput(attrs={'class': "mb-2 px-3 py-2 rounded border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-green-400 w-full"}),
            'opening_time': TimeInput(attrs={'class': "mb-2 px-3 py-2 rounded border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-purple-400 w-full"}),
            'closing_time': TimeInput(attrs={'class': "mb-2 px-3 py-2 rounded border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-purple-400 w-full"}),
            'description': forms.Textarea(attrs={"rows": "5", 'class': "mb-2 px-4 py-2 rounded border focus:border-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),

        }



# ------------------------------------------ Product forms ------------------------------------------------------
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('__all__')
        labels = {'name': 'Nom', 'is_featured': 'En vedette'}
        widgets = {
            'name': forms.TextInput(attrs={'class': "mb-1 px-3 py-2 rounded border focus:border-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),
        }


class FamilyForm(forms.ModelForm):
    class Meta:
        model = Family
        fields = ('__all__')
        labels = {'name': 'Nom', 'category': 'Catégorie', }
        widgets = {
            'category': forms.Select(attrs={'class': "input_selector mb-1 px-3 py-2 rounded border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),
            'name': forms.TextInput(attrs={'class': "mb-1 px-3 py-2 rounded border focus:border-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),
        }


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('__all__')
        exclude =('timestamp','is_favorite','is_new',)

        labels = {
            'name': 'Article',
            'store': 'Boutique',
            'image': 'Image',
            'brand': 'Marque',
            'category': 'Catégorie',
            'family': "Famille",
            'unit': "Unité de mesure",
            'supplier': "Fournisseur",
            'is_new': "Nouvel arrivage",
            'is_favorite': "Très en demande",
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': "mb-1 px-3 py-2 rounded border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),
            'brand': forms.TextInput(attrs={'class': "mb-1 px-3 py-2 rounded border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),
            'store': forms.Select(attrs={'class': "input_selector mb-1 px-3 py-2 rounded border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),
            'supplier': forms.Select(attrs={'class': "mb-1 px-3 py-2 rounded border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),
            'category': forms.Select(attrs={'class': "input_selector mb-1 px-3 py-2 rounded border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),
            'family': forms.Select(attrs={'class': "input_selector mb-1 px-3 py-2 rounded border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),
            'unit': forms.Select(attrs={'class': "mb-1 px-3 py-2 rounded border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),
            'quantity': forms.NumberInput(attrs={'class': "mb-1 px-3 py-2 rounded border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),
            'price': forms.NumberInput(attrs={'class': "mb-1 px-3 py-2 rounded border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),
            'promo_price': forms.NumberInput(attrs={'class': "mb-1 px-3 py-2 rounded border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),
            'description': forms.Textarea(attrs={"rows": "5", 'class': "mb-2 px-4 py-2 rounded border focus:border-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),

        }

        def __init__(self, *args, **kwargs):
            super(ProductForm, self).__init__(*args, **kwargs)
            self.fields['Family'].queryset = Family.objects.none()

            if 'category' in self.data:
                try:
                    category_id = int(self.data.get('category'))
                    self.fields['Family'].queryset = Family.objects.filter(
                        category_id=category_id).order_by('name')
                except (ValueError, TypeError):
                    pass  # invalid input from the client; ignore and fallback to empty Family queryset
            elif self.instance.pk:
                self.fields['Family'].queryset = self.instance.category.Family_set.order_by(
                    'name')


class ProductStockForm(forms.ModelForm):
    class Meta:
        model = ProductStock
        fields = '__all__'
        exclude = ('production_date', 'expiration_date',
                   'is_promoted', 'promo_price', 'observation','timestamp')

        labels = {
            'product': 'Produit',
            'supplier': 'Fournisseur',
            'quantity': 'Quantité',
            'price': "Prix unitaire d'achat",
            'production_date': 'Produit le',
            'expiration_date': 'Expire le',
        }
        widgets = {
            'product': forms.Select(attrs={'class': "input_selector mb-1 px-3 py-2 rounded border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),
            'supplier': forms.Select(attrs={'class': "mb-1 px-3 py-2 rounded border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),
            'lot': forms.Select(attrs={'class': "mb-2 px-3 py-2 rounded border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-green-400 w-full"}),
            'quantity': forms.NumberInput(attrs={'class': "mb-2 px-3 py-2 rounded border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-green-400 w-full"}),
            'price': forms.NumberInput(attrs={'class': "mb-2 px-3 py-2 rounded border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-green-400 w-full"}),
            'observation': forms.Textarea(attrs={"rows": "5", 'class': "mb-2 px-4 py-2 rounded border focus:border-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),
            'production_date': DateInput(attrs={'class': "mb-1 px-3 py-2 rounded border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),
            'expiration_date': DateInput(attrs={'class': "mb-1 px-3 py-2 rounded border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),

        }



# ------------------------------------------ Sale forms ------------------------------------------------------
class SaleForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        curr_obj = kwargs.pop('curr_obj', None)
        super(SaleForm, self).__init__(*args, **kwargs)

        if user and user.role.sec_level < 3:
            self.fields.pop('store')
            self.fields.pop('initiator')
        if not curr_obj:
            self.fields.pop('cashdesk')
            self.fields.pop('discount')
            self.fields.pop('observation')

    class Meta:
        model = Sale
        observation = models.CharField(max_length=500, blank=True, null=True)
        fields = ('store', 'initiator', 'client',
                  'cashdesk', 'discount', 'observation',)

        labels = {
            'store': 'Boutique',
            'initiator': 'Initiateur',
            'cashdesk': 'Caisse',
            'discount': 'Remise',
        }
        widgets = {
            'store': forms.Select(attrs={'class': "input_selector mb-1 px-3 py-2 rounded border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),
            'initiator': forms.Select(attrs={'class': "mb-1 px-3 py-2 rounded border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),
            'client': forms.Select(attrs={'class': "mb-1 px-3 py-2 rounded border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),
            'cashdesk': forms.Select(attrs={'class': "mb-1 px-3 py-2 rounded border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),
            'discount': forms.NumberInput(attrs={'class': "mb-2 px-3 py-2 rounded border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-green-400 w-full"}),
            'observation': forms.Textarea(attrs={"rows": "5", 'class': "mb-2 px-4 py-2 rounded border focus:border-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),

        }


class SaleItemForm(forms.ModelForm):
    class Meta:
        model = SaleItem
        fields = '__all__'
        exclude = ('sale', )

        labels = {
            'sale': 'Vente',
            'product_stock': 'Produit',
            'quantity': 'Quantité',
        }
        widgets = {
            'sale': forms.Select(attrs={'class': "mb-1 px-3 py-2 rounded border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),
            'product_stock': forms.Select(attrs={'class': "mb-1 px-3 py-2 rounded border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),
            'quantity': forms.NumberInput(attrs={'class': "mb-2 px-3 py-2 rounded border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-green-400 w-full"}),

        }



# ------------------------------------------ Purchase forms ------------------------------------------------------
class PurchaseForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        curr_obj = kwargs.pop('curr_obj', None)
        super(PurchaseForm, self).__init__(*args, **kwargs)

        if user and user.role.sec_level < 3:
            self.fields.pop('store')
        if not curr_obj:
            self.fields.pop('cashdesk')
            self.fields.pop('total')
            # self.fields.pop('total_paid')
        if curr_obj and curr_obj.type == 'product':
            self.fields.pop('total')


    class Meta:
        model = Purchase
        fields = (
            'store',
            'label',
            'supplier',
            'cashdesk',
            'total',
            # 'total_paid',
            'description',
        )
        exclude = ('audit', 'timestamp',)

        labels = {
            'store': 'Boutique',
            'label': 'Libelé',
            'supplier': 'Fournisseur',
            'cashdesk': 'Caisse',
            'total': 'Montant à payer',
            'total_paid': 'Montant Payé',
        }
        widgets = {
            'store': forms.Select(attrs={'class': "input_selecto mb-1 px-3 py-2 rounded border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),
            'supplier': forms.Select(attrs={'class': "mb-1 px-3 py-2 rounded border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),
            'label': forms.TextInput(attrs={'class': "mb-2 px-3 py-2 rounded border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-green-400 w-full"}),
            'total': forms.NumberInput(attrs={'class': "mb-2 px-3 py-2 rounded focus:outline-none bg-gray-100 w-full",}),
            'total_paid': forms.NumberInput(attrs={'class': "mb-2 px-3 py-2 rounded border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-green-400 w-full"}),
            'cashdesk': forms.Select(attrs={'class': "mb-1 px-3 py-2 rounded border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),
            'description': forms.Textarea(attrs={"rows": "5", 'class': "mb-2 px-4 py-2 rounded border focus:border-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),

        }


class PurchaseItemForm(forms.ModelForm):
    class Meta:
        model = PurchaseItem
        fields = '__all__'
        exclude = ('purchase', )

        labels = {
            'purchase': 'Achat',
            'product_stock': 'Produit',
            'quantity': 'Quantité',
            'price': 'Prix',
        }
        widgets = {
            'purchase': forms.Select(attrs={'class': "mb-1 px-3 py-2 rounded border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),
            'product_stock': forms.Select(attrs={'class': "mb-1 px-3 py-2 rounded border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),
            'quantity': forms.NumberInput(attrs={'class': "mb-2 px-3 py-2 rounded border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-green-400 w-full"}),
            'price': forms.TextInput(attrs={'class': "mb-2 px-3 py-2 rounded border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-green-400 w-full"}),

        }



# ------------------------------------------ Stock forms ------------------------------------------------------
class StockOperationForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(StockOperationForm, self).__init__(*args, **kwargs)

        self.fields.pop('type')
        if user and user.role.sec_level < 3:
            self.fields.pop('store')
            self.fields.pop('initiator')

    class Meta:
        model = StockOperation
        fields = ['store', 'initiator', 'type','subtype', 'description']

        labels = {
            'store': "Boutique",
            'type': "Type d'operation",
            'subtype': "Sous-type d'operation",
            'initiator': 'Initiateur',
        }
        widgets = {
            'store': forms.Select(attrs={'class': "input_selector mb-1 px-3 py-2 rounded border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),
            'initiator': forms.Select(attrs={'class': "input_selector mb-1 px-3 py-2 rounded border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),
            'type': forms.Select(attrs={'class': "mb-1 px-3 py-2 rounded border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),
            'subtype': forms.Select(attrs={'class': "mb-1 px-3 py-2 rounded border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),
            'description': forms.Textarea(attrs={"rows": "5", 'class': "mb-2 px-4 py-2 rounded border focus:border-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),

        }


class StockOperationItemForm(forms.ModelForm):
    class Meta:
        model = StockOperationItem
        fields = ('product_stock', 'quantity',)

        labels = {
            'product_stock': 'Produit',
            'quantity': 'Quantité',
        }
        widgets = {
            'product_stock': forms.Select(attrs={'class': "mb-1 px-3 py-2 rounded border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),
            'quantity': forms.NumberInput(attrs={'class': "mb-2 px-3 py-2 rounded border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-green-400 w-full"}),
        }



# ------------------------------------------ Inventory form ------------------------------------------------------
class InventoryForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(InventoryForm, self).__init__(*args, **kwargs)

        if user and user.role.sec_level < 3:
            self.fields.pop('store')
            self.fields.pop('supervisor')
            self.fields.pop('initiator')

    class Meta:
        model = Inventory
        fields = (
            'store',
            'initiator',
            'supervisor',
            'date',
            # 'is_valid',
        )

        labels = {
            'store': "Boutique",
            'initiator': 'Initiateur',
            'supervisor': "Superviseur",
            'is_valid': 'Validé',
        }
        widgets = {
            'store': forms.Select(attrs={'class': "input_selector mb-1 px-3 py-2 rounded border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),
            'initiator': forms.Select(attrs={'class': "input_selector mb-1 px-3 py-2 rounded border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),
            'supervisor': forms.Select(attrs={'class': "input_selector mb-1 px-3 py-2 rounded border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),
            'date': DateInput(attrs={'class': "mb-1 px-3 py-2 rounded border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),

        }


class InventoryItemForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(InventoryItemForm, self).__init__(*args, **kwargs)

        if user and user.role.sec_level < 3:
            self.fields.pop('supervisor')
            self.fields.pop('initiator')

    class Meta:
        model = InventoryItem
        fields = (
            # 'supervisor', 'initiator',
            'quantity_expected', 'quantity_found', 'comment')

        labels = {
            'supervisor': "Superviseur",
            'initiator': 'Initiateur',
            'quantity_expected': 'Qantité théorique',
            'quantity_found': 'Qantité physique',
            'comment': 'Commentaire',
        }
        widgets = {
            'supervisor': forms.Select(attrs={'class': "input_selector mb-1 px-3 py-2 rounded border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),
            'initiator': forms.Select(attrs={'class': "input_selector mb-1 px-3 py-2 rounded border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),
            'quantity_expected': forms.NumberInput(attrs={'class': "mb-1 px-3 py-2 rounded focus:border-none focus:outline-none  bg-gray-100 w-full", 'readonly': 'readonly'}),
            'quantity_found': forms.NumberInput(attrs={'class': "mb-2 px-3 py-2 rounded border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-green-400 w-full"}),
            'comment': forms.Textarea(attrs={"rows": "5", 'class': "mb-2 px-4 py-2 rounded border focus:border-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),

        }



# ------------------------------------------ Finance form ------------------------------------------------------
class TransactionForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        desk = kwargs.pop('desk', None)
        super(TransactionForm, self).__init__(*args, **kwargs)

        self.fields.pop('store')
        self.fields.pop('initiator')
        self.fields.pop('cashdesk')

        if user and user.role.sec_level < 3:
            # self.fields.pop('cashdesk')
            self.fields.pop('description')
        if not desk:
            self.fields.pop('type')

    class Meta:
        model = Transaction
        fields = ('store', 'initiator', 'cashdesk','type', 'label',
                  'amount',  'description')

        labels = {
            'store': "Boutique",
            'initiator': "Initiateur",
            'cashdesk': "Caisse",
            'amount': 'Montant',
            'label': 'Libelé',
        }
        widgets = {
            'store': forms.Select(attrs={'class': "input_selector mb-1 px-3 py-2 rounded border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),
            'initiator': forms.Select(attrs={'class': "input_selector mb-1 px-3 py-2 rounded border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),
            'cashdesk': forms.Select(attrs={'class': "input_selector mb-1 px-3 py-2 rounded border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),
            'type': forms.Select(attrs={'class': "input_selector mb-1 px-3 py-2 rounded border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),
            'label': forms.TextInput(attrs={'class': "mb-2 px-3 py-2 rounded border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-green-400 w-full"}),
            'amount': forms.TextInput(attrs={'class': "input_selector mb-1 px-3 py-2 rounded border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),
            'description': forms.Textarea(attrs={"rows": "5", 'class': "mb-2 px-4 py-2 rounded border focus:border-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),

        }


class ReceivableForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(ReceivableForm, self).__init__(*args, **kwargs)

        if user and user.role.sec_level < 2:
            self.fields.pop('sale')
            self.fields.pop('client')

        if user and user.role.sec_level < 3:
            self.fields.pop('client')

    class Meta:
        model = Receivable
        fields = ('sale',
                  'client',
                  'label',
                  'amount',
                  )

        labels = {
            'sale': "Vente",
            'amount': 'Montant',
            'label': 'Libelé',
        }
        widgets = {
            'sale': forms.Select(attrs={'class': "input_selector mb-1 px-3 py-2 rounded border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),
            'client': forms.Select(attrs={'class': "input_selector mb-1 px-3 py-2 rounded border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),
            'label': forms.TextInput(attrs={'class': "mb-2 px-3 py-2 rounded border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-green-400 w-full"}),
            'amount': forms.TextInput(attrs={'class': "input_selector mb-1 px-3 py-2 rounded border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),
        }


class DebtForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(DebtForm, self).__init__(*args, **kwargs)

        if user and user.role.sec_level < 2:
            self.fields.pop('store')
            self.fields.pop('initiator')

        if user and user.role.sec_level < 3:
            self.fields.pop('store')

    class Meta:
        model = Debt
        fields = ('store', 'initiator', 'supplier',
                  'amount', 'label', 'description')

        labels = {
            'store': "Boutique",
            'initiator': "Initiateur",
            'amount': 'Montant',
            'label': 'Libelé',
        }
        widgets = {
            'store': forms.Select(attrs={'class': "input_selector mb-1 px-3 py-2 rounded border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),
            'initiator': forms.Select(attrs={'class': "input_selector mb-1 px-3 py-2 rounded border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),
            'supplier': forms.Select(attrs={'class': "input_selector mb-1 px-3 py-2 rounded border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),
            'amount': forms.TextInput(attrs={'class': "input_selector mb-1 px-3 py-2 rounded border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),
            'label': forms.TextInput(attrs={'class': "mb-2 px-3 py-2 rounded border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-green-400 w-full"}),
            'description': forms.Textarea(attrs={"rows": "5", 'class': "mb-2 px-4 py-2 rounded border focus:border-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),
        }


# ------------- cashdesks
class CashdeskForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(CashdeskForm, self).__init__(*args, **kwargs)

        if user and user.role.sec_level < 3:
            self.fields.pop('store')

    class Meta:
        model = Cashdesk
        fields = ('store',
                  'type',
                  'carrier',
                  'name',
                  'phone',
                  'acc_number',
                  )
        labels = {'store': 'Boutique',
                  'type': 'Type de caisse',
                  'carrier': 'Opérateur',
                  'name': 'Nom',
                  'phone': 'Numero de Telephone',
                  'acc_number': 'Numero de compte',
                  'balance': 'Solde',
                  }
        exclude = ['debits', 'credits']
        widgets = {
            'store': forms.Select(attrs={'class': "input_selector mb-1 px-3 py-2 rounded border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),
            'type': forms.Select(attrs={'class': "input_selector mb-1 px-3 py-2 rounded border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),
            'carrier': forms.Select(attrs={'class': "input_selector mb-1 px-3 py-2 rounded border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),
            'balance': forms.TextInput(attrs={'class': "mb-1 px-3 py-2 rounded border focus:border-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),
            'phone': forms.TextInput(attrs={'class': "mb-1 px-3 py-2 rounded border focus:border-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),
            'acc_number': forms.TextInput(attrs={'class': "mb-1 px-3 py-2 rounded border focus:border-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),
        }


class CashdeskClosingForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(CashdeskClosingForm, self).__init__(*args, **kwargs)

        if user and user.role.sec_level < 3:
            self.fields.pop('initiator')
            self.fields.pop('supervisor')
            self.fields.pop('cashdesk')

    class Meta:
        model = CashdeskClosing
        fields = (
            #   'initiator',
            #   'supervisor',
            #   'cashdesk',
            'balance_expected',
            'balance_found',
            #   'difference',
            'comment',
        )
        labels = {'initiator': 'Initiateur',
                  'supervisor': 'Superviseur',
                  'cashdesk': 'Caisse',
                  'balance_expected': 'Solde théorique',
                  'balance_found': 'Solde physique',
                  'difference': 'Différence',
                  'comment': 'Commentaire',
                  }
        exclude = ['debits', 'credits']
        widgets = {
            'initiator': forms.Select(attrs={'class': "input_selector mb-1 px-3 py-2 rounded border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),
            'supervisor': forms.Select(attrs={'class': "input_selector mb-1 px-3 py-2 rounded border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),
            'cashdesk': forms.Select(attrs={'class': "input_selector mb-1 px-3 py-2 rounded border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),
            'balance_expected': forms.NumberInput(attrs={'id': 'exptd_field', 'class': "mb-1 px-3 py-2 rounded focus:border-none focus:outline-none  bg-gray-100 w-full", 'readonly': 'readonly'}),
            'balance_found': forms.NumberInput(attrs={'id': 'found_field', 'class ': "mb-1 px-3 py-2 rounded border focus:border-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),
            'difference': forms.NumberInput(attrs={'id': 'diff_field', 'class': "mb-1 px-3 py-2 rounded focus:border-none focus:outline-none  bg-gray-100 w-full", 'readonly': 'readonly'}),
            'comment': forms.Textarea(attrs={"rows": "5", 'class': "mb-2 px-4 py-2 rounded border focus:border-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),
        }


class CashReceiptForm(forms.ModelForm):
    class Meta:
        model = CashReceipt
        fields = '__all__'

        labels = {
            'name': 'Nom',
            'value': 'Valeur',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': "mb-2 px-3 py-2 rounded border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-green-400 w-full"}),
            'value': forms.NumberInput(attrs={'class': "mb-2 px-3 py-2 rounded border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-green-400 w-full"}),
            'type': forms.Select(attrs={'class': "input_selector mb-1 px-3 py-2 rounded border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),

        }


class ClosingCashReceiptForm(forms.ModelForm):
    class Meta:
        model = ClosingCashReceipt
        fields = ['cash_receipt', 'count']

        widgets = {
            'cash_receipt': forms.Select(attrs={'class': 'form-control'}),
            'count': forms.NumberInput(attrs={'class': 'form-control'}),
        }
