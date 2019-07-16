# Generated by Django 2.2 on 2019-06-27 11:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0011_remove_user_phone_no'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='staff',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='userphone',
            name='owner',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='user_phone', serialize=False, to=settings.AUTH_USER_MODEL),
        ),
    ]
