# Generated by Django 5.0.6 on 2024-06-26 16:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Aroma", "0005_alter_users_password"),
    ]

    operations = [
        migrations.AlterField(
            model_name="orders",
            name="Type",
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name="product",
            name="Vertical",
            field=models.CharField(
                choices=[("Shake", "Shake"), ("Cake", "Cake"), ("Cookie", "Cookie")],
                max_length=10,
            ),
        ),
    ]
