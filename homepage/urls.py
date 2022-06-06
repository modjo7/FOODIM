from django.urls import path
from django.contrib.auth import views as auth_views

from django.conf.urls import url
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('help/', views.HelpView.as_view(), name='help'),
    path('signup/', views.SignUp .as_view(), name='signup'),
    path('withdrawal/', views.UserDeactivation.as_view(), name='withdrawal'),
    path('change_password/', views.ChangePassword, name='change_password'),
    path('nutrition/', views.NutritionView.as_view(), name='nutrition'),
    path('edit_nutrition/', views.ConsumedDataCreateView.as_view(), name='edit-nutrition'),
    #path('reset_password/', views.PasswordResetView.as_view(), name='reset_password'),

]
