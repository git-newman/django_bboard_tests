# Generated by Django 2.2.13 on 2020-07-16 05:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bboard', '0004_auto_20200715_1151'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bb',
            name='rubric',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='bboard.Rubric',
                                    verbose_name='Рубрика'),
        ),
    ]
