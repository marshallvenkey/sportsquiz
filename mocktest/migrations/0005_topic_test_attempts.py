# Generated by Django 4.0 on 2023-07-02 15:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mocktest', '0004_remove_testresult_end_time_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='topic',
            name='test_attempts',
            field=models.IntegerField(default=1),
        ),
    ]
