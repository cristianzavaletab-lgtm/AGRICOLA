from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Category

@login_required
def category_list(request):
    categories = Category.objects.all().order_by('name')
    return render(request, 'inventory/category_list.html', {'categories': categories})

@login_required
def category_add(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        if name:
            Category.objects.create(name=name)
            messages.success(request, f'Categoría "{name}" creada exitosamente')
            return redirect('category_list')
        else:
            messages.error(request, 'El nombre es requerido')
    return render(request, 'inventory/category_form.html')

@login_required
def category_edit(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        if name:
            category.name = name
            category.save()
            messages.success(request, f'Categoría actualizada exitosamente')
            return redirect('category_list')
        else:
            messages.error(request, 'El nombre es requerido')
    return render(request, 'inventory/category_form.html', {'category': category})

@login_required
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category_name = category.name
        category.delete()
        messages.success(request, f'Categoría "{category_name}" eliminada')
        return redirect('category_list')
    return render(request, 'inventory/category_confirm_delete.html', {'category': category})
