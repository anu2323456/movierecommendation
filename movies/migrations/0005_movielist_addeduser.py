# Generated by Django 4.2.13 on 2024-07-02 11:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0004_category_movielist'),
    ]

    operations = [
        migrations.AddField(
            model_name='movielist',
            name='addeduser',
            field=models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
