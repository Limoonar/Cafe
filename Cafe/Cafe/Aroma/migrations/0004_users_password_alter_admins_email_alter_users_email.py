# Generated by Django 5.0.6 on 2024-06-25 13:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Aroma", "0003_rename_id_product_id_rename_id_storage_id"),
    ]

    operations = [
        migrations.AddField(
            model_name="users",
            name="Password",
            field=models.CharField(
                default=models.CharField(
                    max_length=255, primary_key=True, serialize=False, unique=True
                ),
                max_length=255,
                unique=True,
            ),
        ),
        migrations.AlterField(
            model_name="admins",
            name="Email",
            field=models.EmailField(max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name="users",
            name="Email",
            field=models.EmailField(max_length=255, unique=True),
        ),
    ]
