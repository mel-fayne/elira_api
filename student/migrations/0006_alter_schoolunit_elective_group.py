# Generated by Django 4.1.2 on 2023-05-09 11:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("student", "0005_academicprofile_cs01_academicprofile_cs02_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="schoolunit",
            name="elective_group",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]