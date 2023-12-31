# Generated by Django 4.2.3 on 2023-08-14 20:56

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0002_tokenmodel"),
    ]

    operations = [
        migrations.AlterField(
            model_name="tokenmodel",
            name="token",
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
    ]
