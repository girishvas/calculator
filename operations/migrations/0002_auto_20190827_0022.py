# Generated by Django 2.2.4 on 2019-08-26 20:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operations', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='calculation',
            name='secondValue',
            field=models.DecimalField(blank=True, decimal_places=10, max_digits=19, null=True),
        ),
    ]
