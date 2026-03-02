from django.contrib import admin
from .models import (
    Supplier, Product, Warehouse, InventoryLocation, Movement,
    QualityControl, PurchaseOrder, SalesOrder, SalesAnalytics, Forecast
)


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'city', 'created_at']
    search_fields = ['name', 'email', 'city']
    list_filter = ['city', 'country', 'created_at']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'barcode', 'category', 'supplier', 'unit_price', 'status']
    search_fields = ['name', 'barcode', 'category']
    list_filter = ['category', 'status', 'supplier']


@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = ['name', 'city', 'manager_name', 'capacity']
    search_fields = ['name', 'city']
    list_filter = ['city', 'country']


@admin.register(InventoryLocation)
class InventoryLocationAdmin(admin.ModelAdmin):
    list_display = ['product', 'warehouse', 'aisle', 'rack', 'quantity', 'batch_number']
    search_fields = ['product__name', 'warehouse__name', 'batch_number']
    list_filter = ['warehouse', 'expiry_date']


@admin.register(Movement)
class MovementAdmin(admin.ModelAdmin):
    list_display = ['movement_type', 'inventory_location', 'quantity', 'reference_number', 'created_at']
    search_fields = ['reference_number', 'inventory_location__product__name']
    list_filter = ['movement_type', 'created_at']


@admin.register(QualityControl)
class QualityControlAdmin(admin.ModelAdmin):
    list_display = ['inventory_location', 'status', 'checked_by', 'created_at']
    search_fields = ['inventory_location__product__name', 'status']
    list_filter = ['status', 'created_at']


@admin.register(PurchaseOrder)
class PurchaseOrderAdmin(admin.ModelAdmin):
    list_display = ['po_number', 'supplier', 'product', 'quantity', 'total_cost', 'status']
    search_fields = ['po_number', 'supplier__name', 'product__name']
    list_filter = ['status', 'created_at', 'expected_delivery']


@admin.register(SalesOrder)
class SalesOrderAdmin(admin.ModelAdmin):
    list_display = ['so_number', 'product', 'quantity', 'customer_name', 'status']
    search_fields = ['so_number', 'product__name', 'customer_name']
    list_filter = ['status', 'created_at', 'ship_date']


@admin.register(SalesAnalytics)
class SalesAnalyticsAdmin(admin.ModelAdmin):
    list_display = ['product', 'date', 'units_sold', 'revenue']
    search_fields = ['product__name']
    list_filter = ['date', 'product']


@admin.register(Forecast)
class ForecastAdmin(admin.ModelAdmin):
    list_display = ['product', 'forecast_date', 'predicted_demand', 'confidence_score']
    search_fields = ['product__name']
    list_filter = ['forecast_date', 'product']
