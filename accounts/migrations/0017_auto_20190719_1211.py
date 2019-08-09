# Generated by Django 2.2 on 2019-07-19 12:11

from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0016_auto_20190719_0727'),
    ]

    operations = [
        migrations.AddField(
            model_name='guestemail',
            name='phone_no',
            field=phonenumber_field.modelfields.PhoneNumberField(max_length=128, null=True, region=None),
        ),
        migrations.AlterField(
            model_name='guestemail',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, help_text='email last created on', verbose_name='date created'),
        ),
        migrations.AlterField(
            model_name='guestemail',
            name='email',
            field=models.EmailField(max_length=255, verbose_name='email address'),
        ),
    ]