# Generated by Django 4.1.6 on 2023-02-21 20:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_categories_listings_comments_bids'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='categories',
            name='name',
        ),
        migrations.AddField(
            model_name='categories',
            name='category_type',
            field=models.CharField(choices=[('F', 'Fashion'), ('T', 'Toys'), ('E', 'Electronics'), ('H', 'Home'), ('O', 'Others')], default='F', max_length=1),
        ),
    ]
