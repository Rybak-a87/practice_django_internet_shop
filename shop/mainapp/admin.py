from PIL import Image    # работа с изображением

from django.forms import ModelChoiceField, ModelForm, ValidationError
from django.contrib import admin
from django.utils.safestring import mark_safe    # строку превращает в HTML отрисовывает со стилями и тегами которые ему передаюд

from .models import *


class NotebookAdminForm(ModelForm):    # форма проверки изображения
    def __init__(self, *args, **kwargs):    # подсказка для загрузки изображения
        super().__init__(*args, **kwargs)    # переопределение
        self.fields["image"].help_text = mark_safe(    # закрасить подсказку
            # f"<span style='color:red;'>Загрудайте изображение с минимальным размером "
            f"<span style='color:red;'>Изображение будет обрезано если оно более "
            f"{Product.MIN_RESOLUTION[0]}x{Product.MIN_RESOLUTION[1]}</span>"
        )

    # def clean_image(self):    # работа с изображением (проверка по размеру и разрешению)
    #     image = self.cleaned_data["image"]    # атрибут size - возвращает размер файла
    #     img = Image.open(image)    # атрибут size - возвращает кортех разрешения изображения
    #     min_height, min_width = Product.MIN_RESOLUTION    # минимальное разрешение картинки
    #     max_height, max_width = Product.MAX_RESOLUTION    # максимальное разрешение картинки
    #     if image.size > Product.MAX_IMAGE_SIZE:   # проверка на допучтимый размер файла
    #         raise ValidationError("Размер изображения не должен привышать 3МВ!")    # Вывод ошибки в виде подсказки
    #     if img.height < min_height or img.width < min_width:    # проверка на минимальное разрешение изображения
    #         raise ValidationError("Разрешение изображения меньше минимального!")
    #     if img.height > max_height or img.width > max_width:    # проверка на максимальное разрешение изображения
    #         raise ValidationError("Разрешение изображения больше максимального!")
    #     return image


class NotebookAdmin(admin.ModelAdmin):
    form = NotebookAdminForm

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

