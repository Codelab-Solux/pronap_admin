from .models import *
from django import forms
from django.forms import ModelForm
from django.forms import inlineformset_factory


class TimeInput(forms.TimeInput):
    input_type = 'time'


class DateInput(forms.DateInput):
    input_type = 'date'


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('__all__')
        labels = {'name': 'Nom', 'is_featured':'En vedette' }
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
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': "mb-1 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),
            'brand': forms.TextInput(attrs={'class': "mb-1 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),
            'store': forms.Select(attrs={ 'class': "mb-1 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),
            'supplier': forms.Select(attrs={ 'class': "mb-1 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),
            'category': forms.Select(attrs={ 'class': "input_selector mb-1 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),
            'family': forms.Select(attrs={'class': "input_selector mb-1 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),
            'unit': forms.Select(attrs={ 'class': "mb-1 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),
            'quantity': forms.NumberInput(attrs={'class': "mb-1 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),
            'price': forms.NumberInput(attrs={'class': "mb-1 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),
            'promo_price': forms.NumberInput(attrs={'class': "mb-1 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),
            'description': forms.Textarea(attrs={"rows": "10", 'class': "mb-2 px-4 py-2 rounded-xl border focus:border-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),

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
                self.fields['Family'].queryset = self.instance.category.Family_set.order_by('name')


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
            'observation': forms.Textarea(attrs={"rows": "10", 'class': "mb-2 px-4 py-2 rounded-xl border focus:border-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),
            'production_date': DateInput(attrs={'class': "mb-1 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),
            'expiration_date': DateInput(attrs={'class': "mb-1 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),

        }

class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = '__all__'

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
            'entity_type': forms.Select(attrs={'class': "mb-1 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),
            'domain': forms.TextInput(attrs={'class': "mb-2 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-green-400 w-full"}),
        }


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = '__all__'

        labels = {
            'name': 'Nom',
            'entity_type': 'Type',
            'sex': 'Sexe',
            'phone': 'Telephone',
            'address': 'Adresse',
            'domain': 'Secteur',
        }
        widgets = {
            'entity_type': forms.Select(attrs={'class': "mb-1 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),
            'name': forms.TextInput(attrs={'class': "mb-2 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-green-400 w-full"}),
            'phone': forms.TextInput(attrs={'class': "mb-2 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-green-400 w-full"}),
            'address': forms.TextInput(attrs={'class': "mb-2 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-green-400 w-full"}),
            'email': forms.EmailInput(attrs={'class': "mb-2 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-green-400 w-full"}),
            'sex': forms.Select(attrs={'class': "mb-1 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),
            'domain': forms.TextInput(attrs={'class': "mb-2 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-green-400 w-full"}),
        }

class ServicePurchaseForm(forms.ModelForm):
    class Meta:
        model = ServicePurchase
        fields = '__all__'
        exclude = ('audit','timestamp',)

        labels = {
            'store': 'Boutique',
            'supplier': 'Fournisseur',
            'label': 'Libelé',
            'total': 'Montant',
            'cashdesk': 'Caisse',
            'payment_option': 'Moyen de paiement',
            'payment_status': 'Status du paiement',
        }
        widgets = {
            'store': forms.Select(attrs={'class': "mb-1 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),
            'supplier': forms.Select(attrs={'class': "mb-1 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),
            'label': forms.TextInput(attrs={'class': "mb-2 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-green-400 w-full"}),
            'total': forms.TextInput(attrs={'class': "mb-2 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-green-400 w-full"}),
            'cashdesk': forms.Select(attrs={'class': "mb-1 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),
            'payment_option': forms.Select(attrs={'class': "mb-1 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),
            'payment_status': forms.Select(attrs={'class': "mb-1 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),
            'description': forms.Textarea(attrs={"rows": "10", 'class': "mb-2 px-4 py-2 rounded-xl border focus:border-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),

       }

class ProductPurchaseForm(forms.ModelForm):
    class Meta:
        model = ProductPurchase
        fields = '__all__'
        exclude = ('audit', 'timestamp', 'product_stocks')

        labels = {
            'store': 'Boutique',
            'supplier': 'Fournisseur',
            'label': 'Libelé',
            'total': 'Montant',
            'cashdesk': 'Caisse',
            'payment_option': 'Moyen de paiement',
            'payment_status': 'Status du paiement',
        }
        widgets = {
            'store': forms.Select(attrs={'class': "mb-1 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),
            'supplier': forms.Select(attrs={'class': "mb-1 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),
            'label': forms.TextInput(attrs={'class': "mb-2 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-green-400 w-full"}),
            'total': forms.TextInput(attrs={'class': "mb-2 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-green-400 w-full"}),
            'discount': forms.TextInput(attrs={'class': "mb-2 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-green-400 w-full"}),
            'cashdesk': forms.Select(attrs={'class': "mb-1 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),
            'payment_option': forms.Select(attrs={'class': "mb-1 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),
            'payment_status': forms.Select(attrs={'class': "mb-1 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),
            'observation': forms.Textarea(attrs={"rows": "10", 'class': "mb-2 px-4 py-2 rounded-xl border focus:border-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),

       }


class StockInputForm(forms.ModelForm):
            
    class Meta:
        model = StockInput
        fields = ['initiator', 'type', 'description']

        labels = {
            'type': "Type d'entrée",
            'initiator': 'Initiateur',
        }
        widgets = {
            'initiator': forms.Select(attrs={'class': "input_selector mb-1 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),
            'type': forms.Select(attrs={'class': "mb-1 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),
            'description': forms.Textarea(attrs={"rows": "5", 'class': "mb-2 px-4 py-2 rounded-xl border focus:border-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),

        }

class StockOutputForm(forms.ModelForm):
            
    class Meta:
        model = StockOutput
        fields = ['initiator', 'type', 'description']

        labels = {
            'type': "Type de sortie",
            'initiator': 'Initiateur',
        }
        widgets = {
            'initiator': forms.Select(attrs={'class': "input_selector mb-1 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),
            'type': forms.Select(attrs={'class': "mb-1 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),
            'description': forms.Textarea(attrs={"rows": "5", 'class': "mb-2 px-4 py-2 rounded-xl border focus:border-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),

        }

class InventoryForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = '__all__'

        labels = {
            'supervisor': "Superviseur",
            'initiator': 'Initiateur',
        }
        widgets = {
            'supervisor': forms.Select(attrs={'class': "input_selector mb-1 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),
            'initiator': forms.Select(attrs={'class': "input_selector mb-1 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),
            'date': DateInput(attrs={'class': "mb-2 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-green-400 w-full"}),

        }


InventoryFormSet = inlineformset_factory(
    Inventory,
    InventoryItem,
    fields=['product_stock', 'quantity_expected',
            'quantity_found', 'comment'],
    extra=1,
    can_delete=True,

    labels={
        'product_stock': 'Produit',
        'quantity_expected': 'Qté theorique',
        'quantity_found': 'Qté physique',
        'comment': 'Commentaire',
    },
    widgets={
        'product_stock': forms.Select(attrs={'class': "input_selector mb-1 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),
        'quantity_expected': forms.NumberInput(attrs={'class': "mb-1 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),
        'quantity_found': forms.NumberInput(attrs={'class': "mb-1 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),
        'comment': forms.TextInput(attrs={'class': "mb-1 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-green-400 w-full"}),

    }
)

