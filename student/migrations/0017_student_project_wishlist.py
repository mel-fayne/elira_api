# Generated by Django 4.0.6 on 2023-06-01 00:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0016_alter_studentunit_school_unit'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='project_wishlist',
            field=models.JSONField(default=list),
        ),
    ]
