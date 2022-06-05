from django.urls import path, re_path
from django.conf.urls import url
from django.conf import Settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.StockListView.as_view(), name='inventory'),
    path('new', views.StockCreateView.as_view(), name='new-stock'),
    path('stock/<pk>/edit', views.StockUpdateView.as_view(), name='edit-stock'),
    path('stock/<pk>/delete', views.StockDeleteView.as_view(), name='delete-stock'),

    path('nutrition/', views.NutritionView.as_view(), name='nutrition')
]