from django.shortcuts import render, redirect, get_object_or_404
from datetime import datetime
from home.models import Contact, Product, Order, OrderItem
from django.contrib import messages
from decimal import Decimal
from django.db.models import Q

def index(request):
    products = Product.objects.all()
    return render(request, "index.html", {'products': products})

def about(request):
    return render(request, "about.html")

def cart(request):
    return render(request, "cart.html")

def contact(request):
    success = False  # Initially false
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        comments = request.POST.get('comment')  # match HTML field name

        # Save data to database
        contact = Contact(
            name=name,
            email=email,
            phone=phone,
            comments=comments,
            date=datetime.today()
        )
        contact.save()

        success = True  # To show alert after form submit
        # messages.success(request, 'Your message has been sent!')

    return render(request, "contact.html", {'success': success})

def add_to_cart(request, product_id):
    # Ensure cart exists and is always a dict
    cart = request.session.get('cart', {})
    if not isinstance(cart, dict):
        cart = {}

    product_id_str = str(product_id)
    cart[product_id_str] = cart.get(product_id_str, 0) + 1

    request.session['cart'] = cart
    request.session.modified = True

    return redirect('cart')


def cart_view(request):
    cart = request.session.get('cart', {})
    if not isinstance(cart, dict):
        cart = {}
        request.session['cart'] = cart

    products = []
    total = Decimal('0.00')

    for product_id, quantity in cart.items():
        product = Product.objects.get(id=product_id)
        subtotal = product.price * quantity
        products.append({'product': product, 'quantity': quantity, 'subtotal': subtotal})
        total += subtotal

    return render(request, 'cart.html', {'products': products, 'total': total})


def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    if not isinstance(cart, dict):
        cart = {}
    cart.pop(str(product_id), None)
    request.session['cart'] = cart
    request.session.modified = True
    return redirect('cart')

def confirm_order(request):
    if request.method == 'POST':
        name = request.POST['name']
        phone = request.POST['phone']
        address = request.POST['address']

        cart = request.session.get('cart', {})
        if not cart:
            return redirect('cart')

        total_price = 0
        order = Order.objects.create(
            customer_name=name,
            phone=phone,
            address=address,
            total_price=0,
        )

        for product_id, quantity in cart.items():
            product = Product.objects.get(id=product_id)
            total_price += product.price * quantity
            OrderItem.objects.create(order=order, product=product, quantity=quantity)

        order.total_price = total_price
        order.save()

        # Clear cart
        request.session['cart'] = {}

        return render(request, 'order_success.html', {'order': order})

    return redirect('cart')
    order = get_object_or_404(Order, id=order_id)
    if order.status == 'listed':
        order.delete()
        messages.success(request, "🗑️ Order deleted successfully!")
    else:
        messages.warning(request, "⚠️ Cannot delete order once it is on the way.")
    return redirect('cart')
def my_orders(request):
    orders = Order.objects.all().order_by('-created_at')
    return render(request, 'my_orders.html', {'orders': orders})


def delete_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if order.status == 'listed':
        order.delete()
        messages.success(request, "🗑️ Order deleted successfully!")
    else:
        messages.warning(request, "⚠️ Cannot delete order once it's on the way or delivered.")
    return redirect('my_orders')

def search(request):
    query = request.GET.get('q', '').strip()
    products = []
    orders = []

    if query:
        # Search in products
        products = Product.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )

        # Search in orders by customer name, phone, or product name (through OrderItem)
        orders = Order.objects.filter(
            Q(customer_name__icontains=query)
            | Q(phone__icontains=query)
            | Q(items__product__name__icontains=query)
        ).distinct()

    context = {
        'query': query,
        'products': products,
        'orders': orders,
    }
    return render(request, 'search_results.html', context)