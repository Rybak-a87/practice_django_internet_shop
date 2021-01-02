from django.shortcuts import render
from django.views.generic import DetailView, View

from .models import Notebook, Smartphone, Category, LatestProducts, Customer, Cart
from .mixins import CategoryDetailMixin     # должет первый по порядку наследоватся


# def test_base(request):
#     categories = Category.objects.get_categories_for_left_sidebar()    # для истользования объекта в шаблоне
#     return render(request, "base/base.html", {"categories": categories})


class BaseView(View):
    def get(self, request, *args, **kwargs):    # метод - аналог функции test_base
        categories = Category.objects.get_categories_for_left_sidebar()   # для истользования объекта в шаблоне
        products = LatestProducts.objects.get_products_for_main_page(    # для вывода продусков на главной странице
            "notebook", "smartphone", with_respect_to="notebook"
        )
        context = {
            "categories": categories,
            "products": products,
        }
        return render(request, "base/base.html", context)


class ProductDetailView(CategoryDetailMixin, DetailView):
    CT_MODEL_MODEL_CLASS = {
        "notebook": Notebook,
        "smartphone": Smartphone,
    }

    def dispatch(self, request, *args, **kwargs):
        self.model = self.CT_MODEL_MODEL_CLASS[kwargs["ct_model"]]
        self.queryset = self.model._base_manager.all()
        return super().dispatch(request, *args, **kwargs)

    context_object_name = "product"
    template_name = "mainapp/product_detail.html"
    slug_url_kwarg = "slug"


class CategoryDetailView(CategoryDetailMixin, DetailView):
    model = Category
    queryset = Category.objects.all()
    context_object_name = "category"
    template_name = "mainapp/category_detail.html"
    slug_url_kwarg = "slug"


class CartView(View):
    def get(self, request, *args, **kwargs):
        customer = Customer.objects.get(user=request.user)
        cart = Cart.objects.get(owner=customer)
        categories = Category.objects.get_categories_for_left_sidebar()
        context = {
            "cart": cart,
            "categories": categories,
        }
        return render(request, "mainapp/cart.html", context)
