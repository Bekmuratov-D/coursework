from django.shortcuts import render

import stripe

from django.conf import settings
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import render
from rest_framework import viewsets

from rest_framework import status, authentication, permissions
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.filters import OrderingFilter, SearchFilter 
import django_filters.rest_framework
from django.utils import timezone
from rest_framework.decorators import action

from .models import Order, OrderItem
from .pagination import *
from .serializers import OrderSerializer, MyOrderSerializer, OrderItemSerializer

@api_view(['POST'])                                               
@authentication_classes([authentication.TokenAuthentication])         
@permission_classes([permissions.IsAuthenticated])
def checkout(request):
    serializer = OrderSerializer(data=request.data)

    if serializer.is_valid():
        stripe.api_key = settings.STRIPE_SECRET_KEY
        paid_amount = sum(item.get('quantity') * item.get('product').price for item in serializer.validated_data['items'])

        try:
            charge = stripe.Charge.create(
                amount=int(paid_amount * 100),
                currency='USD',
                description='Charge from Djackets',
                source=serializer.validated_data['stripe_token']
            )

            serializer.save(user=request.user, paid_amount=paid_amount)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OrdersList(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        orders = Order.objects.filter(user=request.user)
        serializer = MyOrderSerializer(orders, many=True)
        return Response(serializer.data)

class Orders_tableViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class =  OrderSerializer
    pagination_class = OrderPagination
    filter_backends = [OrderingFilter, SearchFilter, django_filters.rest_framework.DjangoFilterBackend]
    search_fields = ['address', 'first_name', 'phone']
    ordering_fields = ['first_name']
    filterset_fields = ['first_name', 'address', 'phone']

    @action(methods=['GET'], detail=False)
    def recent_orders(self, request):
        latest_orders = Order.objects.filter(created_at__lte=timezone.now()).order_by('-created_at')[:2]
        serializer = self.get_serializer(latest_orders, many=True)
        return Response(serializer.data)

    @action(methods=['POST'], detail=True, url_path='order_completed')
    def order_completed(self, request, pk=None):
        order = self.queryset.get(id=pk)
        order.status = 'заказ выполнен'
        order.save()
        serializer = self.get_serializer(order)
        return Response(serializer.data)

    @action(methods=['POST'], detail=True, url_path='order_in_progress')
    def order_in_progress(self, request, pk=None):
        order = self.queryset.get(id=pk)
        order.status = 'Заказ выполняется'
        order.save()
        serializer = self.get_serializer(order)
        return Response(serializer.data)

class Order_item_tableViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class =  OrderItemSerializer
    
