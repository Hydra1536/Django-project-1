from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from home import views

urlpatterns = [
    # Core pages
    path("", views.index, name="home"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path("search/", views.search, name="search"),
    # Cart management
    path("cart/", views.cart_view, name="cart"),
    path("add-to-cart/<int:product_id>/", views.add_to_cart, name="add_to_cart"),
    path("remove/<int:product_id>/", views.remove_from_cart, name="remove_from_cart"),
    # RESTful order routes (no GET)
    path("orders/", views.create_order, name="create_order"),  # POST only
    path(
        "orders/<int:pk>/", views.update_or_delete_order, name="update_or_delete_order"
    ),  # PUT, DELETE
    # UI
    path("my_orders/", views.my_orders, name="my_orders"),
    path(
        "order_confirmed/<int:order_id>/", views.order_confirmed, name="order_confirmed"
    ),
    path("delete_order/<int:order_id>/", views.delete_order, name="delete_order"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
