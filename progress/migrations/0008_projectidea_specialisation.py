# Generated by Django 4.0.6 on 2023-06-01 21:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('progress', '0007_specroadmap_remove_projectidea_specialisation'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectidea',
            name='specialisation',
            field=models.CharField(choices=[('AI', 'Artificial Intellignce & Data Science'), ('CS', 'Cyber Security'), ('DA', 'Data Administration'), ('GD', 'Graphic Design'), ('HO', 'Hardware & Operating Systems'), ('IS', 'Information Systems'), ('NC', 'Network Configuration'), ('SD', 'Software Development')], max_length=50, null=True),
        ),
    ]