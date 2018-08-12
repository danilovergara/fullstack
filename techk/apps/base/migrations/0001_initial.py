# Generated by Django 2.0.5 on 2018-08-12 22:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('price', models.FloatField(default=0.0)),
                ('tax', models.FloatField(default=0.0)),
                ('thumbnail_url', models.CharField(max_length=255)),
                ('added_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('product_description', models.TextField()),
                ('active', models.BooleanField(default=True)),
                ('upc', models.CharField(max_length=16)),
                ('stock', models.BooleanField(default=False)),
                ('rating', models.IntegerField(default=0)),
                ('reviews', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('active', models.BooleanField(default=True)),
            ],
        ),
        migrations.AddField(
            model_name='book',
            name='category_id',
            field=models.ForeignKey(on_delete='restrict', to='base.Category'),
        ),
    ]
