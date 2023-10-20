from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View, TemplateView

from store.models import Product
from .cart import Cart
from .forms import CartAddProductForm


class CartAddView(View):
    """Добавление товара корзину"""

    def post(self, request, pk):
        cart = Cart(request)
        product = get_object_or_404(Product, id=pk)
        form = CartAddProductForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            cart.add(product=product, quantity=cd['quantity'], update_quantity=cd['update'])
        return redirect('cart_detail')


class CartUpdateView(View):
    """Обновление quantity товара в корзине"""
    def post(self, request, pk):
        cart = Cart(request)
        product = get_object_or_404(Product, id=pk)
        form = CartAddProductForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            cart.add(product=product, quantity=cd['quantity'], update_quantity=True)
        return redirect('cart_detail')



def cart_remove(request, product_id):
    """Удаление товара из корзины"""
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart_detail')


def cart_remove_all(request):
    """Очистка всех товаров из корзины"""
    cart = Cart(request)
    cart.remove_all()
    return redirect('cart_detail')


class CartDetailView(TemplateView):
    """Страница корзины"""
    template_name = 'cart/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = Cart(self.request)
        context['cart'] = cart
        context['cart_product_form'] = CartAddProductForm()
        return context
