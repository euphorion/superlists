# Generated by Django 4.0.1 on 2022-01-31 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lists', '0003_alter_item_text'),
    ]

    operations = [
        migrations.CreateModel(
            name='List',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
    ]
