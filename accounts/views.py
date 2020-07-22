from django.shortcuts import render, redirect
from .models import *
from .forms import OrderForm
from django.forms import inlineformset_factory
from .filters import OrderFilter

def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()

    total_customers = orders.count()
    total_orders = customers.count()

    delivered = orders.filter(status='Delivered')
    pending = orders.filter(status='Pending')

    context = {
        'orders': orders,
        'customers': customers,
        'total_customers': total_customers,
        'total_orders': total_orders,
        'delivered': delivered,
        'pending': pending
    }

    return render(request, 'accounts/dashboard.html', context)


def products(request):
    products = Product.objects.all()
    return render(request, 'accounts/products.html', {'products': products})


def customer(request, pk_test):
    customer = Customer.objects.get(id=pk_test)

    orders = customer.order_set.all()
    order_count = orders.count()

    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs

    return render(request, 'accounts/customer.html', {
        'customer': customer,
        'orders': orders,
        'order_count': order_count,
        'myFilter': myFilter
    })


def createOrder(request, pk):
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=10)
    customer = Customer.objects.get(id=pk)
    formset = OrderFormSet(request.POST or None, instance=customer)
    # form = OrderForm(request.POST or None, initial={'customer': customer})
    if formset.is_valid():
        formset.save()
        return redirect('/')

    context = {'formset': formset}
    return render(request, 'accounts/order_form.html', context)


def updateOrder(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(request.POST or None, instance=order)
    if form.is_valid():
        form.save()
        return redirect('/')
    context = {'form': form}
    return render(request, 'accounts/order_form.html', context)

def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('/')
    context = { 'order': order }
    return render(request, 'accounts/delete.html', context)