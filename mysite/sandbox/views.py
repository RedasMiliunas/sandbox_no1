from django.shortcuts import render, get_object_or_404, redirect, reverse
from .models import Product, VehicleModel, ProductPrice, Order, OrderLine, Status
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Q
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.forms import User
from django.contrib import messages
from django.views.generic.edit import FormMixin
from .forms import OrderReviewForm, UserUpdateForm, UserProfileUpdateForm, OrderForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin
from datetime import date


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

def contacts(request):
    return render(request, 'contacts.html')


def products(request):
    paginator = Paginator(Product.objects.all(), 4)
    page_number = request.GET.get('page')
    paged_services = paginator.get_page(page_number)
    context = {
        'products': paged_services
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

def models(request):
    paginator = Paginator(VehicleModel.objects.all(), 3)
    page_number = request.GET.get('page')
    paged_models = paginator.get_page(page_number)
    context = {
        'models': paged_models,
    }
    return render(request, 'models.html', context=context)

def model(request, model_id):
    context = {
        'model': get_object_or_404(VehicleModel, pk=model_id),
        'products': Product.objects.all(),
    }
    return render(request, 'model.html', context=context)

def search(request):
    query = request.GET.get('query')
    search_results = Product.objects.filter(Q(name__icontains=query))
    # search_results2 = ProductPrice.objects.filter(Q(model__model__icontains=query))
    context = {
        'products': search_results,
        # 'products2': search_results2,
        'query': query,
    }
    return render(request, 'search.html', context=context)


# class ProductPriceListView(generic.ListView):
#     model = ProductPrice
#     template_name = 'product_price.html'
#     context_object_name = 'product_price'

class VehicleModelDetailView(generic.DetailView):
    model = VehicleModel
    template_name = 'vehicle_model.html'
    context_object_name = 'vehicle_model'


@csrf_protect
def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, f'Username "{username}" already taken!')
                return redirect('register')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, f'Email "{email}" is already in use!')
                    return redirect('register')
                else:
                    User.objects.create_user(username=username, email=email, password=password)
                    messages.info(request, f' User "{username}" successfully created! Now you can login!')
                    return redirect('login')
        else:
            messages.error(request, f'Passwords did not match!')
            return redirect('register')
    else:
       return render(request, 'registration/register.html')


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = UserProfileUpdateForm(request.POST, request.FILES, instance=request.user.userprofile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.info(request, f'Profile was successfully UPDATED!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = UserProfileUpdateForm(instance=request.user.userprofile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
    }

    return render(request, 'profile.html', context=context)


class OrderListView(LoginRequiredMixin, generic.ListView):
    model = Order
    template_name = 'orders.html'
    context_object_name = 'orders'


class OrderDetailView(FormMixin, generic.DetailView):
    model = Order
    template_name = 'order.html'
    context_object_name = 'order'
    form_class = OrderReviewForm

    def get_success_url(self):
        return reverse('order', kwargs={'pk': self.object.id})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

# galima tiesiog Generate form_valid ir return'e palikti kaip buna
    def form_valid(self, form):
        form.instance.order = self.object
        form.instance.commentator = self.request.user
        form.save()
        return super(OrderDetailView, self).form_valid(form)

class UserOrdersListView(LoginRequiredMixin, generic.ListView):
    model = Order
    template_name = 'user_orders.html'
    context_object_name = 'user_orders'

    def get_queryset(self):
        return Order.objects.filter(customer=self.request.user)

class UserOrderDetailView(LoginRequiredMixin, generic.DetailView):
    model = OrderLine
    template_name = 'user_order.html'
    context_object_name = 'user_order'


# ===================================================================================
# class CustomOrderCreateView( LoginRequiredMixin, generic.CreateView):
#     model = Order
#     success_url = '/user_orders/'
#     template_name = 'order_form.html'
#     form_class = CustomOrderForm
#
#     def form_valid(self, form):
#         form.instance.customer = self.request.user
#         return super().form_valid(form)
#
#PABANDYTI SITA!: (Video 1 val.)
#     def test_func(self):
#         authorized_customer = Order.customer.user.get(pk=self.kwargs['pk'])
#         return authorized_customer == self.request.user
# ===================================================================================
class OrderCreateView( LoginRequiredMixin, generic.CreateView):
    model = Order
    # fields = ['model', 'due_back', 'status', ]
    success_url = '/user_orders/'
    template_name = 'order_form.html'
    form_class = OrderForm
    # form_class1 = CustomOrderForm


    def form_valid(self, form):
        form.instance.customer = self.request.user
        return super().form_valid(form)


class OrderUpdateView(UserPassesTestMixin, LoginRequiredMixin, generic.UpdateView):
    model = Order
    # fields = ['model', 'due_back', 'status', ]
    form_class = OrderForm
    # success_url = '/user_orders/'
    template_name = 'order_form.html'

    def get_success_url(self):
        return reverse('order', kwargs={'pk': self.object.id})    #todo reikia 2nd ID (NE!) BUTINAI 'pk', o ne 'id'!!
    def form_valid(self, form):
        form.instance.customer = self.request.user
        return super().form_valid(form)

    def test_func(self):
        return self.get_object().customer == self.request.user

# ===================================================================================
# from django.contrib.auth.mixins import UserPassesTestMixin
#
# def is_staff_or_superuser(user):
#     return user.is_staff or user.is_superuser
#
# class OrderCreateView(LoginRequiredMixin, generic.CreateView):
#     model = Order
#     fields = ['model']
#     success_url = '/user_orders/'
#     template_name = 'order_form.html'
#
#     def form_valid(self, form):
#         form.instance.customer = self.request.user
#         return super().form_valid(form)
#
#
# class OrderUpdateView(UserPassesTestMixin, LoginRequiredMixin, generic.UpdateView):
#     model = Order
#     fields = ['model', 'due_back', 'status']
#     template_name = 'order_form.html'
#
#     def get_success_url(self):
#         return reverse('order', kwargs={'pk': self.object.id})
#
#     def form_valid(self, form):
#         form.instance.customer = self.request.user
#         return super().form_valid(form)
#
#     def test_func(self):
#         return is_staff_or_superuser(self.request.user)
# ===================================================================================
class OrderDeleteView(UserPassesTestMixin, LoginRequiredMixin, generic.DeleteView):
    model = Order
    context_object_name = 'order'
    template_name = 'order_delete.html'
    success_url = '/user_orders/'

    def test_func(self):
        return self.get_object().customer == self.request.user


# ===================================================================================

class OrderLineCreateView(LoginRequiredMixin, UserPassesTestMixin, generic.CreateView):
    model = OrderLine
    fields = ['product', 'qty']
    template_name = 'orderline_form.html'

    def test_func(self):
        order = Order.objects.get(pk=self.kwargs['pk'])
        return order.customer == self.request.user

    def get_success_url(self):
        return reverse('order', kwargs={'pk': self.kwargs['pk']})

    def form_valid(self, form):
        form.instance.order = Order.objects.get(pk=self.kwargs['pk'])
        return super().form_valid(form)
