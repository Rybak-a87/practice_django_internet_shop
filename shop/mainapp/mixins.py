from django.views.generic.detail import SingleObjectMixin
from django.views.generic import View

from .models import Category, Cart, Customer


# Миксин для вывода информации о категориях на любой странице сайта
class CategoryDetailMixin(SingleObjectMixin):
    def get_context_data(self, **kwargs):    # функция для вывода контента в вьешке (аналог <{"categories": categories}> в функции test_view)
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.get_categories_for_left_sidebar()
        return context


class CartMixin(View):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:    # если пользователь авторизован
            customer = Customer.objects.filter(user=request.user).first()    # поиск пользователя
            if not customer:    # если покупателя нет - создаем покупателя
                customer = Customer.objects.cteate(user=request.user)
            cart = Cart.objects.filter(owner=customer, in_order=False).first()    # поиск корзины которая относится к этому пользователю и не находится в заказе
            if not cart:    # если корзина найдена - созается новую корзина этого пользователя
                cart = Cart.objects.create(owner=customer)
        else:    # если пользовательне авторизован
            cart = Cart.objects.filter(for_anonymous_user=True).first()    # поиск корзины анонимного пользователя
            if not cart:
                cart = Cart.objects.create(for_anonymous_user=True)    # создание анонимной корзины
        self.cart = cart
        return super().dispatch(request, *args, **kwargs)