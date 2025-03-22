from django.urls import path
from . import views

urlpatterns = [
    path('basket/', views.basket_view, name='basket'),
    path('basket/add/<int:product_id>/', views.add_to_basket, name='add_to_basket'),
    path('basket/remove/<int:product_id>/', views.remove_from_basket, name='remove_from_basket'),
    path('basket/update/', views.update_basket, name='update_basket'),
    path('order/create/', views.order_create, name='order_create'),
    # Путь для страницы успешного оформления заказа (её нужно создать)
    path('order/success/', views.order_create, name='order_success'),
]
