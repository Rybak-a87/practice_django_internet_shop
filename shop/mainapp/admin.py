from django.forms import ModelChoiceField

from django.contrib import admin

from .models import *


class NotebookAdmin(admin.ModelAdmin):
    # form = NotebookAdminForm

    def formfield_for_foreignkey(self, db_field, request, **kwargs):    # для вывода только категори "notebook" при добавлении данных в БД
        if db_field.name == "category":
            return ModelChoiceField(Category.objects.filter(slug="notebooks"))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)    # если условие не срабатывает - возвращает стандартный результат работы


class SmartphoneAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):    # для вывода только категори "smartphone" при добавлении данных в БД
        if db_field.name == "category":
            return ModelChoiceField(Category.objects.filter(slug="smartphones"))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(Category)
admin.site.register(Notebook, NotebookAdmin)
admin.site.register(Smartphone, SmartphoneAdmin)
admin.site.register(CartProduct)
admin.site.register(Cart)
admin.site.register(Customer)

