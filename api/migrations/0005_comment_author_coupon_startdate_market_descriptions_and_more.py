# Generated by Django 5.0.1 on 2025-01-11 02:53

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_product_farmer'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='author',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='coupon',
            name='startDate',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='market',
            name='descriptions',
            field=models.TextField(default="hello"),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='market',
            name='isActive',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='market',
            name='logoImage',
            field=models.CharField(default="hello", max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='market',
            name='slug',
            field=models.SlugField(blank=True, max_length=200, null=True, unique=True),
        ),
    ]
