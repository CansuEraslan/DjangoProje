# Generated by Django 3.0.4 on 2020-05-15 22:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0004_auto_20200509_0413'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('New', 'New'), ('Accepted', 'Accepted'), ('Preaparing', 'Preaparing'), ('Onshipping', 'Onshipping'), ('Completed', 'Completed'), ('Canceled', 'Canceled'), ('Library', 'Library')], default='New', max_length=10),
        ),
    ]
