from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib import messages
from inventory.models import Product
from .cart import Cart
from .models import Sale, SaleDetail, Client

@login_required
def pos_view(request):
    products = Product.objects.all().select_related('category')
    show_out = request.GET.get('show_out') == '1'
    q = request.GET.get('q')
    if q:
        products = products.filter(name__icontains=q)
    if not show_out:
        products = products.filter(stock__gt=0)
    
    return render(request, 'sales/pos.html', {'products': products, 'show_out': show_out})

@login_required
@require_POST
def checkout(request):
    product_id = request.POST.get('product_id')
    quantity = int(request.POST.get('quantity', 1))
    client_name = request.POST.get('client_name', '').strip()
    client_dni = request.POST.get('client_dni', '').strip()
    client_phone = request.POST.get('client_phone', '').strip()
    
    if not all([product_id, quantity, client_name, client_dni]):
        messages.error(request, 'Todos los campos son requeridos')
        return redirect('pos')
    
    try:
        product = get_object_or_404(Product, id=product_id)
        
        # Verify stock
        if product.stock < quantity:
            messages.error(request, f'Stock insuficiente. Disponible: {product.stock}')
            return redirect('pos')
        
        # Get or create client
        client, created = Client.objects.get_or_create(
            dni=client_dni,
            defaults={
                'name': client_name,
                'phone': client_phone
            }
        )
        
        # If client exists, update info
        if not created:
            client.name = client_name
            if client_phone:
                client.phone = client_phone
            client.save()
        
        # Calculate total
        total = product.price_sell * quantity
        
        # Create sale
        sale = Sale.objects.create(
            user=request.user,
            client=client,
            total=total
        )
        
        # Create sale detail
        SaleDetail.objects.create(
            sale=sale,
            product=product,
            quantity=quantity,
            price_unit=product.price_sell,
            subtotal=total
        )
        
        # Update stock
        product.stock -= quantity
        product.save()
        
        messages.success(request, f'¡Venta Registrada! Total: S/ {total:.2f}')
        
        # Redirect to invoice
        return redirect('invoice_pdf', sale_id=sale.id)
        
    except Exception as e:
        messages.error(request, f'Error al procesar la venta: {str(e)}')
        return redirect('pos')

