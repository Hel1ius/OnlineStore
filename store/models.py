from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

from autoslug import AutoSlugField


class Customer(models.Model):
    """Покупатели"""
    User = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField("Имя", max_length=100)
    ordered = models.IntegerField("Количество заказов", default=0)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Покупатель"
        verbose_name_plural = "Покупатели"


class Category(models.Model):
    """Категории"""
    name = models.CharField("Категория", max_length=100)
    description = models.TextField("Описание")
    url = models.SlugField(max_length=160, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Manufacturer(models.Model):
    """Производители"""
    name = models.CharField("Производитель", max_length=160, unique=True)
    url = models.SlugField(max_length=160, unique=True)
    website = models.CharField("Сайт", max_length=255, unique=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Производитель"
        verbose_name_plural = "Производители"


class Product(models.Model):
    """Товары"""
    name = models.CharField("Название", max_length=150)
    description = models.TextField("Описание")
    preview = models.ImageField("Изображение", upload_to='products/')
    price = models.IntegerField("Цена")
    quantity = models.IntegerField("Количество", default=0)
    is_new = models.BooleanField("Новинка", default=True)
    is_on_sale = models.BooleanField("По скидке?", default=False)
    sale_price = models.IntegerField("Цена по скидке", null=True, blank=True)
    is_hit = models.BooleanField("Хит продаж", default=False)
    bought = models.IntegerField("Продано шт", default=0)
    draft = models.BooleanField("Черновик", default=False)
    time_in = models.DateTimeField(auto_now=True)
    manufacturer = models.ForeignKey(
        Manufacturer, verbose_name="Производитель", on_delete=models.SET_NULL, null=True
    )
    category = models.ForeignKey(
        Category, verbose_name="Категория", on_delete=models.SET_NULL, null=True
    )
    url = AutoSlugField(max_length=160, unique=True, populate_from='name')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={"slug": self.url})

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"


class CharacteristicsProduct(models.Model):
    """Характеристики товара"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Товар")
    name = models.CharField("Название характеристики", max_length=150, blank=True)
    value = models.CharField("Значение характеристик", max_length=150, blank=True)

    def __str__(self):
        return f'{self.name}: {self.value}'

    class Meta:
        verbose_name = "Характеристика продукта"
        verbose_name_plural = "Характеристики продукта"


class ProductImages(models.Model):
    """Фотки товара"""
    title = models.CharField("Заголовок", max_length=100)
    image = models.ImageField("Изображение", upload_to='product_images/')
    product = models.ForeignKey(Product, verbose_name="Товар", on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Фото товара"
        verbose_name_plural = "Фотки товаров"


class Order(models.Model):
    """Заказы"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    products = models.ManyToManyField(Product, through='OrderItem')
    status = models.BooleanField("Оплачен", default=False)

    def __str__(self):
        return f'Номер вашего заказа: {self.id}'

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)


class FavoriteProduct(models.Model):
    """Избранные товары"""
    customer = models.ForeignKey(Customer, verbose_name="Покупатель", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name="Товар", on_delete=models.CASCADE)

    def __str__(self):
        return self.product

    class Meta:
        verbose_name = "Избранный товар"
        verbose_name_plural = "Избранные товары"


class Reviews(models.Model):
    """Отзывы"""
    name = models.CharField("Имя", max_length=100)
    email = models.EmailField()
    text = models.TextField("Отзыв", max_length=3000)
    product = models.ForeignKey(Product, verbose_name="Товар", on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name} - {self.product}'

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"


class RatingStar(models.Model):
    """Звезды рейтинга"""
    value = models.SmallIntegerField("Значение", default=0)

    def __str__(self):
        return f'{self.value}'

    class Meta:
        verbose_name = "Звезда рейтинга"
        verbose_name_plural = "Звезды рейтинга"
        ordering = ['-value']


class Rating(models.Model):
    """Рейтинг"""
    ip = models.CharField("IP адрес", max_length=15)
    star = models.ForeignKey(RatingStar, on_delete=models.CASCADE, verbose_name="Звезда")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Товар")

    def __str__(self):
        return f'{self.star} - {self.product}'

    class Meta:
        verbose_name = "Рейтинг"
        verbose_name_plural = "Рейтинги"
