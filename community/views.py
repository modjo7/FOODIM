from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import (
    View, 
    ListView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import (
    PurchaseArticle, 
    Item, 
    PurchaseItem,
    PurchaseArticleDetails,
    SaleArticle,  
    SaleItem,
    SaleArticleDetails
)
from .forms import (
    SelectItemForm, 
    PurchaseItemFormset,
    PurchaseDetailsForm, 
    ItemForm, 
    SaleForm,
    SaleItemFormset,
    SaleDetailsForm
)
from inventory.models import Stock




# shows a lists of all items
class ItemListView(ListView):
    model = Item
    template_name = "items/items_list.html"
    queryset = Item.objects.filter(is_deleted=False)
    paginate_by = 10


# used to add a new item
class ItemCreateView(SuccessMessageMixin, CreateView):
    model = Item
    form_class = ItemForm
    success_url = '/community/items'
    success_message = "Item has been created successfully"
    template_name = "items/edit_item.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'New Item'
        context["savebtn"] = 'Add Item'
        return context     


# used to update a item's info
class ItemUpdateView(SuccessMessageMixin, UpdateView):
    model = Item
    form_class = ItemForm
    success_url = '/community/items'
    success_message = "Item details has been updated successfully"
    template_name = "items/edit_item.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Edit Item'
        context["savebtn"] = 'Save Changes'
        context["delbtn"] = 'Delete Item'
        return context


# used to delete a item
class ItemDeleteView(View):
    template_name = "items/delete_item.html"
    success_message = "Item has been deleted successfully"

    def get(self, request, pk):
        item = get_object_or_404(Item, pk=pk)
        return render(request, self.template_name, {'object' : item})

    def post(self, request, pk):  
        item = get_object_or_404(Item, pk=pk)
        item.is_deleted = True
        item.save()                                               
        messages.success(request, self.success_message)
        return redirect('items-list')


# used to view a item's profile
class ItemView(View):
    def get(self, request, name):
        itemobj = get_object_or_404(Item, name=name)
        article_list = PurchaseArticle.objects.filter(item=itemobj)
        page = request.GET.get('page', 1)
        paginator = Paginator(article_list, 10)
        try:
            articles = paginator.page(page)
        except PageNotAnInteger:
            articles = paginator.page(1)
        except EmptyPage:
            articles = paginator.page(paginator.num_pages)
        context = {
            'item'  : itemobj,
            'articles'     : articles
        }
        return render(request, 'items/item.html', context)




# shows the list of articles of all purchases 
class PurchaseView(ListView):
    model = PurchaseArticle
    template_name = "purchases/purchases_list.html"
    context_object_name = 'articles'
    ordering = ['-time']
    paginate_by = 10


# used to select the item
class SelectItemView(View):
    form_class = SelectItemForm
    template_name = 'purchases/select_item.html'

    def get(self, request, *args, **kwargs):                                    # loads the form page
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):                                   # gets selected item and redirects to 'PurchaseCreateView' class
        form = self.form_class(request.POST)
        if form.is_valid():
            itemid = request.POST.get("item")
            item = get_object_or_404(Item, id=itemid)
            return redirect('new-purchase', item.pk)
        return render(request, self.template_name, {'form': form})


# used to generate a article object and save items
class PurchaseCreateView(View):                                                 
    template_name = 'purchases/new_purchase.html'

    def get(self, request, pk):
        formset = PurchaseItemFormset(request.GET or None)                      # renders an empty formset
        itemobj = get_object_or_404(Item, pk=pk)                        # gets the item object
        context = {
            'formset'   : formset,
            'item'  : itemobj,
        }                                                                       # sends the item and formset as context
        return render(request, self.template_name, context)

    def post(self, request, pk):
        formset = PurchaseItemFormset(request.POST)                             # recieves a post method for the formset
        itemobj = get_object_or_404(Item, pk=pk)                        # gets the item object
        if formset.is_valid():
            # saves article
            articleobj = PurchaseArticle(item=itemobj)                        # a new object of class 'PurchaseArticle' is created with item field set to 'itemobj'
            articleobj.save()                                                      # saves object into the db
            # create article details object
            articledetailsobj = PurchaseArticleDetails(articleno=articleobj)
            articledetailsobj.save()
            for form in formset:                                                # for loop to save each individual form as its own object
                # false saves the item and links article to the item
                articleitem = form.save(commit=False)
                articleitem.articleno = articleobj                                       # links the article object to the items
                # gets the stock item
                stock = get_object_or_404(Stock, name=articleitem.stock.name)       # gets the item
                # calculates the total price
                articleitem.totalprice = articleitem.perprice * articleitem.quantity
                # updates quantity in stock db
                stock.quantity += articleitem.quantity                              # updates quantity
                # saves article item and stock
                stock.save()
                articleitem.save()
            messages.success(request, "Purchased items have been registered successfully")
            return redirect('purchase-article', articleno=articleobj.articleno)
        formset = PurchaseItemFormset(request.GET or None)
        context = {
            'formset'   : formset,
            'item'  : itemobj
        }
        return render(request, self.template_name, context)


# used to delete a article object
class PurchaseDeleteView(SuccessMessageMixin, DeleteView):
    model = PurchaseArticle
    template_name = "purchases/delete_purchase.html"
    success_url = '/community/purchases'
    
    def delete(self, *args, **kwargs):
        self.object = self.get_object()
        items = PurchaseItem.objects.filter(articleno=self.object.articleno)
        for item in items:
            stock = get_object_or_404(Stock, name=item.stock.name)
            if stock.is_deleted == False:
                stock.quantity -= item.quantity
                stock.save()
        messages.success(self.request, "Purchase article has been deleted successfully")
        return super(PurchaseDeleteView, self).delete(*args, **kwargs)




