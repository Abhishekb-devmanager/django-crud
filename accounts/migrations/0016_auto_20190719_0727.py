# Generated by Django 2.2 on 2019-07-19 07:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0015_auto_20190719_0726'),
    ]

    operations = [
        migrations.AddField(
            model_name='guestemail',
            name='modified_at',
            field=models.DateTimeField(auto_now=True, help_text='email last updated on', verbose_name='date created'),
        ),
        migrations.AlterField(
            model_name='guestemail',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, help_text='email last updated on', verbose_name='date created'),
        ),
    ]
