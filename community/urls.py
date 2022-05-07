from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('items/', views.ItemListView.as_view(), name='items-list'),
    path('items/new', views.ItemCreateView.as_view(), name='new-item'),
    path('items/<pk>/edit', views.ItemUpdateView.as_view(), name='edit-item'),
    path('items/<pk>/delete', views.ItemDeleteView.as_view(), name='delete-item'),
    path('items/<name>', views.ItemView.as_view(), name='item'),

    path('purchases/', views.PurchaseView.as_view(), name='purchases-list'), 
    path('purchases/new', views.SelectItemView.as_view(), name='select-item'), 
    path('purchases/new/<pk>', views.PurchaseCreateView.as_view(), name='new-purchase'),    
    path('purchases/<pk>/delete', views.PurchaseDeleteView.as_view(), name='delete-purchase'),
    
    path('sales/', views.SaleView.as_view(), name='sales-list'),
    path('sales/new', views.SaleCreateView.as_view(), name='new-sale'),
    path('sales/<pk>/delete', views.SaleDeleteView.as_view(), name='delete-sale'),

    path("purchases/<articleno>", views.PurchaseArticleView.as_view(), name="purchase-article"),
    path("sales/<articleno>", views.SaleArticleView.as_view(), name="sale-article"),
    path('board/', views.BoardView.as_view(), name='board')
]