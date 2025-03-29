from django.db import models
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail.models import Orderable, Page
from wagtail.admin.panels import FieldPanel
from wagtail.fields import StreamField
from wagtail.images import get_image_model_string
from wagtail.admin.panels import InlinePanel, MultiFieldPanel


class ProductImage(Orderable):
    page = ParentalKey('shop.ProductPage', on_delete=models.CASCADE, related_name='gallery_images')
    image = models.ForeignKey(
        get_image_model_string(),
        on_delete=models.CASCADE,
        related_name='+',
        verbose_name="Изображение"
    )
    caption = models.CharField(blank=True, max_length=250, verbose_name="Подпись")

    panels = [
        FieldPanel('image'),
        FieldPanel('caption'),
    ]


# class ProductPage(Page):
#     price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
#     description = models.TextField(verbose_name="Описание")
#     image = models.ImageField(upload_to='products/', null=True, blank=True, verbose_name="Изображение")
#
#     content_panels = Page.content_panels + [
#         FieldPanel('price'),
#         FieldPanel('description'),
#         FieldPanel('image'),
#     ]

class ProductPage(Page):
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    description = models.TextField(verbose_name="Описание")

    content_panels = Page.content_panels + [
        FieldPanel('price'),
        FieldPanel('description'),
        InlinePanel('gallery_images', label="Галерея изображений"),
    ]


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата заказа")
    customer_name = models.CharField(max_length=255, verbose_name="Имя покупателя")
    customer_phone = models.CharField(max_length=50, verbose_name="Телефон")
    delivery_method = models.CharField(
        max_length=50,
        choices=(
            ('post', 'Почта'),
            ('courier', 'Курьер'),
            ('pickup', 'Самовывоз'),
        ),
        verbose_name="Способ доставки"
    )
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Итоговая сумма")
    status = models.CharField(max_length=50, default='new', verbose_name="Статус заказа")

    def __str__(self):
        return f"Заказ #{self.id} от {self.customer_name}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE, verbose_name="Заказ")
    product = models.ForeignKey(ProductPage, on_delete=models.CASCADE, verbose_name="Продукт")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Количество")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")

    def __str__(self):
        return f"{self.product.title} x {self.quantity}"


class HomePage(Page):
    """
    Главная страница сайта.
    В шаблоне будем выводить каталог товаров (ProductPage).
    """
    # Пример дополнительного поля для главной страницы
    introduction = models.TextField(
        blank=True,
        help_text="Краткое описание или приветственный текст на главной странице"
    )

    content_panels = Page.content_panels + [
        FieldPanel('introduction'),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        # products = ProductPage.objects.live()

        # 2. Если хотим показывать только товары, которые являются дочерними страницами HomePage:
        products = ProductPage.objects.child_of(self).live()

        context['products'] = products
        return context

    class Meta:
        verbose_name = "Главная страница"
        verbose_name_plural = "Главные страницы"
