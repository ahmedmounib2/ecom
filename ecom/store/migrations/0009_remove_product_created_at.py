# Generated by Django 4.2.10 on 2024-05-07 14:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0008_alter_profile_date_modified_remove_profile_old_cart_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='created_at',
        ),
    ]
