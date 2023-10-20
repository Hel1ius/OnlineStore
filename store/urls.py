from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('category/<str:name>', views.ProductInCategory.as_view(), name='product_category'),
    path('filter/', views.FilterProductView.as_view(), name='filter'),
    path('shop/', views.ProductsView.as_view(), name='shop'),
    path('product/<slug:slug>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('review/<int:pk>', views.AddReview.as_view(), name='add_review'),
]
