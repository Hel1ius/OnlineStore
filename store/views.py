from django.db.models import Q
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, View

from .models import Product, Category, Manufacturer
from .forms.review_forms import ReviewForm
from cart.forms import CartAddProductForm


class HomeView(ListView):
    """Домашняя страница"""
    model = Product
    context_object_name = 'home_list'
    template_name = 'store/home.html'


class ProductsView(ListView):
    """Список товаров"""
    model = Product
    context_object_name = 'product_list'
    template_name = 'store/product_list.html'
    queryset = Product.objects.filter(draft=False)
    paginate_by = 9
    ordering = '-time_in'



class ProductDetailView(DetailView):
    """Детальная информация о товаре"""
    model = Product
    slug_field = 'url'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart_product_form'] = CartAddProductForm()
        return context

class AddReview(View):
    """Отправка отзыва"""
    def post(self, request, pk):
        form = ReviewForm(request.POST)
        product = Product.objects.get(id=pk)
        if form.is_valid():
            form = form.save(commit=False)
            form.product = product
            form.save()
        return redirect(product.get_absolute_url())


class ProductInCategory(ListView):
    """Фильтрация по выпадающему меню Shop"""
    model = Product
    template_name = 'store/product_list.html'
    context_object_name = 'product_list'

    def get_queryset(self):
        name = self.kwargs['name']
        categories = Category.objects.values_list('name', flat=True)
        manufacturers = Manufacturer.objects.values_list('name', flat=True)
        if name in categories:
            return Product.objects.filter(category__name=name)
        else:
            return Product.objects.filter(manufacturer__name=name)


class FilterProductView(ListView):
    """Фильтрация фильмов в product_list"""
    def get_queryset(self):
        queryset = Product.objects.filter(
            category__in=self.request.GET.getlist('category'), manufacturer__in=self.request.GET.getlist('manufacturer')
        )
        print(queryset)
        return queryset

#TODO СДЕЛАТЬ ДОБАВЛЕНИЕ ТОВАРА В КОРЗИНУ!
class AddToCart(View):
    def get(self, request):
        pass


# class AddReview(View):
#     """Отправка отзыва"""
#     def post(self, request, pk):
#         form = ReviewForm(request.POST)
#         product = Product.objects.get(id=pk)
#         if form.is_valid():
#             form = form.save(commit=False)
#             form.product = product
#             form.save()
#         return redirect(product.get_absolute_url())