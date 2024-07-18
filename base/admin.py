from django.contrib import admin
from .models import *

admin.site.register(EntityType)
admin.site.register(Client)
admin.site.register(Supplier)
admin.site.register(Store)
# finances
admin.site.register(Cashdesk)
admin.site.register(CashdeskClosing)
admin.site.register(CashReceipt)
admin.site.register(ClosingCashReceipt)
admin.site.register(Transaction)
admin.site.register(Payment)
admin.site.register(Debt)
admin.site.register(Receivable)
# products
admin.site.register(Lot)
admin.site.register(Category)
admin.site.register(Family)
admin.site.register(Product)
admin.site.register(ProductStock)
# sales
admin.site.register(Sale)
admin.site.register(SaleItem)
# purchases
admin.site.register(Purchase)
admin.site.register(PurchaseItem)
# stock operations
admin.site.register(StockOperation)
admin.site.register(StockOperationItem)
# inventories
admin.site.register(Inventory)
admin.site.register(InventoryItem)
