# Generated by Django 2.2 on 2019-06-07 12:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_auto_20190607_1143'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phone_no',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.UserPhone', to_field='phone_no'),
        ),
    ]
