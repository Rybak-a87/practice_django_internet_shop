from django.views.generic.detail import SingleObjectMixin

from .models import Category


# Миксин
class CategoryDetailMixin(SingleObjectMixin):
    def get_context_data(self, **kwargs):    # функция для вывода контента в вьешке (аналог <{"categories": categories}> в функции test_view)
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.get_categories_for_left_sidebar()
        return context
