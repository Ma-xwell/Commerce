# Generated by Django 4.1.6 on 2023-02-25 03:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0012_rename_winners_winner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='photo_url',
            field=models.URLField(max_length=500, null=True),
        ),
    ]
