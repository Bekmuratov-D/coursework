# Generated by Django 4.1.7 on 2023-04-14 04:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0003_rename_date_added_order_time'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='time',
        ),
    ]
