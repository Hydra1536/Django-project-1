from datetime import datetime
from decimal import Decimal
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse, HttpResponseNotAllowed
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt

from home.forms import ContactForm, OrderForm
from home.models import Contact, Order, OrderItem, Product


# -------------------- BASIC PAGES --------------------
def index(request):
    products = Product.objects.all()
    return render(request, "index.html", {"products": products})


def about(request):
    return render(request, "about.html")


# -------------------- CONTACT --------------------
def contact(request):
    success = False
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save(commit=False)
            contact.date = datetime.today()
            contact.save()
            messages.success(request, f"Thank you, {contact.name}! Message received.")
            success = True
            form = ContactForm()
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ContactForm()
    return render(request, "contact.html", {"form": form, "success": success})


# -------------------- CART --------------------
def add_to_cart(request, product_id):
    cart = request.session.get("cart", {})
    cart[str(product_id)] = cart.get(str(product_id), 0) + 1
    request.session["cart"] = cart
    request.session.modified = True
    messages.success(request, "✅ Product added to cart!")
    return redirect("cart")


def cart_view(request):
    cart = request.session.get("cart", {})
    products_in_cart, total = [], Decimal("0.00")

    for pid, qty in cart.items():
        try:
            product = Product.objects.get(id=pid)
            subtotal = product.price * qty
            products_in_cart.append({"product": product, "quantity": qty, "subtotal": subtotal})
            total += subtotal
        except Product.DoesNotExist:
            continue

    form = OrderForm()
    return render(request, "cart.html", {"products": products_in_cart, "total": total, "form": form})


def remove_from_cart(request, product_id):
    cart = request.session.get("cart", {})
    cart.pop(str(product_id), None)
    request.session["cart"] = cart
    request.session.modified = True
    messages.info(request, "🗑️ Item removed from cart.")
    return redirect("cart")


# -------------------- RESTFUL ORDER ENDPOINTS --------------------

@csrf_exempt
@require_http_methods(["POST"])
def create_order(request):
    """
    POST /orders/ → Create new order (from session cart)
    """
    cart = request.session.get("cart", {})
    if not cart:
        return JsonResponse({"error": "Cart is empty!"}, status=400)

    form = OrderForm(request.POST)
    if not form.is_valid():
        return JsonResponse({"errors": form.errors}, status=400)

    order = form.save(commit=False)
    total = Decimal("0.00")

    for pid, qty in cart.items():
        try:
            product = Product.objects.get(id=pid)
            total += product.price * qty
        except Product.DoesNotExist:
            continue

    order.total_price = total
    order.status = "listed"
    order.save()

    # Add ordered items
    for pid, qty in cart.items():
        product = Product.objects.get(id=pid)
        OrderItem.objects.create(order=order, product=product, quantity=qty)

    # Clear session cart after placing order
    request.session["cart"] = {}
    request.session.modified = True

    return JsonResponse({"message": "Order placed successfully!", "order_id": order.id})


@csrf_exempt
@require_http_methods(["PUT", "DELETE"])
def update_or_delete_order(request, pk):
    """
    PUT /orders/<id>/?status=on_the_way → Update order status  
    DELETE /orders/<id>/ → Delete order (only if listed)
    """
    order = get_object_or_404(Order, pk=pk)

    if request.method == "PUT":
        new_status = request.GET.get("status")
        if new_status not in dict(Order.STATUS_CHOICES):
            return JsonResponse({"error": "Invalid status"}, status=400)
        order.status = new_status
        order.save()
        return JsonResponse({"message": "Order status updated", "status": order.status})

    elif request.method == "DELETE":
        if order.status != "listed":
            return JsonResponse(
                {"error": "Cannot delete order that is On the Way or Delivered"}, status=400
            )
        order.delete()
        return JsonResponse({"message": "Order deleted successfully"})


# -------------------- UI --------------------
def my_orders(request):
    orders = Order.objects.all().order_by("-created_at")
    return render(request, "my_orders.html", {"orders": orders})


# -------------------- SEARCH --------------------
def search(request):
    query = request.GET.get("q", "").strip()
    context = {"query": query, "products": [], "orders": []}

    if query:
        context["products"] = Product.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )
        context["orders"] = Order.objects.filter(
            Q(customer_name__icontains=query)
            | Q(phone__icontains=query)
            | Q(items__product__name__icontains=query)
        ).distinct()

    return render(request, "search_results.html", context)
