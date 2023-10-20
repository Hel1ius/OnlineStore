from django import template

from store.models import Category, Manufacturer, Product

register = template.Library()


@register.simple_tag()
def get_categories():
    """Вывод категорий"""
    return Category.objects.all()


@register.simple_tag()
def get_manufacturers():
    """Вывод производителей"""
    return Manufacturer.objects.all()


@register.inclusion_tag('store/tags/featured_products.html')
def get_featured_products():
    """Вывод новых и популярных товаров на домашней странице"""
    new_products = Product.objects.filter(is_new=True)[:10]
    trend_products = Product.objects.filter(is_hit=True)[:10]
    return {'new_products': new_products, 'trend_products': trend_products}


@register.inclusion_tag('store/tags/filter_products.html')
def get_filter_products():
    """Фильтр для страницы product_list"""
    categories = Category.objects.all()
    manufacturers = Manufacturer.objects.all()
    return {'categories': categories, 'manufacturers': manufacturers}