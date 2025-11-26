from django.urls import path
from . import views
from .views_pdf import invoice_pdf

urlpatterns = [
    path('pos/', views.pos_view, name='pos'),
    path('checkout/', views.checkout, name='checkout'),
    path('invoice/<int:sale_id>/pdf/', invoice_pdf, name='invoice_pdf'),
]
