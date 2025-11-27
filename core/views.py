from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.urls import reverse_lazy

from django.db.models import Sum, F
from django.utils import timezone
from inventory.models import Product
from sales.models import Sale
from django.db import connection

class CustomLoginView(LoginView):
    template_name = 'core/login.html'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('dashboard')

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'core/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = timezone.now().date()
        
        # Sales Today
        sales_today = Sale.objects.filter(date__date=today).aggregate(Sum('total'))['total__sum'] or 0
        context['sales_today'] = sales_today
        
        # Product Count
        context['product_count'] = Product.objects.count()
        
        # Low Stock
        context['low_stock_count'] = Product.objects.filter(stock__lte=F('stock_min')).count()
        
        # Expiring Soon (next 30 days)
        next_30_days = today + timezone.timedelta(days=30)
        context['expiring_count'] = Product.objects.filter(
            expiration_date__isnull=False,
            expiration_date__lte=next_30_days,
            expiration_date__gte=today
        ).count()
        
        # Recent Sales
        context['recent_sales'] = Sale.objects.order_by('-date')[:5]

        return context

def healthz(request):
    check_db = request.GET.get('db')
    if check_db:
        try:
            with connection.cursor() as cursor:
                cursor.execute('SELECT 1')
                row = cursor.fetchone()
            return HttpResponse('OK DB')
        except Exception as e:
            return HttpResponse(f'DB ERROR: {str(e)}', status=500)
    return HttpResponse('OK')
