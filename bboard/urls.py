from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView, \
    PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import reverse_lazy

from .views import *

app_name = 'bboard'

urlpatterns = [
    path('<int:rubric_id>/',    BbByRubricView.as_view(),   name='by_rubric'),  # имя маршрута by_rubric
    path('',                    index,                      name='index'),      # имя маршрута index
    path('add/',                BbCreateView.as_view(),     name='add'),     # добавление записи
    path('edit/<int:pk>/',      BbUpdateView.as_view(),     name='edit'),    # изменение записи
    path('delete/<int:pk>/',    BbDeleteView.as_view(),     name='delete'),  # удаление записи
    path('detail/<int:pk>/',    BbDetailView.as_view(),     name='detail'),  # просмотр записи

    path('accounts/login/',     LoginView.as_view(),        name='login'),   # логин
    path('accounts/logout/',    LogoutView.as_view(),       name='logout'),  # выход из под пользователя

    path('accounts/password_change/',       PasswordChangeView.as_view(      # изменение пароля
        template_name='registration/change_password.html', success_url=reverse_lazy('bboard:password_change_done')),
        name='password_change'),
    path('accounts/password_change/done/',  PasswordChangeDoneView.as_view(  # сообщение об успешном изменении пароля
        template_name='registration/password_changed.html'), name='password_change_done'),

    path('accounts/password_reset/', PasswordResetView.as_view(              # запрос на сброс пароля
        template_name='registration/reset_password.html',
        success_url=reverse_lazy('bboard:password_reset_done'),
        subject_template_name='registration/reset_subject.txt',
        email_template_name='registration/reset_email.txt'),
        name='password_reset'),
    path('accounts/password_reset/done/', PasswordResetDoneView.as_view(template_name='registration/email_sent.html'),
         name='password_reset_done'),

    path('accounts/reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view( # сброс пароля
        template_name='registration/confirm_password.html', success_url=reverse_lazy('bboard:password_reset_complete')
    ), name='password_reset_confirm'),
    path('accounts/reset/done/', PasswordResetCompleteView.as_view(
        template_name='registration/password_confirmed.html'), name='password_reset_complete'),


    path('pictures/', add_picture, name='add_picture'),


    # REST

    path('api/rubrics/', api_rubrics, name='apirub'),
    path('api/bboard/<int:pk>/', BboardDetailRestView.as_view(), name='apirub'),
]