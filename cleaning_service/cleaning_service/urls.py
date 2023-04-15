from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter



from product.views import *
from order.views import *

router = DefaultRouter()
router.register('category', Category_tableViewSet)
router.register('products', Products_tableViewSet)
router.register('orders', Orders_tableViewSet)
router.register('orders_item', Order_item_tableViewSet)



admin.site.site_header = 'Админка "Cleaning_Server"'
admin.site.index_title = 'Администрирование сайта - "Cleaning_Server"'

urlpatterns = [
    path('api/', include(router.urls)),
    path('admin/', admin.site.urls),
    path('api/v1/', include('djoser.urls')),
    path('api/v1/', include('djoser.urls.authtoken')),
    path('api/v1/', include('product.urls')),
    path('api/v1/', include('order.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
