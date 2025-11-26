from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Expense
from django import forms

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = '__all__'
        widgets = {
            'description': forms.TextInput(attrs={'class': 'input-field'}),
            'amount': forms.NumberInput(attrs={'class': 'input-field'}),
            'date': forms.DateInput(attrs={'class': 'input-field', 'type': 'date'}),
            'category': forms.Select(attrs={'class': 'input-field'}),
        }

class ExpenseListView(LoginRequiredMixin, ListView):
    model = Expense
    template_name = 'finance/expense_list.html'
    context_object_name = 'expenses'
    ordering = ['-date']

class ExpenseCreateView(LoginRequiredMixin, CreateView):
    model = Expense
    form_class = ExpenseForm
    template_name = 'finance/expense_form.html'
    success_url = reverse_lazy('expense_list')

class ExpenseUpdateView(LoginRequiredMixin, UpdateView):
    model = Expense
    form_class = ExpenseForm
    template_name = 'finance/expense_form.html'
    success_url = reverse_lazy('expense_list')

class ExpenseDeleteView(LoginRequiredMixin, DeleteView):
    model = Expense
    template_name = 'finance/expense_confirm_delete.html'
    success_url = reverse_lazy('expense_list')
