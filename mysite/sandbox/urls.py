"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views



urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('products/', views.products, name='products'),
    path('products/<int:product_id>', views.product, name='product'),
    path('orders/', views.OrderListView.as_view(), name='orders'),
    path('orders/<int:pk>', views.OrderDetailView.as_view(), name='order'),
    path('user_orders/', views.UserOrdersListView.as_view(), name='user_orders'),
    path('models/', views.models, name='models'),
    path('models/<int:model_id>', views.model, name='model'),
    path('search/', views.search, name='search'),
    path('register/', views.register, name='register'),
    # path('product_price/', views.ProductPriceListView.as_view(), name='product_price'),
    path('vehicle_model/<int:pk>', views.VehicleModelDetailView.as_view(), name='vehicle_model'),
    # path('user_orders/<int:pk>', views.UserOrderDetailView.as_view(), name='user_order'),
    path('user_orders/new', views.OrderCreateView.as_view(), name='order_new'),
    # path('user_orders/custom_new', views.CustomOrderCreateView.as_view(), name='custom_new'),
    path('orders/<int:pk>/update', views.OrderUpdateView.as_view(), name='order_update'),
    path('orders/<int:pk>/delete', views.OrderDeleteView.as_view(), name='order_delete'),
    path('orders/<int:pk>/new_orderline', views.OrderLineCreateView.as_view(), name='new_orderline'),
    path('orders/<int:order_id>/update_orderline/<int:pk>', views.OrderLineUpdateView.as_view(), name='update_orderline'),
    path('orders/<int:order_id>/delete_orderline/<int:pk>', views.OrderLineDeleteView.as_view(), name='delete_orderline'),
    path('contacts/', views.contacts, name='contacts'),
    path('profile/', views.profile, name='profile'),
]
