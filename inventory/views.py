from urllib import request
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import (
    View,
    CreateView,
    UpdateView
)
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from .models import Stock
from .forms import StockForm
from django_filters.views import FilterView
from .filters import StockFilter

import datetime
import logging


class StockListView(FilterView):
    filterset_class = StockFilter
    queryset = Stock.objects.filter(is_deleted=False)
    template_name = 'inventory.html'
    paginate_by = 10

    # DEV : to be modified
    # temp will be expdate. ( I failed to bring expdate data here due to DeferredAttribute error )

    # Current date
    dt_now = datetime.datetime.now()  # almost same : dt_today = datetime.date.today()

    # test : failed (DeferredAttribute error, I don't know why). expdate is also the same.
    #temp1 = Stock.expdate2
    #timeleft_temp1 = datetime.datetime.strptime(temp1, '%Y-%m-%d') - dt_now

    # Fixed date string (temp) : success
    temp = "2022-12-30"
    timeleft_temp = datetime.datetime.strptime(temp, '%Y-%m-%d') - dt_now
    Stock.timeleft = timeleft_temp.days

    # END


# createview class to add new stock, mixin used to display message


class StockCreateView(SuccessMessageMixin, CreateView):
    model = Stock
    # setting 'Stock' model as model

    # setting 'StockForm' form as form
    form_class = StockForm
    # 'edit_stock.html' used as the template
    template_name = "edit_stock.html"
    # redirects to 'inventory' page in the url after submitting the form
    success_url = '/inventory'
    # displays message when form is submitted
    success_message = "Stock has been created successfully"

    # used to send additional context
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'New Stock'
        context["savebtn"] = 'Add to Inventory'
        return context


# updateview class to edit stock, mixin used to display message
class StockUpdateView(SuccessMessageMixin, UpdateView):
    # setting 'Stock' model as model
    model = Stock
    # setting 'StockForm' form as form
    form_class = StockForm
    # 'edit_stock.html' used as the template
    template_name = "edit_stock.html"
    # redirects to 'inventory' page in the url after submitting the form
    success_url = '/inventory'
    # displays message when form is submitted
    success_message = "Stock has been updated successfully"

    # used to send additional context
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Edit Stock'
        context["savebtn"] = 'Update Stock'
        context["delbtn"] = 'Delete Stock'
        return context


# view class to delete stock
class StockDeleteView(View):
    # 'delete_stock.html' used as the template
    template_name = "delete_stock.html"
    # displays message when form is submitted
    success_message = "Stock has been deleted successfully"

    def get(self, request, pk):
        stock = get_object_or_404(Stock, pk=pk)
        return render(request, self.template_name, {'object': stock})

    def post(self, request, pk):
        stock = get_object_or_404(Stock, pk=pk)
        stock.is_deleted = True
        stock.save()
        messages.success(request, self.success_message)
        return redirect('inventory')


class NutritionView(View):
    template_name = "nutrition.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        return render(request, self.template_name)
