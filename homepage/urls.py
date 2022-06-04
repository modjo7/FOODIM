from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('help/', views.HelpView.as_view(), name='help'),
    path('signup/', views.SignUp .as_view(), name='signup'),
    path('deactivate/', views.UserDeactivation.as_view(), name='deactivate'),
    url(r'^password/$', views.change_password, name='change_password'),
]
