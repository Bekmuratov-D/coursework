from django.contrib import admin
from django.contrib.admin import AdminSite

from .models import Category, Product

from simple_history.admin import SimpleHistoryAdmin
from import_export.admin import ImportExportModelAdmin


class CategoryAdmin(SimpleHistoryAdmin, ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['name']

admin.site.register(Category, CategoryAdmin)


class ProductAdmin(SimpleHistoryAdmin, ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['id', 'name', 'price', 'date_added']

admin.site.register(Product, ProductAdmin)