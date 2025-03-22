from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404

from .models import ProductPage, Order, OrderItem


# Добавление товара в корзину (с использованием сессии)
def add_to_basket(request, product_id):
    product = get_object_or_404(ProductPage, id=product_id)
    basket = request.session.get('basket', {})
    basket[str(product_id)] = basket.get(str(product_id), 0) + 1
    request.session['basket'] = basket
    total_items = sum(basket.values())
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'basket_count': total_items})
    else:
        return redirect('basket')


# Удаление товара из корзины
def remove_from_basket(request, product_id):
    basket = request.session.get('basket', {})
    if str(product_id) in basket:
        del basket[str(product_id)]
    request.session['basket'] = basket
    return redirect('basket')


# Обновление количества товаров в корзине
def update_basket(request):
    if request.method == 'POST':
        basket = request.session.get('basket', {})
        for key, value in request.POST.items():
            if key.isdigit():
                basket[key] = int(value)
        request.session['basket'] = basket
    return redirect('basket')


# Отображение корзины
def basket_view(request):
    basket = request.session.get('basket', {})
    items = []
    total = 0
    for product_id, quantity in basket.items():
        product = get_object_or_404(ProductPage, id=product_id)
        item_total = product.price * quantity
        total += item_total
        items.append(
            {
                'product': product,
                'quantity': quantity,
                'item_total': item_total,
            }
        )
    context = {
        'items': items,
        'total': total,
    }
    return render(request, 'shop/basket.html', context)


# Оформление заказа
def order_create(request):
    basket = request.session.get('basket', {})
    if request.method == 'POST':
        customer_name = request.POST.get('customer_name')
        customer_phone = request.POST.get('customer_phone')
        delivery_method = request.POST.get('delivery_method')
        # Расчет итоговой суммы
        total = 0
        for product_id, quantity in basket.items():
            product = get_object_or_404(ProductPage, id=product_id)
            total += product.price * quantity
        order = Order.objects.create(
            customer_name=customer_name,
            customer_phone=customer_phone,
            delivery_method=delivery_method,
            total_amount=total,
        )
        for product_id, quantity in basket.items():
            product = get_object_or_404(ProductPage, id=product_id)
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                price=product.price,
            )
        # Очистка корзины после оформления заказа
        request.session['basket'] = {}
        return redirect('order_success')  # Создайте страницу подтверждения заказа
    return render(request, 'shop/order_form.html')
