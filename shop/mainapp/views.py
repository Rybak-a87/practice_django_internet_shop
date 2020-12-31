from django.shortcuts import render
from django.views.generic import DetailView

from .models import Notebook, Smartphone


def test_base(request):
    return render(request, "base/base.html")


class ProductDetailView(DetailView):
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
