from django.shortcuts import render, redirect
from datetime import datetime
from home.models import Contact, Product, Order, OrderItem, CartItem
from django.contrib import messages
from decimal import Decimal
from django.db.models import Q
from home.forms import ContactForm  # ✅ import the form
from home.forms import OrderForm


def index(request):
    products = Product.objects.all()
    return render(request, "index.html", {'products': products})


def about(request):
    return render(request, "about.html")


def contact(request):
    success = False
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save(commit=False)
            contact.date = datetime.today()
            contact.save()
            messages.success(request, f"Thank you, {contact.name}! Your message has been submitted successfully.")
            success = True
            form = ContactForm()  # Clear form after submission
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ContactForm()

    return render(request, "contact.html", {'form': form, 'success': success})


def add_to_cart(request, product_id):
    cart = request.session.get('cart', {})
    if not isinstance(cart, dict):
        cart = {}

    product_id_str = str(product_id)
    cart[product_id_str] = cart.get(product_id_str, 0) + 1
    request.session['cart'] = cart
    request.session.modified = True
    messages.success(request, "Product added to cart!")
    return redirect('cart')


def cart_view(request):
    cart = request.session.get('cart', {})
    if not isinstance(cart, dict):
        cart = {}
        request.session['cart'] = cart

    products_in_cart = []
    total = Decimal('0.00')

    for product_id, quantity in cart.items():
        product_qs = Product.objects.filter(id=product_id)
        if product_qs.exists():
            product = product_qs.first()
            subtotal = product.price * Decimal(quantity)
            products_in_cart.append({'product': product, 'quantity': quantity, 'subtotal': subtotal})
            total += subtotal

    return render(request, 'cart.html', {'products': products_in_cart, 'total': total})


def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    if not isinstance(cart, dict):
        cart = {}
    cart.pop(str(product_id), None)
    request.session['cart'] = cart
    request.session.modified = True
    messages.info(request, "Item removed from cart.")
    return redirect('cart')


def confirm_order(request):
    cart_items = CartItem.objects.all()
    total = sum(item.product.price * item.quantity for item in cart_items)

    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.total_price = total
            order.status = "Order Listed"
            order.save()

            # create OrderItems for each CartItem
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    subtotal=item.product.price * item.quantity
                )

            cart_items.delete()  # clear the cart after confirming order
            messages.success(request, "✅ Your order has been placed successfully!")
            return redirect("orders")
    else:
        form = OrderForm()

    return render(request, "confirm_order.html", {"form": form, "cart_items": cart_items, "total": total})
def my_orders(request):
    orders = Order.objects.all().order_by('-created_at')
    return render(request, 'my_orders.html', {'orders': orders})


def delete_order(request, order_id):
    order_qs = Order.objects.filter(id=order_id)
    if not order_qs.exists():
        messages.error(request, "❌ Order not found.")
        return redirect('my_orders')

    order = order_qs.first()
    if order.status.lower() == 'listed':
        order.delete()
        messages.success(request, "🗑️ Order deleted successfully!")
    else:
        messages.warning(request, "⚠️ Cannot delete order once it's on the way or delivered.")
    return redirect('my_orders')


def search(request):
    query = request.GET.get('q', '').strip()
    products, orders = [], []

    if query:
        products = Product.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )
        orders = Order.objects.filter(
            Q(customer_name__icontains=query)
            | Q(phone__icontains=query)
            | Q(orderitem__product__name__icontains=query)
        ).distinct()

    context = {
        'query': query,
        'products': products,
        'orders': orders,
    }
    return render(request, 'search_results.html', context)