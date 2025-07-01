# views.py
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Product
from .forms import ProductForm
from django.contrib.auth import login, logout
from django.contrib import messages

class ProductListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'main/home.html'
    context_object_name = 'products'

    def get_queryset(self):
        return Product.objects.filter(user=self.request.user)

class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'main/product_form.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'main/product_form.html'
    success_url = reverse_lazy('home')

    def get_queryset(self):
        return Product.objects.filter(user=self.request.user)

class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = 'main/product_confirm_delete.html'
    success_url = reverse_lazy('home')

    def get_queryset(self):
        return Product.objects.filter(user=self.request.user)



class LoginView(FormView):
    template_name = 'main/login.html'
    form_class = AuthenticationForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        messages.success(self.request, 'Вы успешно вошли в систему!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Ошибка входа. Неверный логин или пароль.')
        return super().form_invalid(form)

class LogoutView(View):
    def get(self, request):
        logout(request)
        messages.info(request, 'Вы вышли из системы.')
        return redirect('login')