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

from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import (
    View,
    ListView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import ConsumedData

from .forms import ConsumedDataForm

class HomeView(View):
    template_name = "home.html"

    def get(self, request):        
        labels = []
        data = []
        timeleft = []
        timeleft_user = []
        nutrition_recommended = []
        nutrition_labels = ['Protein', 'Fat', 'Carbohydrate']

        dt_now = datetime.date.today()

        stockqueryset = Stock.objects.filter(is_deleted=False).order_by('timeleft')

        for item in stockqueryset:
            if (request.user.username == item.username):

                x = (item.expdate - dt_now).total_seconds()
                x = x/(60*60*24)
                item.timeleft = int(x)
                item.save()

                labels.append(item.name)
                data.append(item.quantity)

                if (item.timeleft <= 3 and item.timeleft >= 0):
                    timeleft.append(item.name + " : " + str(item.timeleft) + " days left")
                    timeleft_user.append(item.username)

        sales = SaleArticle.objects.order_by('-time')[:3]
        purchases = PurchaseArticle.objects.order_by('-time')[:3]

        context = {
            'labels'    : labels,
            'data'      : data,
            'timeleft'  : timeleft,
            'timeleft_user': timeleft_user,
            'nutrition_recommended': nutrition_recommended,
            'nutrition_labels': nutrition_labels,
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

class NutritionView(View):
    template_name = "nutrition.html"

    def get(self, request):

        nutrition_recommended = []
        nutrition_consumed = []
        nutrition_labels = ['Protein', 'Fat', 'Carbohydrate', 'Vitamin']

        dt_now = datetime.date.today()

        y = (dt_now - request.user.signupday).total_seconds()
        y = y / (60 * 60 * 24)
        y = y + 1

        a = 100 * y
        b = 80 * y
        c = 60 * y
        d = 20 * y

        queryset = ConsumedData.objects.filter(username=request.user.username)

        for item in queryset:
            e = item.protein
            f = item.fat
            g = item.carbohydrate
            h = item.vitamin

        nutrition_recommended.append(a)
        nutrition_recommended.append(b)
        nutrition_recommended.append(c)
        nutrition_recommended.append(d)

        nutrition_consumed.append(e)
        nutrition_consumed.append(f)
        nutrition_consumed.append(g)
        nutrition_consumed.append(h)

        context = {
            'nutrition_recommended': nutrition_recommended,
            'nutrition_consumed': nutrition_consumed,
            'nutrition_labels': nutrition_labels,
        }
        return render(request, self.template_name, context)



class ConsumedDataCreateView(SuccessMessageMixin, CreateView):
    model = ConsumedData
    form_class = ConsumedDataForm
    success_url = '/nutrition'
    success_message = "Nutrition information been modified successfully"
    template_name = "edit_nutrition.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Nutrition User information'
        context["savebtn"] = 'Continue'
        return context
