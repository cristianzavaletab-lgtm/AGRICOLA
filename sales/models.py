from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from inventory.models import Product

class Client(models.Model):
    name = models.CharField(max_length=200, verbose_name="Nombre Completo")
    dni = models.CharField(max_length=20, blank=True, verbose_name="DNI/RUC")
    phone = models.CharField(max_length=20, blank=True, verbose_name="Teléfono")
    address = models.TextField(blank=True, verbose_name="Dirección")
    is_frequent = models.BooleanField(default=False, verbose_name="Cliente Frecuente")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"

    def __str__(self):
        return self.name

class Sale(models.Model):
    PAYMENT_METHODS = [
        ('CASH', 'Efectivo'),
        ('CARD', 'Tarjeta'),
        ('CREDIT', 'Crédito'),
        ('YAPE', 'Yape/Plin'),
    ]

    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Cliente")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="Vendedor")
    date = models.DateTimeField(default=timezone.now, verbose_name="Fecha")
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Total")
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHODS, default='CASH', verbose_name="Método de Pago")
    is_paid = models.BooleanField(default=True, verbose_name="Pagado")
    
    class Meta:
        verbose_name = "Venta"
        verbose_name_plural = "Ventas"

    def __str__(self):
        return f"Venta #{self.id} - {self.date.strftime('%d/%m/%Y')}"

class SaleDetail(models.Model):
    sale = models.ForeignKey(Sale, related_name='details', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, verbose_name="Producto")
    quantity = models.IntegerField(verbose_name="Cantidad")
    price_unit = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio Unitario")
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Subtotal")

    def save(self, *args, **kwargs):
        if not self.subtotal:
            self.subtotal = self.quantity * self.price_unit
        super().save(*args, **kwargs)

class Payment(models.Model):
    sale = models.ForeignKey(Sale, related_name='payments', on_delete=models.CASCADE, verbose_name="Venta")
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Monto Pagado")
    date = models.DateTimeField(default=timezone.now, verbose_name="Fecha de Pago")
    note = models.CharField(max_length=200, blank=True, verbose_name="Nota")

    class Meta:
        verbose_name = "Pago"
        verbose_name_plural = "Pagos"
