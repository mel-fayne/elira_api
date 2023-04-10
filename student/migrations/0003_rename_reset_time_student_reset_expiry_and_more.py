# Generated by Django 4.1.2 on 2023-04-10 09:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0002_rename_last_name_name_student_last_name_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='student',
            old_name='reset_time',
            new_name='reset_expiry',
        ),
        migrations.AddField(
            model_name='student',
            name='isVerified',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='student',
            name='verify_otp',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='first_name',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='last_name',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='reset_otp',
            field=models.IntegerField(null=True),
        ),
    ]
