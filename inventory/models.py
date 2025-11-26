from django.db import models
from django.utils import timezone

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Nombre")
    description = models.TextField(blank=True, verbose_name="Descripción")

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"

    def __str__(self):
        return self.name

class Supplier(models.Model):
    name = models.CharField(max_length=200, verbose_name="Nombre/Empresa")
    phone = models.CharField(max_length=20, blank=True, verbose_name="Teléfono")
    email = models.EmailField(blank=True, verbose_name="Email")
    address = models.TextField(blank=True, verbose_name="Dirección")

    class Meta:
        verbose_name = "Proveedor"
        verbose_name_plural = "Proveedores"

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name="Nombre del Producto")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, verbose_name="Categoría")
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, verbose_name="Proveedor Principal")
    price_buy = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio Compra")
    price_sell = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio Venta")
    stock = models.IntegerField(default=0, verbose_name="Stock Actual")
    stock_min = models.IntegerField(default=5, verbose_name="Stock Mínimo")
    image = models.ImageField(upload_to='products/', blank=True, null=True, verbose_name="Imagen")
    expiration_date = models.DateField(blank=True, null=True, verbose_name="Fecha Vencimiento")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"

    def __str__(self):
        return self.name
    
    @property
    def is_low_stock(self):
        return self.stock <= self.stock_min

class Purchase(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, verbose_name="Proveedor")
    date = models.DateTimeField(default=timezone.now, verbose_name="Fecha de Compra")
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Total")
    note = models.TextField(blank=True, verbose_name="Nota")

    class Meta:
        verbose_name = "Compra"
        verbose_name_plural = "Compras"

    def __str__(self):
        return f"Compra #{self.id} - {self.supplier.name}"

class PurchaseDetail(models.Model):
    purchase = models.ForeignKey(Purchase, related_name='details', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Producto")
    quantity = models.IntegerField(verbose_name="Cantidad")
    price_unit = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio Unitario")
    
    def save(self, *args, **kwargs):
        # Update product stock on save? 
        # Better to handle this in a service or signal to avoid double counting on edits.
        # For simplicity in this MVP, we might do it in views or signals.
        super().save(*args, **kwargs)
