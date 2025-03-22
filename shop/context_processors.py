def basket_count(request):
    """
    Возвращает общее количество товаров в корзине, чтобы можно было
    отобразить это число в шапке сайта при каждом рендере страницы.
    """
    basket = request.session.get('basket', {})
    count = sum(basket.values())
    return {'basket_count': count}
