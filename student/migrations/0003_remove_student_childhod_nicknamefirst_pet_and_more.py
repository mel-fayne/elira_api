# Generated by Django 4.1.2 on 2023-05-09 10:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0002_student_password'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='childhod_nicknamefirst_pet',
        ),
        migrations.AddField(
            model_name='student',
            name='first_pet',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='childhod_nickname',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='childhood_street',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='favourite_flavour',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='first_phone',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='first_teacher',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
