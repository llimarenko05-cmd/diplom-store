from django.contrib import admin
from .models import ActionLog, Category, Product, Sale, StockReceipt, Supplier


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "phone", "email")
    search_fields = ("name", "phone", "email")
    list_filter = ("name",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "category",
        "supplier",
        "gender",
        "size",
        "color",
        "article",
        "price",
        "quantity",
        "minimum_quantity",
    )
    list_filter = ("category", "supplier", "gender", "size", "color")
    search_fields = ("name", "article")


@admin.register(StockReceipt)
class StockReceiptAdmin(admin.ModelAdmin):
    list_display = ("id", "product", "quantity", "supplier", "receipt_date")
    list_filter = ("receipt_date", "supplier")
    search_fields = ("product__name", "supplier", "comment")


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ("id", "product", "quantity", "sale_date")
    list_filter = ("sale_date",)
    search_fields = ("product__name", "comment")


@admin.register(ActionLog)
class ActionLogAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "action_type", "product", "created_at")
    list_filter = ("action_type", "created_at")
    search_fields = ("user__username", "product__name", "description")
