# Generated by Django 3.1.3 on 2020-11-21 19:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0005_auto_20201121_1948'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='favourite_category',
            field=models.ManyToManyField(blank=True, to='news.Category'),
        ),
    ]
