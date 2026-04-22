from django.contrib import admin
from .models import (
    Category,
    Supplier,
    Product,
    StockReceipt,
    Sale,
    SaleOrder,
    SaleItem,
    ReceiptOrder,
    ReceiptItem,
    ActionLog,
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phone', 'email')
    search_fields = ('name', 'phone', 'email')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'category',
        'supplier',
        'gender',
        'size',
        'color',
        'article',
        'price',
        'quantity',
        'minimum_quantity',
    )
    list_filter = ('category', 'gender', 'size', 'color')
    search_fields = ('name', 'article', 'color')


@admin.register(StockReceipt)
class StockReceiptAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'quantity', 'supplier', 'receipt_date')
    list_filter = ('receipt_date', 'supplier')
    search_fields = ('product__name', 'supplier', 'comment')


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'quantity', 'sale_date')
    list_filter = ('sale_date',)
    search_fields = ('product__name', 'comment')


class SaleItemInline(admin.TabularInline):
    model = SaleItem
    extra = 0


@admin.register(SaleOrder)
class SaleOrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at')
    inlines = [SaleItemInline]


class ReceiptItemInline(admin.TabularInline):
    model = ReceiptItem
    extra = 0


@admin.register(ReceiptOrder)
class ReceiptOrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'supplier_name', 'created_at')
    inlines = [ReceiptItemInline]


@admin.register(ActionLog)
class ActionLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at', 'user', 'action_type', 'product', 'description')
    list_filter = ('action_type', 'created_at')
    search_fields = ('user__username', 'product__name', 'description')
