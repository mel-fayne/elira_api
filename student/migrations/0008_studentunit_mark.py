# Generated by Django 4.1.2 on 2023-05-09 15:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("student", "0007_alter_schoolunit_name_alter_schoolunit_school_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="studentunit",
            name="mark",
            field=models.FloatField(default=0.0),
        ),
    ]
