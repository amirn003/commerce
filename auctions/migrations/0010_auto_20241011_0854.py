# Generated by Django 3.1.3 on 2024-10-11 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0009_auto_20241011_0842'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='picture',
            field=models.ImageField(blank=True, default='pictures/default.jpeg', null=True, upload_to='pictures/'),
        ),
    ]
