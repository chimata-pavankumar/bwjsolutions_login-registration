# Generated by Django 2.0.7 on 2020-01-09 14:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users_table',
            name='Resume',
            field=models.ImageField(upload_to="{% static 'styles/images' %}"),
        ),
    ]