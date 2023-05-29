from django.shortcuts import render, get_object_or_404
from .models import Product, VehicleModel, ProductPrice, Order, OrderLine, Status
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.

def homepage(request):

    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits + 1

    context = {
        'service_count': Product.objects.count(),
        'orders_count': Order.objects.count(),
        'orders_done': Status.objects.filter(name='Done').count(),
        'num_visits': num_visits,
    }
    return render(request, 'homepage.html', context=context)

def products(request):
    context = {
        'products': Product.objects.all()
    }
    return render(request, 'products.html', context=context)

def product(request, product_id):
    context = {
        'product': get_object_or_404(Product, pk=product_id),
        'models': VehicleModel.objects.all(),
        # 'prices': ProductPrice.objects.filter(pk=product_id)
        # 'prices': ProductPrice.objects.filter(pk=product_id).all(),
        # 'prices': get_object_or_404(ProductPrice, pk=product_id),
    }
    return render(request, 'product.html', context=context)

class OrderListView(generic.ListView):
    model = Order
    template_name = 'orders.html'
    context_object_name = 'orders'

class OrderDetailView(generic.DetailView):
    model = Order
    template_name = 'order.html'
    context_object_name = 'order'

class UserOrdersListView(LoginRequiredMixin, generic.ListView):
    model = Order
    template_name = 'user_orders.html'
    context_object_name = 'user_orders'

    def get_queryset(self):
        return Order.objects.filter(customer=self.request.user)


