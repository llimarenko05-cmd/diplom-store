from django.urls import path
from . import views

urlpatterns = [
    path('', views.role_redirect, name='role_redirect'),
    path('home/', views.home, name='home'),

    path('products/', views.product_list, name='product_list'),
    path('products/export/', views.export_products_excel, name='export_products_excel'),
    path('products/create/', views.create_product, name='create_product'),
    path('products/<int:product_id>/', views.product_detail, name='product_detail'),
    path('products/<int:product_id>/edit/', views.edit_product, name='edit_product'),
    path('products/<int:product_id>/delete/', views.delete_product, name='delete_product'),
    path('products/<int:product_id>/history/', views.product_history, name='product_history'),

    path('stock/', views.stock_list, name='stock_list'),

    path('low-stock/', views.low_stock, name='low_stock'),
    path('low-stock/export/', views.export_low_stock_excel, name='export_low_stock_excel'),

    path('replenishment/', views.replenishment_list, name='replenishment_list'),
    path('replenishment/export/', views.export_replenishment_excel, name='export_replenishment_excel'),

    path('no-movement/', views.no_movement_products, name='no_movement_products'),
    path('no-movement/export/', views.export_no_movement_excel, name='export_no_movement_excel'),

    path('action-log/', views.action_log_list, name='action_log_list'),

    path('sales/create/', views.create_sale, name='create_sale'),
    path('receipts/create/', views.create_receipt, name='create_receipt'),

    path('sales/report/', views.sales_report, name='sales_report'),
    path('sales/report/export/', views.export_sales_report_excel, name='export_sales_report_excel'),

   path('sales/new/', views.create_sale_order, name='create_sale_order'),
]
