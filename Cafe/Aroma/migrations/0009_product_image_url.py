# Generated by Django 5.0.6 on 2024-06-29 11:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Aroma", "0008_alter_orders_type_alter_product_vertical"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="image_url",
            field=models.URLField(default=""),
        ),
    ]
