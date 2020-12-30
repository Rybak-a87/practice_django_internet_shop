from django.urls import path
from . import views


app_name = "mainapp"    # имя приложения


urlpatterns = [
    path("", views.test_base, name="base"),
]
