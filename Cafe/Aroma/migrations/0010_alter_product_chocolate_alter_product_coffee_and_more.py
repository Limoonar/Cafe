# Generated by Django 5.0.6 on 2024-07-02 04:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Aroma', '0009_product_image_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='Chocolate',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='product',
            name='Coffee',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='product',
            name='Flour',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='product',
            name='Price',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='product',
            name='Sugar',
            field=models.FloatField(),
        ),
    ]
