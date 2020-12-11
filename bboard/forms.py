from django.forms import ModelForm
from django.core.exceptions import ValidationError
from .models import *
from django import forms
from captcha.fields import CaptchaField
from django.core import validators


class BbForm(ModelForm):
    price = forms.DecimalField(decimal_places=2)
    captcha = CaptchaField(label='Введите текст с картинки', error_messages={'invalid': 'Неправильный текст капчи'})

    class Meta:
        model = Bb
        fields = ('title', 'content', 'price', 'rubric', 'captcha')

    def clean(self):
        super().clean()
        errors = {}
        if not self.cleaned_data['content']:
            errors['content'] = ValidationError('Укажите описание продаваемого товара')
        if not self.cleaned_data['price']:
            errors['price'] = ValidationError('Укажите правильное значение цены')
        elif int(self.cleaned_data['price']) < 0:
            errors['price'] = ValidationError('Укажите неотрицательное значение цены')
        if errors:
            raise ValidationError(errors)


class SearchFrom(forms.Form):
    keyword = forms.CharField(max_length=20, label='Искомое слово')
    rubric = forms.ModelChoiceField(queryset=Rubric.objects.all(), label='Рубрика')


class ImgForm(forms.ModelForm):
    img = forms.ImageField(label='Изображение', validators=[validators.FileExtensionValidator(
        allowed_extensions=('gif', 'jpg', 'png', 'jpeg'))],
        error_messages={'invalid_extension': 'Этот формат файлов не поддерживается'},
        widget=forms.widgets.ClearableFileInput(attrs={'multiple':True}))
    desc = forms.CharField(label='Описание', widget=forms.widgets.Textarea())

    class Meta:
        model = Img
        fields = '__all__'
