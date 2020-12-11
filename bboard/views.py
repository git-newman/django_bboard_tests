from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.core.paginator import Paginator
from django.template.response import TemplateResponse
from django.contrib.messages.views import SuccessMessageMixin
from rest_framework.views import APIView

from .forms import *

from .models import *
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView

from django.contrib.auth.mixins import LoginRequiredMixin

from django.views.decorators.http import require_http_methods

#  REST

from django.http import JsonResponse
from .serializer import *
from rest_framework.response import Response
from rest_framework.decorators import api_view


# Create your views here.


def index(request):
    """Контроллер главной страницы"""
    imgs = Img.objects.all()
    bbs = Bb.objects.all()
    paginator = Paginator(bbs, 5)
    if 'page' in request.GET:
        page_num = request.GET['page']
    else:
        page_num = 1
    page = paginator.get_page(page_num)

    page_start = 1

    if int(page_num) > 2:
        page_start = int(page_num) - 2

    if int(page_num) + 2 >= page.paginator.num_pages:
        page_end = page.paginator.num_pages
    else:
        page_end = int(page_num) + 3

    page_list = list(range(int(page_start), page_end + 1))

    context = {'page': page, 'bbs': page.object_list, 'page_list': page_list, 'imgs': imgs}
    return TemplateResponse(request, 'bboard/index.html', context)


class BbCreateView(SuccessMessageMixin, CreateView):
    """Контроллер создания объявления"""
    template_name = 'bboard/create.html'  # путь к файлу шаблона для вывода страницы с формой
    form_class = BbForm  # класс формы
    success_url = '/{rubric_id}'  # адрес для перехода в случае успеха через имя маршрута
    success_message = 'Объявление создано'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class BbUpdateView(SuccessMessageMixin, UpdateView):
    """Контроллер изменения объявления"""
    model = Bb
    form_class = BbForm  # класс формы
    success_url = '/'  # адрес для перехода в случае успеха через имя маршрута
    success_message = 'Объявление изменено'
    template_name_suffix = '_update'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['rubrics'] = Rubric.objects.all()
        return context


class BbDeleteView(SuccessMessageMixin, DeleteView):
    """Контроллер удаления объявления с подтверждением"""
    model = Bb
    success_url = '/'
    success_message = 'Объявление удалено'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        return context


class BbDetailView(DetailView):
    """Контроллер подробного вывода одной записи"""
    model = Bb

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        return context


class BbByRubricView(LoginRequiredMixin, ListView):
    """Контроллер вывода всех записей по рубрике"""
    template_name = 'bboard/by_rubric.html'
    context_object_name = 'bbs'

    # def get_paginator(self, queryset, per_page, orphans=0,
    #                   allow_empty_first_page=True, **kwargs):
    #     return Paginator(Rubric.objects.get(pk=self.kwargs['rubric_id']), 5)

    def get_queryset(self):
        return Bb.objects.filter(rubric=self.kwargs['rubric_id'])

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['current_rubric'] = Rubric.objects.get(pk=self.kwargs['rubric_id'])
        return context


def add_picture(request):
    if request.method == 'POST':
        form = ImgForm(request.POST, request.FILES)
        if form.is_valid():
            for file in request.FILES.getlist('img'):
                img = Img()
                img.desc = form.cleaned_data['desc']
                img.img = file
                img.save()
            return redirect('bboard:index')
    else:
        form = ImgForm()
    context = {'form': form}
    return render(request, 'bboard/upload_picture.html', context)


# REST

@api_view(['GET'])
def api_rubrics(request):
    if request.method == 'GET':
        rubrics = Rubric.objects.filter(id=1)
        serializer = RubricSerializer(rubrics, many=True)
        return Response(data=serializer.data, template_name=None)


class BboardDetailRestView(APIView):

    def get(self, request, pk):
        bb = Bb.objects.get(id=pk)
        serializer = BboardSerialiser(bb, many=False)
        return Response(serializer.data)


# def add_and_save(request):
#     rubrics = Rubric.objects.all()
#     if request.method == 'POST':
#         bbf = BbForm(request.POST)
#         if bbf.is_valid():
#             bbf.save()
#             return redirect('bboard:by_rubric', rubric_id=bbf.cleaned_data['rubric'].pk)
#         else:
#             context = {'form': bbf, 'rubrics': rubrics}
#             return render(request, 'bboard/create.html', context)
#     else:
#         bbf = BbForm()
#         context = {'form': bbf, 'rubrics': rubrics}
#         return render(request, 'bboard/create.html', context)


# def by_rubric(request, rubric_id):
#    bbs = Bb.objects.filter(rubric=rubric_id)
#    rubrics = Rubric.objects.all()
#    current_rubric = Rubric.objects.get(pk=rubric_id)
#    context = {'bbs': bbs, 'rubrics': rubrics, 'current_rubric': current_rubric}
#    return render(request, 'bboard/by_rubric.html', context)


# class BbCreateView(FormView):
#     """контроллер для создания объявления"""
#     template_name = 'bboard/create.html'
#     form_class = BbForm
#     initial = {'price': 0.0}
#
#     def get_context_data(self, *args, **kwargs):
#         context = super().get_context_data(*args, **kwargs)
#         context['rubrics'] = Rubric.objects.all()
#         return context
#
#     def form_valid(self, form):
#         form.save()
#         return super().form_valid(form)
#
#     def get_form(self, form_class=None):
#         self.object = super().get_form(form_class)
#         return self.object
#
#     def get_success_url(self):
#         return reverse('bboard:by_rubric', kwargs={'rubric_id': self.object.cleaned_data['rubric'].pk})
