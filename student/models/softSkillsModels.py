from django.db import models

from student.models.studentModels import Student

class SoftSkillProfile(models.Model):

    student_id = models.OneToOneField(
        Student, null=True, on_delete=models.CASCADE)
    soft_skill_score = models.FloatField(default=0.0)

    @property
    def ssProfileId(self):
        return self.id


class SoftSkill(models.Model):
    SOFTSKILLS = (
        ('Teamwork', 'Teamwork'),
        ('Adaptability', 'Adaptability'),
        ('Problem Solving', 'Problem Solving'),
        ('Critical Thinking', 'Critical Thinking'),
        ('Communication', 'Communication'),
        ('Interpersonal Skills', 'Interpersonal Skills'),
        ('Leadership', 'Leadership'),
        ('Responsibility', 'Responsibility')
    )

    name = models.CharField(max_length=50, choices=SOFTSKILLS)
    score = models.FloatField(default=0.0)
    ss_profile = models.ForeignKey(
        SoftSkillProfile, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    @property
    def ssProfileId(self):
        return self.id
