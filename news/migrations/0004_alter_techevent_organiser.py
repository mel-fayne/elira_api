# Generated by Django 4.1.2 on 2023-04-06 16:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0003_alter_techevent_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='techevent',
            name='organiser',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
