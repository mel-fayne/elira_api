# Generated by Django 4.1.2 on 2023-04-17 10:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0010_softskillprofile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='softskillprofile',
            name='mbti',
        ),
        migrations.RemoveField(
            model_name='softskillprofile',
            name='skills',
        ),
        migrations.AlterField(
            model_name='softskillprofile',
            name='student_id',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='student.student'),
        ),
        migrations.AlterField(
            model_name='technicalprofile',
            name='student_id',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='student.student'),
        ),
        migrations.AlterField(
            model_name='workexpprofile',
            name='student_id',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='student.student'),
        ),
        migrations.CreateModel(
            name='SoftSkill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('Teamwork', 'Teamwork'), ('Adaptability', 'Adaptability'), ('Problem Solving', 'Problem Solving'), ('Critical Thinking', 'Critical Thinking'), ('Communication', 'Communication'), ('Interpersonal Skills', 'Interpersonal Skills'), ('Leadership', 'Leadership'), ('Responsibility', 'Responsibility')], max_length=50)),
                ('score', models.FloatField(default=0.0)),
                ('ss_profile', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='student.softskillprofile')),
            ],
        ),
    ]
