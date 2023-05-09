# Generated by Django 4.1.2 on 2023-05-09 16:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("student", "0008_studentunit_mark"),
    ]

    operations = [
        migrations.AddField(
            model_name="academicprofile",
            name="school",
            field=models.CharField(
                choices=[
                    ("UoN", "University of Nairobi"),
                    ("CUEA", "Catholic University of East Africa"),
                    ("KU", "Kenyatta University"),
                    ("JKUAT", "Jomo Kenyatta University"),
                    ("STRATH", "Strathmore University"),
                ],
                default="JKUAT",
                max_length=50,
            ),
            preserve_default=False,
        ),
    ]
