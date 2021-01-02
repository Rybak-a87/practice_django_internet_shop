from django.urls import path
from . import views


app_name = "mainapp"    # имя приложения


urlpatterns = [
    path("", views.test_base, name="base"),
    path("products/<str:ct_model>/<str:slug>/", views.ProductDetailView.as_view(), name="product_detail"),
    path("category/<str:slug>/", views.CategoryDetailView.as_view(), name="category_detail"),
]
