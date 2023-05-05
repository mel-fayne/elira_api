# from django.db import models

# from student.models.authModels import Student

# class TechnicalProfile(models.Model):

#     student_id = models.OneToOneField(
#         Student, null=True, on_delete=models.CASCADE)
#     git_username = models.CharField(max_length=50)
#     total_commits = models.IntegerField(default=0)
#     total_prs = models.IntegerField(default=0)
#     current_streak = models.IntegerField(default=0)
#     top_languages = models.JSONField(default=dict)
#     repos = models.JSONField(default=dict)
#     technical_score = models.FloatField(default=0.0)
#     specialisation_rank = models.JSONField(default=dict)

#     def __str__(self):
#         return self.git_username


# class WorkExpProfile(models.Model):
#     student_id = models.OneToOneField(
#         Student, null=True, on_delete=models.CASCADE)
#     work_exp_score = models.FloatField(default=0.0)
#     specialisation_rank = models.JSONField(default=dict)

#     def getId(self):
#         return self.id


# class WorkExp(models.Model):
#     EMP_TYPE = (
#         ('Full-Time', 'Full-Time'),
#         ('Part-Time', 'Part-Time'),
#         ('Internship', 'Internship')
#     )

#     LOC_TYPE = (
#         ('Online', 'Online'),
#         ('Hybrid', 'Hybrid'),
#         ('On-Site', 'On-Site')
#     )

#     INDUSTRIES = (
#         ('Software Development', 'Software Development'),
#         ('Networking', 'Networking'),
#         ('Data Science & AI', 'Data Science & AI'),
#         ('Cyber Security', 'Cyber Security'),
#         ('Database Administration', 'Database Administration'),
#         ('IT & Support', 'IT & Support'),
#         ('Mobile Development', 'Mobile Development'),
#         ('Web Development', 'Web Development'),
#         ('Design', 'Design'),
#     )

#     wx_profile = models.ForeignKey(
#         WorkExpProfile, null=True, on_delete=models.CASCADE)
#     title = models.CharField(max_length=100)
#     employment_type = models.CharField(max_length=100, choices=EMP_TYPE)
#     company_name = models.CharField(max_length=100)
#     location = models.CharField(max_length=100)
#     location_type = models.CharField(max_length=100, choices=LOC_TYPE)
#     start_date = models.DateField()
#     end_date = models.DateField(null=True)
#     industry = models.CharField(max_length=100, choices=INDUSTRIES)
#     skills = models.JSONField(default=dict)

#     def __str__(self):
#         return self.title


# class SoftSkillProfile(models.Model):

#     student_id = models.OneToOneField(
#         Student, null=True, on_delete=models.CASCADE)
#     soft_skill_score = models.FloatField(default=0.0)

#     def getId(self):
#         return self.id


# class SoftSkill(models.Model):
#     SOFTSKILLS = (
#         ('Teamwork', 'Teamwork'),
#         ('Adaptability', 'Adaptability'),
#         ('Problem Solving', 'Problem Solving'),
#         ('Critical Thinking', 'Critical Thinking'),
#         ('Communication', 'Communication'),
#         ('Interpersonal Skills', 'Interpersonal Skills'),
#         ('Leadership', 'Leadership'),
#         ('Responsibility', 'Responsibility')
#     )

#     name = models.CharField(max_length=50, choices=SOFTSKILLS)
#     score = models.FloatField(default=0.0)
#     ss_profile = models.ForeignKey(
#         SoftSkillProfile, null=True, on_delete=models.CASCADE)

#     def __str__(self):
#         return self.name
