from django.contrib import admin
from .models import OrderItem, Order

from simple_history.admin import SimpleHistoryAdmin
from import_export.admin import ImportExportModelAdmin


class OrderAdmin(SimpleHistoryAdmin, ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['first_name', 'address', 'phone', 'status']

admin.site.register(Order, OrderAdmin)


class OrderItemAdmin(SimpleHistoryAdmin, ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['price', 'product', 'order']

admin.site.register(OrderItem, OrderItemAdmin)

