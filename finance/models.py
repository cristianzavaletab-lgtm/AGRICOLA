from django.db import models
from django.utils import timezone

class Expense(models.Model):
    CATEGORIES = [
        ('LUZ', 'Luz'),
        ('AGUA', 'Agua'),
        ('ALQUILER', 'Alquiler'),
        ('TRANSPORTE', 'Transporte'),
        ('PERSONAL', 'Personal'),
        ('OTROS', 'Otros'),
    ]

    description = models.CharField(max_length=255, verbose_name="Descripción")
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Monto")
    date = models.DateField(default=timezone.now, verbose_name="Fecha")
    category = models.CharField(max_length=20, choices=CATEGORIES, default='OTROS', verbose_name="Categoría")
    
    class Meta:
        verbose_name = "Gasto"
        verbose_name_plural = "Gastos"

    def __str__(self):
        return f"{self.get_category_display()} - {self.amount}"
