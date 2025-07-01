from django.shortcuts import render
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views import View
from django.views.generic import (
    ListView, CreateView, UpdateView, DeleteView, TemplateView
)
from django import forms


from django.db.models import Sum
from django.views.generic import ListView
from main.models import Product

#
class UserProductListView(View):
    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        products = Product.objects.filter(user=user)
        context = {
            'user': user,
            'products': products,
        }
        return render(request, 'custom_admin/user_application.html', context)


class AdminProductSummaryView(ListView):
    template_name = 'custom_admin/applications.html'
    context_object_name = 'summary'

    def get_queryset(self):
        return Product.objects.values('name').annotate(total_quantity=Sum('quantity')).order_by('name')

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'is_active', 'is_staff', 'is_superuser']


class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff

class UserListView(LoginRequiredMixin, StaffRequiredMixin, ListView):
    model = User
    template_name = 'custom_admin/user_list.html'
    context_object_name = 'users'

class UserCreateView(LoginRequiredMixin, StaffRequiredMixin, View):
    def get(self, request):
        return render(request, 'custom_admin/user_create.html', {'errors': []})

    def post(self, request):
        errors = []
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not username or not password:
            errors.append('Имя пользователя и пароль обязательны')
        elif User.objects.filter(username=username).exists():
            errors.append('Пользователь с таким логином уже существует')

        if not errors:
            User.objects.create_user(username=username, email=email, password=password)
            return redirect('custom_admin:user_list')

        return render(request, 'custom_admin/user_create.html', {'errors': errors})

class UserEditView(LoginRequiredMixin, StaffRequiredMixin, View):
    def get(self, request, user_id):
        user = get_object_or_404(User, pk=user_id)
        return render(request, 'custom_admin/user_edit.html', {'user_obj': user, 'errors': []})

    def post(self, request, user_id):
        user = get_object_or_404(User, pk=user_id)
        errors = []

        username = request.POST.get('username')
        email = request.POST.get('email')
        is_active = bool(request.POST.get('is_active'))
        is_staff = bool(request.POST.get('is_staff'))
        is_superuser = bool(request.POST.get('is_superuser'))

        if not username:
            errors.append("Имя пользователя обязательно")
        elif User.objects.exclude(pk=user.pk).filter(username=username).exists():
            errors.append("Пользователь с таким логином уже существует")

        if not errors:
            user.username = username
            user.email = email
            user.is_active = is_active
            user.is_staff = is_staff
            user.is_superuser = is_superuser
            user.save()
            return redirect('custom_admin:user_list')

        return render(request, 'custom_admin/user_edit.html', {
            'user_obj': user,
            'errors': errors
        })
class UserDeleteView(LoginRequiredMixin, StaffRequiredMixin, DeleteView):
    model = User
    template_name = 'custom_admin/user_confirm_delete.html'
    success_url = reverse_lazy('custom_admin:user_list')
    context_object_name = 'user_obj'

class DashboardView(LoginRequiredMixin, StaffRequiredMixin, TemplateView):
    template_name = 'custom_admin/dashboard.html'


class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('custom_admin:dashboard')
        return render(request, 'custom_admin/login.html', {'form': {}})

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_staff:
            login(request, user)
            return redirect('custom_admin:dashboard')

        return render(request, 'custom_admin/login.html', {'form': {'errors': True}})



class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        return redirect('custom_admin:login')