from django.shortcuts import render
from django.contrib.contenttypes.models import ContentType
from django.contrib import messages    # выводит информацию о каких либо осуществленных действиях
from django.http import HttpResponseRedirect    # для перенаправления
from django.views.generic import DetailView, View

from .models import Notebook, Smartphone, Category, LatestProducts, Customer, Cart, CartProduct
from .mixins import CategoryDetailMixin, CartMixin     # должет первый по порядку наследоватся


# def test_base(request):
#     categories = Category.objects.get_categories_for_left_sidebar()    # для истользования объекта в шаблоне
#     return render(request, "base/base.html", {"categories": categories})


class BaseView(CartMixin, View):
    def get(self, request, *args, **kwargs):    # метод - аналог функции test_base (гет запрос)
        categories = Category.objects.get_categories_for_left_sidebar()   # для истользования объекта в шаблоне
        products = LatestProducts.objects.get_products_for_main_page(    # для вывода продусков на главной странице
            "notebook", "smartphone", with_respect_to="notebook"
        )
        context = {
            "categories": categories,
            "products": products,
            "cart": self.cart,
        }
        return render(request, "base/base.html", context)


class ProductDetailView(CartMixin, CategoryDetailMixin, DetailView):
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

    def get_context_data(self, **kwargs):    # для вывода необходимой информации для шаблона
        context = super().get_context_data(**kwargs)
        context["ct_model"] = self.model._meta.model_name
        context["cart"] = self.cart
        return context


class CategoryDetailView(CartMixin, CategoryDetailMixin, DetailView):
    model = Category
    queryset = Category.objects.all()
    context_object_name = "category"
    template_name = "mainapp/category_detail.html"
    slug_url_kwarg = "slug"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cart"] = self.cart
        return context


class AddToCartView(CartMixin, View):
    def get(self, request, *args, **kwargs):
        # логика добавление в корзину
        ct_model = kwargs.get("ct_model")    # контент-тайп модели
        product_slug = kwargs.get("slug")    # слаг товара
        # заменено миксином <CartMixin>
        # customer = Customer.objects.get(user=request.user)    # определение покупателя
        # cart = Cart.objects.get(owner=customer, in_order=False)    # выбор корзины данного покупателя
        content_type = ContentType.objects.get(model=ct_model)    # определение модели для выбранного товара
        product = content_type.model_class().objects.get(slug=product_slug)    # получение продукта через модель, находя продукт по слагу товара
        cart_product, created = CartProduct.objects.get_or_create(    # создание нового карт-продукт объекта с необходимым набором аргументов (get_or_create - для проверки наличия товара в корзине (возвращает кортеж)
            user=self.cart.owner, cart=self.cart, content_type=content_type,
            object_id=product.id,
        )
        if created:    # проверяет был ли создан новый объект (чтобы не добавлять один и тот же товар в корзину)
            self.cart.products.add(cart_product)    # добавление в корзину (add - это добавление в многих ко многим)
        self.cart.save()
        messages.add_message(request, messages.INFO, "Товар успешно добавлен")    # вывод информации о действии
        return HttpResponseRedirect("/cart/")    # перенаправить сразу в корзину


class DeleteFromCartView(CartMixin, View):
    def get(self, request, *args, **kwargs):
        ct_model = kwargs.get("ct_model")  # контент-тайп модели
        product_slug = kwargs.get("slug")  # слаг товара
        content_type = ContentType.objects.get(model=ct_model)  # определение модели для выбранного товара
        product = content_type.model_class().objects.get(
            slug=product_slug)  # получение продукта через модель, находя продукт по слагу товара
        cart_product = CartProduct.objects.get(
            user=self.cart.owner, cart=self.cart, content_type=content_type,
            object_id=product.id,
        )
        self.cart.products.remove(cart_product)  # удаление из корзины (remove - это удаление в многих ко многим)
        cart_product.delete()    # удаление товара из базы данных
        self.cart.save()
        messages.add_message(request, messages.INFO, "Товар успешно удален")  # вывод информации о действии
        return HttpResponseRedirect("/cart/")  # перенаправить сразу в корзину


class ChangeQTYView(CartMixin, View):
    def post(self, request, *args, **kwargs):    # пост запрос
        ct_model = kwargs.get("ct_model")  # контент-тайп модели
        product_slug = kwargs.get("slug")  # слаг товара
        content_type = ContentType.objects.get(model=ct_model)  # определение модели для выбранного товара
        product = content_type.model_class().objects.get(
            slug=product_slug)  # получение продукта через модель, находя продукт по слагу товара
        cart_product = CartProduct.objects.get(
            user=self.cart.owner, cart=self.cart, content_type=content_type,
            object_id=product.id,
        )
        qty = int(request.POST.get("qty"))
        cart_product.qty = qty
        cart_product.save()    # посчитать наличие корзины
        self.cart.save()    # сохранить информацию в корзину
        messages.add_message(request, messages.INFO, "Количество успешно изменено")  # вывод информации о действии
        return HttpResponseRedirect("/cart/")


class CartView(CartMixin, View):
    def get(self, request, *args, **kwargs):
        categories = Category.objects.get_categories_for_left_sidebar()
        context = {
            "cart": self.cart,
            "categories": categories,
        }
        return render(request, "mainapp/cart.html", context)
