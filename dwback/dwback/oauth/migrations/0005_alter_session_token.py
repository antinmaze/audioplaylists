# Generated by Django 4.0.1 on 2022-01-27 21:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oauth', '0004_alter_session_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='session',
            name='token',
            field=models.CharField(max_length=300),
        ),
    ]
