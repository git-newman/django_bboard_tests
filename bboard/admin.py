from django.contrib import admin

# Register your models here.

from .models import *


class BbAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'price', 'published', 'rubric')  # отображение списка записей
    list_display_links = ('title', 'content')  # поля которые преобразованы в гиперссылки
    search_fields = ('title', 'content',)  # поля по которым идет фильтрация


class RubricAdmin(admin.ModelAdmin):
    list_display = ('name',)  # отображение списка записей
    list_display_links = ('name',)  # поля которые преобразованы в гиперссылки
    search_fields = ('name',)  # поля по которым идет фильтрация


class ImgAdmin(admin.ModelAdmin):
    list_display = ('img', 'desc')


# вносим изменения в админскую страницу
admin.site.register(Bb, BbAdmin)
admin.site.register(Rubric, RubricAdmin)
admin.site.register(Img, ImgAdmin)
