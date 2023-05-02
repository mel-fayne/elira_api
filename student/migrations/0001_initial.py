# Generated by Django 4.1.2 on 2023-05-02 22:26

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50, null=True)),
                ('last_name', models.CharField(max_length=50, null=True)),
                ('email', models.CharField(max_length=100, unique=True)),
                ('specialisation', models.CharField(choices=[('AI', 'Artificial Intellignce & Data Science'), ('CS', 'Cyber Security'), ('DA', 'Data Administration'), ('GD', 'Graphic Design'), ('HO', 'Hardware & Operating Systems'), ('IS', 'Information Systems'), ('NC', 'Network Configuration'), ('SD', 'Software Development')], max_length=50)),
                ('compatibility_scores', models.JSONField(default=list)),
                ('user_token', models.CharField(max_length=200, null=True)),
                ('last_active', models.CharField(max_length=200, null=True)),
                ('first_pet', models.CharField(max_length=200, null=True)),
                ('childhood_street', models.CharField(max_length=200, null=True)),
                ('first_teacher', models.CharField(max_length=200, null=True)),
                ('favourite_flavour', models.CharField(max_length=200, null=True)),
                ('childhod_nickname', models.CharField(max_length=200, null=True)),
                ('first_phone', models.CharField(max_length=200, null=True)),
                ('news_history', models.JSONField(default=list, null=True)),
            ],
        ),
    ]
