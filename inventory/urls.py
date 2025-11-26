from django.urls import path
from .views import (
    ProductListView, ProductCreateView, ProductUpdateView, ProductDeleteView,
    SupplierListView, SupplierCreateView, SupplierUpdateView
)
from .views_purchase import PurchaseListView, PurchaseCreateView
from .views_category import category_list, category_add, category_edit, category_delete

urlpatterns = [
    # Products
    path('products/', ProductListView.as_view(), name='product_list'),
    path('products/add/', ProductCreateView.as_view(), name='product_add'),
    path('products/<int:pk>/edit/', ProductUpdateView.as_view(), name='product_edit'),
    path('products/<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),
    
    # Categories
    path('categories/', category_list, name='category_list'),
    path('categories/add/', category_add, name='category_add'),
    path('categories/<int:pk>/edit/', category_edit, name='category_edit'),
    path('categories/<int:pk>/delete/', category_delete, name='category_delete'),
    
    # Suppliers
    path('suppliers/', SupplierListView.as_view(), name='supplier_list'),
    path('suppliers/add/', SupplierCreateView.as_view(), name='supplier_add'),
    path('suppliers/<int:pk>/edit/', SupplierUpdateView.as_view(), name='supplier_edit'),

    # Purchases
    path('purchases/', PurchaseListView.as_view(), name='purchase_list'),
    path('purchases/add/', PurchaseCreateView.as_view(), name='purchase_add'),
]