# shows the list of articles of all sales 
class SaleView(ListView):
    model = SaleArticle
    template_name = "sales/sales_list.html"
    context_object_name = 'articles'
    ordering = ['-time']
    paginate_by = 10


# used to generate a article object and save items
class SaleCreateView(View):                                                      
    template_name = 'sales/new_sale.html'

    def get(self, request):
        form = SaleForm(request.GET or None)
        formset = SaleItemFormset(request.GET or None)                          # renders an empty formset
        stocks = Stock.objects.filter(is_deleted=False)
        context = {
            'form'      : form,
            'formset'   : formset,
            'stocks'    : stocks
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = SaleForm(request.POST)
        formset = SaleItemFormset(request.POST)                                 # recieves a post method for the formset
        if form.is_valid() and formset.is_valid():
            # saves article
            articleobj = form.save(commit=False)
            articleobj.save()     
            # create article details object
            articledetailsobj = SaleArticleDetails(articleno=articleobj)
            articledetailsobj.save()
            for form in formset:                                                # for loop to save each individual form as its own object
                # false saves the item and links article to the item
                articleitem = form.save(commit=False)
                articleitem.articleno = articleobj                                       # links the article object to the items
                # gets the stock item
                stock = get_object_or_404(Stock, name=articleitem.stock.name)      
                # calculates the total price
                articleitem.totalprice = articleitem.perprice * articleitem.quantity
                # updates quantity in stock db
                stock.quantity -= articleitem.quantity   
                # saves article item and stock
                stock.save()
                articleitem.save()
            messages.success(request, "Sold items have been registered successfully")
            return redirect('sale-article', articleno=articleobj.articleno)
        form = SaleForm(request.GET or None)
        formset = SaleItemFormset(request.GET or None)
        context = {
            'form'      : form,
            'formset'   : formset,
        }
        return render(request, self.template_name, context)


# used to delete a article object
class SaleDeleteView(SuccessMessageMixin, DeleteView):
    model = SaleArticle
    template_name = "sales/delete_sale.html"
    success_url = '/community/sales'
    
    def delete(self, *args, **kwargs):
        self.object = self.get_object()
        items = SaleItem.objects.filter(articleno=self.object.articleno)
        for item in items:
            stock = get_object_or_404(Stock, name=item.stock.name)
            if stock.is_deleted == False:
                stock.quantity += item.quantity
                stock.save()
        messages.success(self.request, "Sale article has been deleted successfully")
        return super(SaleDeleteView, self).delete(*args, **kwargs)




# used to display the purchase article object
class PurchaseArticleView(View):
    model = PurchaseArticle
    template_name = "article/purchase_article.html"
    article_base = "article/article_base.html"

    def get(self, request, articleno):
        context = {
            'article'          : PurchaseArticle.objects.get(articleno=articleno),
            'items'         : PurchaseItem.objects.filter(articleno=articleno),
            'articledetails'   : PurchaseArticleDetails.objects.get(articleno=articleno),
            'article_base'     : self.article_base,
        }
        return render(request, self.template_name, context)

    def post(self, request, articleno):
        form = PurchaseDetailsForm(request.POST)
        if form.is_valid():
            articledetailsobj = PurchaseArticleDetails.objects.get(articleno=articleno)

            articledetailsobj.title = request.POST.get("title")
            articledetailsobj.comment = request.POST.get("comment")
            articledetailsobj.contact = request.POST.get("contact")
            articledetailsobj.address = request.POST.get("address")
            articledetailsobj.save()

            messages.success(request, "Article details have been modified successfully")
        context = {
            'article'          : PurchaseArticle.objects.get(articleno=articleno),
            'items'         : PurchaseItem.objects.filter(articleno=articleno),
            'articledetails'   : PurchaseArticleDetails.objects.get(articleno=articleno),
            'article_base'     : self.article_base,
        }
        return render(request, self.template_name, context)


# used to display the sale article object
class SaleArticleView(View):
    model = SaleArticle
    template_name = "article/sale_article.html"
    article_base = "article/article_base.html"
    
    def get(self, request, articleno):
        context = {
            'article'          : SaleArticle.objects.get(articleno=articleno),
            'items'         : SaleItem.objects.filter(articleno=articleno),
            'articledetails'   : SaleArticleDetails.objects.get(articleno=articleno),
            'article_base'     : self.article_base,
        }
        return render(request, self.template_name, context)

    def post(self, request, articleno):
        form = SaleDetailsForm(request.POST)
        if form.is_valid():
            articledetailsobj = SaleArticleDetails.objects.get(articleno=articleno)

            articledetailsobj.address = request.POST.get("address")
            articledetailsobj.save()

            messages.success(request, "Article details have been modified successfully")
        context = {
            'article'          : SaleArticle.objects.get(articleno=articleno),
            'items'         : SaleItem.objects.filter(articleno=articleno),
            'articledetails'   : SaleArticleDetails.objects.get(articleno=articleno),
            'article_base'     : self.article_base,
        }
        return render(request, self.template_name, context)


class BoardView(View):
    template_name = "board/board.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        return render(request, self.template_name)
