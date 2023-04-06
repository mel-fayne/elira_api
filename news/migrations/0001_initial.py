# Generated by Django 4.1.2 on 2023-04-04 12:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='NewsGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_ids', models.JSONField(default=list)),
            ],
        ),
        migrations.CreateModel(
            name='NewsPiece',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source', models.CharField(max_length=50)),
                ('source_img', models.CharField(max_length=50)),
                ('title', models.CharField(max_length=500)),
                ('link', models.CharField(max_length=800)),
                ('header_img', models.CharField(max_length=800)),
                ('publication', models.CharField(max_length=50)),
                ('tags', models.JSONField(default=list)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]