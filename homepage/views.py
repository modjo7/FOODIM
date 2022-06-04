from re import template
from django.contrib.auth import logout as auth_logout, get_user_model
from django.shortcuts import render
from django.views.generic import View, TemplateView
from inventory.models import Stock
from community.models import SaleArticle, PurchaseArticle

from django.contrib.auth import logout as auth_logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.shortcuts import render, redirect, get_object_or_404

from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect

from django.urls import reverse_lazy
from django.views import generic

from .forms import CustomUserCreationForm


class HomeView(View):
    template_name = "home.html"

    def get(self, request):
        labels = []
        data = []
        stockqueryset = Stock.objects.filter(
            is_deleted=False).order_by('-quantity')
        for item in stockqueryset:
            labels.append(item.name)
            data.append(item.quantity)
        sales = SaleArticle.objects.order_by('-time')[:3]
        purchases = PurchaseArticle.objects.order_by('-time')[:3]
        context = {
            'labels': labels,
            'data': data,
            'sales': sales,
            'purchases': purchases
        }
        return render(request, self.template_name, context)


class HelpView(TemplateView):
    template_name = "help.html"


class SignUpView(TemplateView):
    template_name = "signup.html"
    #template_name = "home2.html"


class SignUp(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'


class UserDeactivation(View):
    template_name = 'deactivate.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        user_pk = request.user.pk
        auth_logout(request)
        User = get_user_model()
        User.objects.filter(pk=user_pk).update(is_active=False)

        return redirect('home')
        # return render(request, self.template_name)


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(
                request, 'Your password was successfully updated!')
            return redirect('home')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {
        'form': form
    })
