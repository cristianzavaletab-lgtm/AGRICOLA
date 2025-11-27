from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import inlineformset_factory
from django.db import transaction
from django.urls import reverse_lazy
from .models import Purchase, PurchaseDetail, Product
from .forms import PurchaseForm, PurchaseDetailForm

class PurchaseListView(LoginRequiredMixin, ListView):
    model = Purchase
    template_name = 'inventory/purchase_list.html'
    context_object_name = 'purchases'
    ordering = ['-date']
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        qs = context['purchases']
        context['total_sum'] = sum(p.total for p in qs)
        return context

class PurchaseCreateView(LoginRequiredMixin, CreateView):
    model = Purchase
    form_class = PurchaseForm
    template_name = 'inventory/purchase_form.html'
    success_url = reverse_lazy('purchase_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        PurchaseDetailFormSet = inlineformset_factory(
            Purchase, PurchaseDetail, form=PurchaseDetailForm,
            extra=1, can_delete=True
        )
        if self.request.POST:
            context['details'] = PurchaseDetailFormSet(self.request.POST)
        else:
            context['details'] = PurchaseDetailFormSet()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        details = context['details']
        
        with transaction.atomic():
            self.object = form.save()
            if details.is_valid():
                details.instance = self.object
                saved_details = details.save()
                
                # Update Stock
                total_purchase = 0
                for detail in saved_details:
                    product = detail.product
                    product.stock += detail.quantity
                    # Optionally update buy price
                    product.price_buy = detail.price_unit
                    product.save()
                    total_purchase += detail.quantity * detail.price_unit
                
                self.object.total = total_purchase
                self.object.save()
            else:
                return self.render_to_response(self.get_context_data(form=form))
                
        return redirect(self.success_url)
