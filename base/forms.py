from .models import *
from django import forms
from django.forms import ModelForm
from django.forms import inlineformset_factory


class TimeInput(forms.TimeInput):
    input_type = 'time'


class DateInput(forms.DateInput):
    input_type = 'date'


class EntityTypeForm(forms.ModelForm):
    class Meta:
        model = EntityType
        fields = '__all__'

        labels = {
            'name': 'Nom',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': "mb-2 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-green-400 w-full"}),
            'description': forms.Textarea(attrs={"rows": "5", 'class': "mb-2 px-4 py-2 rounded-xl border focus:border-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),

        }


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
            'type': forms.Select(attrs={'class': "input_selector mb-1 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),
            'manager': forms.Select(attrs={'class': "input_selector mb-1 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),
            'name': forms.TextInput(attrs={'class': "mb-2 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-green-400 w-full"}),
            'phone': forms.TextInput(attrs={'class': "mb-2 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-green-400 w-full"}),
            'address': forms.TextInput(attrs={'class': "mb-2 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-green-400 w-full"}),
            'email': forms.EmailInput(attrs={'class': "mb-2 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-green-400 w-full"}),
            'city': forms.TextInput(attrs={'class': "mb-2 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-green-400 w-full"}),
            'opening_time': TimeInput(attrs={'class': "mb-2 px-3 py-2 rounded-md border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-purple-400 w-full"}),
            'closing_time': TimeInput(attrs={'class': "mb-2 px-3 py-2 rounded-md border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-purple-400 w-full"}),
            'description': forms.Textarea(attrs={"rows": "5", 'class': "mb-2 px-4 py-2 rounded-xl border focus:border-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),

        }


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('__all__')
        labels = {'name': 'Nom', 'is_featured': 'En vedette'}
        widgets = {
            'name': forms.TextInput(attrs={'class': "mb-1 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),
        }


class FamilyForm(forms.ModelForm):
    class Meta:
        model = Family
        fields = ('__all__')
        labels = {'name': 'Nom', 'category': 'Catégorie', }
        widgets = {
            'category': forms.Select(attrs={'class': "input_selector mb-1 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),
            'name': forms.TextInput(attrs={'class': "mb-1 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),
        }


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('__all__')

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
            'name': forms.TextInput(attrs={'class': "mb-1 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),
            'brand': forms.TextInput(attrs={'class': "mb-1 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),
            'store': forms.Select(attrs={'class': "input_selector mb-1 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),
            'supplier': forms.Select(attrs={'class': "mb-1 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),
            'category': forms.Select(attrs={'class': "input_selector mb-1 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),
            'family': forms.Select(attrs={'class': "input_selector mb-1 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),
            'unit': forms.Select(attrs={'class': "mb-1 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),
            'quantity': forms.NumberInput(attrs={'class': "mb-1 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),
            'price': forms.NumberInput(attrs={'class': "mb-1 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),
            'promo_price': forms.NumberInput(attrs={'class': "mb-1 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),
            'description': forms.Textarea(attrs={"rows": "5", 'class': "mb-2 px-4 py-2 rounded-xl border focus:border-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),

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
                   'is_promoted', 'promo_price', 'observation',)

        labels = {
            'product': 'Produit',
            'supplier': 'Fournisseur',
            'quantity': 'Quantité',
            'price': 'Prix',
            'production_date': 'Produit le',
            'expiration_date': 'Expire le',
        }
        widgets = {
            'product': forms.Select(attrs={'class': "input_selector mb-1 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),
            'supplier': forms.Select(attrs={'class': "mb-1 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),
            'lot': forms.NumberInput(attrs={'class': "mb-2 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-green-400 w-full"}),
            'quantity': forms.NumberInput(attrs={'class': "mb-2 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-green-400 w-full"}),
            'price': forms.NumberInput(attrs={'class': "mb-2 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-green-400 w-full"}),
            'observation': forms.Textarea(attrs={"rows": "5", 'class': "mb-2 px-4 py-2 rounded-xl border focus:border-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),
            'production_date': DateInput(attrs={'class': "mb-1 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),
            'expiration_date': DateInput(attrs={'class': "mb-1 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),

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
            'name': forms.TextInput(attrs={'class': "mb-2 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-green-400 w-full"}),
            'phone': forms.TextInput(attrs={'class': "mb-2 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-green-400 w-full"}),
            'address': forms.TextInput(attrs={'class': "mb-2 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-green-400 w-full"}),
            'email': forms.EmailInput(attrs={'class': "mb-2 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-green-400 w-full"}),
            'type': forms.Select(attrs={'class': "mb-1 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),
            'domain': forms.TextInput(attrs={'class': "mb-2 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-green-400 w-full"}),
            'description': forms.Textarea(attrs={"rows": "5", 'class': "mb-2 px-4 py-2 rounded-xl border focus:border-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),

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
            'type': forms.Select(attrs={'class': "mb-1 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),
            'name': forms.TextInput(attrs={'class': "mb-2 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-green-400 w-full"}),
            'phone': forms.TextInput(attrs={'class': "mb-2 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-green-400 w-full"}),
            'address': forms.TextInput(attrs={'class': "mb-2 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-green-400 w-full"}),
            'email': forms.EmailInput(attrs={'class': "mb-2 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-green-400 w-full"}),
            'sex': forms.Select(attrs={'class': "mb-1 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),
            'domain': forms.TextInput(attrs={'class': "mb-2 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-green-400 w-full"}),
            'description': forms.Textarea(attrs={"rows": "5", 'class': "mb-2 px-4 py-2 rounded-xl border focus:border-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),

        }


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
            'store': forms.Select(attrs={'class': "input_selector mb-1 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),
            'initiator': forms.Select(attrs={'class': "mb-1 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),
            'client': forms.Select(attrs={'class': "mb-1 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),
            'cashdesk': forms.Select(attrs={'class': "mb-1 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),
            'discount': forms.NumberInput(attrs={'class': "mb-2 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-green-400 w-full"}),
            'observation': forms.Textarea(attrs={"rows": "5", 'class': "mb-2 px-4 py-2 rounded-xl border focus:border-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),

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
            'sale': forms.Select(attrs={'class': "mb-1 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),
            'product_stock': forms.Select(attrs={'class': "mb-1 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),
            'quantity': forms.NumberInput(attrs={'class': "mb-2 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-green-400 w-full"}),

        }


class ServicePurchaseForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(ServicePurchaseForm, self).__init__(*args, **kwargs)

        if user and user.role.sec_level < 3:
            self.fields.pop('store')

    class Meta:
        model = ServicePurchase
        fields = (
            'store',
            'label',
            'supplier',
            'total',
            'cashdesk',
            'amount_paid',
            'payment_option',
            'payment_status',
            'description',)
        exclude = ('audit', 'timestamp',)

        labels = {
            'store': 'Boutique',
            'label': 'Libelé',
            'supplier': 'Fournisseur',
            'cashdesk': 'Caisse',
            'total': 'Montant à payer',
            'amount_paid': 'Montant Payé',
            'payment_option': 'Moyen de paiement',
            'payment_status': 'Status du paiement',
        }
        widgets = {
            'store': forms.Select(attrs={'class': "input_selector mb-1 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),
            'supplier': forms.Select(attrs={'class': "mb-1 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),
            'label': forms.TextInput(attrs={'class': "mb-2 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-green-400 w-full"}),
            'total': forms.TextInput(attrs={'class': "mb-2 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-green-400 w-full"}),
            'cashdesk': forms.Select(attrs={'class': "mb-1 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),
            'amount_paid': forms.TextInput(attrs={'class': "mb-2 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-green-400 w-full"}),
            'payment_option': forms.Select(attrs={'class': "mb-1 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),
            'payment_status': forms.Select(attrs={'class': "mb-1 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),
            'description': forms.Textarea(attrs={"rows": "5", 'class': "mb-2 px-4 py-2 rounded-xl border focus:border-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),

        }


class ProductPurchaseForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        curr_obj = kwargs.pop('curr_obj', None)
        super(ProductPurchaseForm, self).__init__(*args, **kwargs)

        if user and user.role.sec_level < 3:
            self.fields.pop('store')
        if not curr_obj:
            self.fields.pop('cashdesk')
            self.fields.pop('amount_paid')
            self.fields.pop('total')
            self.fields.pop('payment_option')
            self.fields.pop('payment_status')

    class Meta:
        model = ProductPurchase
        fields = (
            'store',
            'label',
            'supplier',
            'cashdesk',
            'total',
            'amount_paid',
            'payment_option',
            'payment_status',
            'description',
            )
        exclude = ('audit', 'timestamp',)

        labels = {
            'store': 'Boutique',
            'label': 'Libelé',
            'supplier': 'Fournisseur',
            'cashdesk': 'Caisse',
            'total': 'Montant à payer',
            'amount_paid': 'Montant Payé',
            'payment_option': 'Moyen de paiement',
            'payment_status': 'Status du paiement',
        }
        widgets = {
            'store': forms.Select(attrs={'class': "input_selector mb-1 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),
            'supplier': forms.Select(attrs={'class': "mb-1 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),
            'label': forms.TextInput(attrs={'class': "mb-2 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-green-400 w-full"}),
            'total': forms.TextInput(attrs={'class': "mb-2 px-3 py-2 rounded-lg focus:outline-none bg-gray-100 w-full", 'readonly': 'readonly'}),
            'amount_paid': forms.TextInput(attrs={'class': "mb-2 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-green-400 w-full"}),
            'cashdesk': forms.Select(attrs={'class': "mb-1 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),
            'payment_option': forms.Select(attrs={'class': "mb-1 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),
            'payment_status': forms.Select(attrs={'class': "mb-1 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),
            'description': forms.Textarea(attrs={"rows": "5", 'class': "mb-2 px-4 py-2 rounded-xl border focus:border-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),

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
            'purchase': forms.Select(attrs={'class': "mb-1 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),
            'product_stock': forms.Select(attrs={'class': "mb-1 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),
            'quantity': forms.NumberInput(attrs={'class': "mb-2 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-green-400 w-full"}),
            'price': forms.TextInput(attrs={'class': "mb-2 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-green-400 w-full"}),

        }


class StockInputForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(StockInputForm, self).__init__(*args, **kwargs)

        if user and user.role.sec_level < 3:
            self.fields.pop('store')
            self.fields.pop('initiator')

    class Meta:
        model = StockInput
        fields = ['store', 'initiator', 'type', 'description']

        labels = {
            'store': "Boutique",
            'type': "Type d'entrée",
            'initiator': 'Initiateur',
        }
        widgets = {
            'store': forms.Select(attrs={'class': "input_selector mb-1 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),
            'initiator': forms.Select(attrs={'class': "input_selector mb-1 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),
            'type': forms.Select(attrs={'class': "mb-1 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),
            'description': forms.Textarea(attrs={"rows": "5", 'class': "mb-2 px-4 py-2 rounded-xl border focus:border-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),

        }


class StockInputItemForm(forms.ModelForm):
    class Meta:
        model = StockInputItem
        fields = ('product_stock', 'quantity',)

        labels = {
            'product_stock': 'Produit',
            'quantity': 'Quantité',
        }
        widgets = {
            'product_stock': forms.Select(attrs={'class': "mb-1 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),
            'quantity': forms.NumberInput(attrs={'class': "mb-2 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-green-400 w-full"}),
        }


class StockOutputForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(StockOutputForm, self).__init__(*args, **kwargs)

        if user and user.role.sec_level < 3:
            self.fields.pop('store')

    class Meta:
        model = StockOutput
        fields = ['store', 'initiator', 'type', 'description']

        labels = {
            'store': "Boutique",
            'type': "Type de sortie",
            'initiator': 'Initiateur',
        }
        widgets = {
            'store': forms.Select(attrs={'class': "input_selector mb-1 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),
            'initiator': forms.Select(attrs={'class': "input_selector mb-1 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),
            'type': forms.Select(attrs={'class': "mb-1 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),
            'description': forms.Textarea(attrs={"rows": "5", 'class': "mb-2 px-4 py-2 rounded-xl border focus:border-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),

        }


class StockOutputItemForm(forms.ModelForm):
    class Meta:
        model = StockOutputItem
        fields = ('product_stock', 'quantity')

        labels = {
            'product_stock': 'Produit',
            'quantity': 'Quantité',
        }
        widgets = {
            'product_stock': forms.Select(attrs={'class': "mb-1 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),
            'quantity': forms.NumberInput(attrs={'class': "mb-2 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-green-400 w-full"}),
            'comment': forms.Textarea(attrs={"rows": "5", 'class': "mb-2 px-4 py-2 rounded-xl border focus:border-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),

        }


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
            'store': forms.Select(attrs={'class': "input_selector mb-1 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),
            'initiator': forms.Select(attrs={'class': "input_selector mb-1 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),
            'supervisor': forms.Select(attrs={'class': "input_selector mb-1 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),
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
            'supervisor': forms.Select(attrs={'class': "input_selector mb-1 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),
            'initiator': forms.Select(attrs={'class': "input_selector mb-1 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),
            'quantity_expected': forms.NumberInput(attrs={'class': "mb-1 px-3 py-2 rounded-lg focus:border-none focus:outline-none  bg-gray-100 w-full", 'readonly': 'readonly'}),
            'quantity_found': forms.NumberInput(attrs={'class': "mb-2 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-green-400 w-full"}),
            'comment': forms.Textarea(attrs={"rows": "5", 'class': "mb-2 px-4 py-2 rounded-xl border focus:border-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),

        }


class PaymentForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(PaymentForm, self).__init__(*args, **kwargs)

        if user and user.role.sec_level < 3:
            self.fields.pop('store')

    class Meta:
        model = Payment
        fields = ('store', 'initiator', 'cashdesk',
                  'amount', 'label', 'description')

        labels = {
            'store': "Boutique",
            'initiator': "Initiateur",
            'cashdesk': "Caisse",
            'amount': 'Montant',
            'label': 'Libelé',
        }
        widgets = {
            'store': forms.Select(attrs={'class': "input_selector mb-1 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),
            'initiator': forms.Select(attrs={'class': "input_selector mb-1 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),
            'cashdesk': forms.Select(attrs={'class': "input_selector mb-1 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),
            'amount': forms.TextInput(attrs={'class': "input_selector mb-1 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),
            'label': forms.TextInput(attrs={'class': "mb-2 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-green-400 w-full"}),
            'description': forms.Textarea(attrs={"rows": "5", 'class': "mb-2 px-4 py-2 rounded-xl border focus:border-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),

        }


class TransactionForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        cashdesk = kwargs.pop('cashdesk', None)
        super(TransactionForm, self).__init__(*args, **kwargs)

        if user and user.role.sec_level < 3:
            self.fields.pop('store')
        if cashdesk:
            self.fields.pop('store')
            self.fields.pop('cashdesk')

    class Meta:
        model = Transaction
        fields = ('store', 'cashdesk', 'label', 'amount', 'description')

        labels = {
            'store': "Boutique",
            'cashdesk': "Caisse",
            'label': 'Libelé',
            'amount': 'Montant',
        }
        widgets = {
            'store': forms.Select(attrs={'class': "input_selector mb-1 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),
            'cashdesk': forms.Select(attrs={'class': "input_selector mb-1 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),
            'amount': forms.TextInput(attrs={'class': "input_selector mb-1 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),
            'label': forms.TextInput(attrs={'class': "mb-2 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-green-400 w-full"}),
            'description': forms.Textarea(attrs={"rows": "5", 'class': "mb-2 px-4 py-2 rounded-xl border focus:border-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),

        }


class ReceivableForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(ReceivableForm, self).__init__(*args, **kwargs)

        if user and user.role.sec_level < 2:
            self.fields.pop('store')
            self.fields.pop('initiator')

        if user and user.role.sec_level < 3:
            self.fields.pop('store')

    class Meta:
        model = Receivable
        fields = ('store', 'initiator', 'client',
                  'amount', 'label', 'description')

        labels = {
            'store': "Boutique",
            'initiator': "Initiateur",
            'amount': 'Montant',
            'label': 'Libelé',
        }
        widgets = {
            'store': forms.Select(attrs={'class': "input_selector mb-1 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),
            'initiator': forms.Select(attrs={'class': "input_selector mb-1 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),
            'client': forms.Select(attrs={'class': "input_selector mb-1 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),
            'amount': forms.TextInput(attrs={'class': "input_selector mb-1 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),
            'label': forms.TextInput(attrs={'class': "mb-2 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-green-400 w-full"}),
            'description': forms.Textarea(attrs={"rows": "5", 'class': "mb-2 px-4 py-2 rounded-xl border focus:border-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),

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
            'store': forms.Select(attrs={'class': "input_selector mb-1 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),
            'initiator': forms.Select(attrs={'class': "input_selector mb-1 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),
            'supplier': forms.Select(attrs={'class': "input_selector mb-1 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),
            'amount': forms.TextInput(attrs={'class': "input_selector mb-1 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),
            'label': forms.TextInput(attrs={'class': "mb-2 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-green-400 w-full"}),
            'description': forms.Textarea(attrs={"rows": "5", 'class': "mb-2 px-4 py-2 rounded-xl border focus:border-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),
        }



# 
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
            'store': forms.Select(attrs={'class': "input_selector mb-1 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),
            'type': forms.Select(attrs={'class': "input_selector mb-1 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),
            'carrier': forms.Select(attrs={'class': "input_selector mb-1 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),
            'balance': forms.TextInput(attrs={'class': "mb-1 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),
            'phone': forms.TextInput(attrs={'class': "mb-1 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),
            'acc_number': forms.TextInput(attrs={'class': "mb-1 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),
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
            'initiator': forms.Select(attrs={'class': "input_selector mb-1 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),
            'supervisor': forms.Select(attrs={'class': "input_selector mb-1 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),
            'cashdesk': forms.Select(attrs={'class': "input_selector mb-1 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),
            'balance_expected': forms.NumberInput(attrs={'id': 'exptd_field', 'class': "mb-1 px-3 py-2 rounded-lg focus:border-none focus:outline-none  bg-gray-100 w-full", 'readonly': 'readonly'}),
            'balance_found': forms.NumberInput(attrs={'id': 'found_field','class ': "mb-1 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),
            'difference': forms.NumberInput(attrs={'id': 'diff_field', 'class': "mb-1 px-3 py-2 rounded-lg focus:border-none focus:outline-none  bg-gray-100 w-full", 'readonly': 'readonly'}),
            'comment': forms.Textarea(attrs={"rows": "5", 'class': "mb-2 px-4 py-2 rounded-xl border focus:border-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),
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
            'name': forms.TextInput(attrs={'class': "mb-2 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-green-400 w-full"}),
            'value': forms.NumberInput(attrs={'class': "mb-2 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-green-400 w-full"}),
            'type': forms.Select(attrs={'class': "input_selector mb-1 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),

        }

class ClosingCashReceiptForm(forms.ModelForm):
    class Meta:
        model = ClosingCashReceipt
        fields = ['cash_receipt', 'count']

        widgets = {
            'cash_receipt': forms.Select(attrs={'class': 'form-control'}),
            'count': forms.NumberInput(attrs={'class': 'form-control'}),
        }
