# Generated by Django 4.1.6 on 2023-02-22 19:16

import datetime
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_listing_rename_bids_bid_rename_comments_comment_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='bid',
            name='date',
            field=models.DateField(default=datetime.date.today, null=True),
        ),
        migrations.AddField(
            model_name='bid',
            name='listing',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='listing_bid', to='auctions.listing'),
        ),
        migrations.AddField(
            model_name='bid',
            name='value',
            field=models.IntegerField(null=True, validators=[django.core.validators.MinValueValidator(1)]),
        ),
        migrations.AddField(
            model_name='comment',
            name='content',
            field=models.CharField(max_length=2500, null=True),
        ),
        migrations.AddField(
            model_name='comment',
            name='date',
            field=models.DateField(default=datetime.date.today, null=True),
        ),
        migrations.AddField(
            model_name='comment',
            name='listing',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='listing_comment', to='auctions.listing'),
        ),
        migrations.AddField(
            model_name='listing',
            name='date',
            field=models.DateField(default=datetime.date.today, null=True),
        ),
        migrations.AlterField(
            model_name='bid',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='bid_owner', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='comment',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comment_owner', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='listing',
            name='current_bid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='current_bid', to='auctions.bid'),
        ),
        migrations.CreateModel(
            name='Watchlist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('listing', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='listing_watchlist', to='auctions.listing')),
                ('owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='watchlist_owner', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
