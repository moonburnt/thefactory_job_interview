# Generated by Django 4.2.3 on 2023-08-14 22:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("api", "0003_alter_tokenmodel_token"),
    ]

    operations = [
        migrations.CreateModel(
            name="TgUserModel",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("user_id", models.TextField(editable=False, unique=True)),
                (
                    "token",
                    models.OneToOneField(
                        default=None,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="tg_bot_token",
                        to="api.tokenmodel",
                    ),
                ),
            ],
        ),
    ]
