# Generated by Django 4.2.1 on 2023-06-23 16:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mocktest', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userdetail',
            old_name='add1',
            new_name='distname',
        ),
        migrations.RenameField(
            model_name='userdetail',
            old_name='mobile',
            new_name='mandalname',
        ),
        migrations.RenameField(
            model_name='userdetail',
            old_name='cat',
            new_name='schoolname',
        ),
        migrations.RenameField(
            model_name='userdetail',
            old_name='gender',
            new_name='studentname',
        ),
    ]
