from re import template
from django.contrib.auth import logout as auth_logout, get_user_model
from django.shortcuts import render
from django.views.generic import View, TemplateView
from inventory.models import Stock
from community.models import SaleArticle, PurchaseArticle

from django.urls import reverse_lazy
from django.views import generic
import datetime

from .forms import CustomUserCreationForm

from django.contrib.auth import logout as auth_logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.shortcuts import render, redirect, get_object_or_404

from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
class HomeView(View):
    template_name = "home.html"

    def get(self, request):        
        labels = []
        data = []
        timeleft = []
        timeleft_user = []

        dt_now = datetime.date.today()

        stockqueryset = Stock.objects.filter(is_deleted=False).order_by('-quantity')

        for item in stockqueryset:
            v = str(item.expdate - dt_now).split()
            item.timeleft = int(v[0])

            labels.append(item.name)
            data.append(item.quantity)
            if (item.timeleft <= 2 and item.timeleft >= 0): # if timeleft 0,1,2, the notice will be added.
                timeleft.append(item.name + " : " + str(item.timeleft) + " days left")
                timeleft_user.append(item.username)

        sales = SaleArticle.objects.order_by('-time')[:3]
        purchases = PurchaseArticle.objects.order_by('-time')[:3]

        context = {
            'labels'    : labels,
            'data'      : data,
            'timeleft'  : timeleft,
            'timeleft_user': timeleft_user,
            'sales'     : sales,
            'purchases' : purchases
        }
        return render(request, self.template_name, context)

class HelpView(TemplateView):
    template_name = "help.html"

class SignUpView(TemplateView):
    template_name = "signup.html"

class SignUp(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = "signup.html"

class UserDeactivation(View):
    template_name = 'withdrawal.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        user_pk = request.user.pk
        auth_logout(request)
        User = get_user_model()
        User.objects.filter(pk=user_pk).update(is_active=False)

        return redirect('home')

def ChangePassword(request):
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
