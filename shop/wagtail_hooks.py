from wagtail_modeladmin.options import (
    ModelAdmin, modeladmin_register
)
from .models import Order, OrderItem


class OrderAdmin(ModelAdmin):
    model = Order
    menu_label = "Заказы"
    menu_icon = "list-ul"  # иконка из Wagtail, можно поменять
    menu_order = 200
    list_display = ("id", "customer_name", "customer_phone", "status", "created_at")
    list_filter = ("status",)
    search_fields = ("customer_name", "customer_phone")


class OrderItemAdmin(ModelAdmin):
    model = OrderItem
    menu_label = "Позиции заказа"
    menu_icon = "list-ol"
    menu_order = 210
    list_display = ("id", "order", "product", "quantity", "price")


# Регистрируем обе «админки»:
modeladmin_register(OrderAdmin)
modeladmin_register(OrderItemAdmin)
