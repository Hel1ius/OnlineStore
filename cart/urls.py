from django.urls import path

from . import views


urlpatterns = [
    path('', views.CartDetailView.as_view(), name='cart_detail'),
    path('add/<int:pk>', views.CartAddView.as_view(), name='cart_add'),
    path('update/<int:pk>', views.CartUpdateView.as_view(), name='cart_update'),
    path('remove/<int:product_id>', views.cart_remove, name='cart_remove'),
    path('remove_all', views.cart_remove_all, name='cart_remove_all'),
]