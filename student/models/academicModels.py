from django.db import models

from student.models.authModels import Student

SCHOOLS = (
    ('UoN', 'University of Nairobi'),
    ('CUEA', 'Catholic University of East Africa'),
    ('KU', 'Kenyatta University'),
    ('JKUAT', 'Jomo Kenyatta University'),
    ('STRATH', 'Strathmore University')
)

SEMESETERS = (
    ('1.0', '1.0'),
    ('1.1', '1.1'),
    ('1.2', '1.2'),
    ('2.0', '2.0'),
    ('2.1', '2.1'),
    ('2.2', '2.2'),
    ('3.0', '3.0'),
    ('3.1', '3.1'),
    ('3.2', '3.2'),
    ('4.0', '4.0'),
    ('4.1', '4.1'),
    ('4.2', '4.2')
)

class AcademicProfile(models.Model):
    HONOURS = (
        ('First Class', 'First Class'),
        ('Second Upper', 'Second Upper'),
        ('Second Lower', 'Second Lower'),
        ('Pass', 'Pass'),
        ('Fail', 'Fail')
    )

    student_id = models.OneToOneField(
        Student, null=True, on_delete=models.CASCADE)
    school = models.CharField(max_length=50, choices=SCHOOLS)
    current_sem = models.CharField(max_length=50, choices=SEMESETERS)
    current_avg = models.FloatField(default=0.0)
    current_honours = models.CharField(max_length=50, choices=HONOURS)
    cs01 = models.FloatField(default=0.0)
    cs02 = models.FloatField(default=0.0)
    cs03 = models.FloatField(default=0.0)
    cs04 = models.FloatField(default=0.0)
    cs05 = models.FloatField(default=0.0)
    cs06 = models.FloatField(default=0.0)
    cs07 = models.FloatField(default=0.0)
    cs08 = models.FloatField(default=0.0)
    cs09 = models.FloatField(default=0.0)
    cs10 = models.FloatField(default=0.0)
    cs11 = models.FloatField(default=0.0)
    cs12 = models.FloatField(default=0.0)
    cs13 = models.FloatField(default=0.0)
    cs14 = models.FloatField(default=0.0)
    cs15 = models.FloatField(default=0.0)
    cs16 = models.FloatField(default=0.0)
    cs17 = models.FloatField(default=0.0)
    cs18 = models.FloatField(default=0.0)


class SchoolUnit(models.Model):     # a general unit stored for the differnet schools with their grouping details

    school = models.CharField(max_length=50, choices=SCHOOLS)
    semester = models.CharField(max_length=50, choices=SEMESETERS)
    name = models.CharField(max_length=50)
    elective = models.BooleanField(default=False)
    elective_group = models.CharField(max_length=50, null=True)
    grouping_name = models.JSONField(default=list)
    grouping_code = models.JSONField(default=list)
    unit_perc = models.JSONField(default=list)

    def __str__(self):
        return self.name
    

class StudentUnit(models.Model):    # a unit a studnet is taking along with their mark for that unit
    GRADES = (
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D'),
        ('E', 'E')
    )
    
    ac_profile = models.ForeignKey(
        AcademicProfile, null=True, on_delete=models.CASCADE)
    school_unit = models.OneToOneField(
        SchoolUnit, null=True, on_delete=models.CASCADE)
    grade = models.CharField(max_length=1, choices=GRADES)
    mark = models.FloatField(default=0.0)

    def __str__(self):
        return self.grade
