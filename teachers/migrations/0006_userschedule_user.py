# Generated by Django 4.0 on 2023-06-21 16:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('teachers', '0005_remove_userschedule_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='userschedule',
            name='user',
            field=models.ForeignKey(default=True, on_delete=django.db.models.deletion.CASCADE, to='auth.user'),
            preserve_default=False,
        ),
    ]
