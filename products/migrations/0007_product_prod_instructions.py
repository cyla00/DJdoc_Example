# Generated by Django 3.1.2 on 2020-12-11 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_auto_20201209_1710'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='prod_instructions',
            field=models.TextField(default='null', null=True),
        ),
    ]
