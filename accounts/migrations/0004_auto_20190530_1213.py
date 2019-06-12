# Generated by Django 2.2 on 2019-05-30 12:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_remove_user_is_admin'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='is_active',
            new_name='active',
        ),
        migrations.AddField(
            model_name='user',
            name='admin',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='reader',
            field=models.BooleanField(default=True),
        ),
    ]
