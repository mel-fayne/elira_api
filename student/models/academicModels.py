from django.db import models

from student.models.studentModels import Student


GROUPINGS = ['cs01', 'cs02', 'cs03', 'cs04', 'cs05', 'cs06', 'cs07', 'cs08',
                 'cs09', 'cs10', 'cs11', 'cs12', 'cs13', 'cs14', 'cs15', 'cs16', 'cs17', 'cs18']

SCHOOLS = (
    ('UoN', 'University of Nairobi'),
    ('CUEA', 'Catholic University of East Africa'),
    ('KU', 'Kenyatta University'),
    ('JKUAT', 'Jomo Kenyatta University'),
    ('STRATH', 'Strathmore University')
)

SEMESETERS = (
    (1.0, 1.0),
    (1.1, 1.1),
    (1.2, 1.2),
    (2.0, 2.0),
    (2.1, 2.1),
    (2.2, 2.2),
    (3.0, 3.0),
    (3.1, 3.1),
    (3.2, 3.2),
    (4.0, 4.0),
    (4.1, 4.1),
    (4.2, 4.2)
)

GRADES = (
    ('A', 'A'),
    ('B', 'B'),
    ('C', 'C'),
    ('D', 'D'),
    ('E', 'E')
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
    current_sem = models.FloatField(max_length=50, choices=SEMESETERS)
    current_avg = models.FloatField(default=0.0)
    current_honours = models.CharField(
        max_length=50, choices=HONOURS, null=True)
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

    def __str__(self):
        return self.current_honours

    @property
    def acProfileId(self):
        return self.id
    
    @property
    def currentSem(self):
        return self.current_sem

    @property
    def school(self):
        return self.school

    @property
    def csMarks(self):
        marks = []
        for cs in GROUPINGS:
            marks.append(self.cs)
        return marks
    
    @property
    def cs01(self):
        return self.cs01
    
    @property
    def cs02(self):
        return self.cs02
    
    @property
    def cs03(self):
        return self.cs03
    
    @property
    def cs04(self):
        return self.cs04
    
    @property
    def cs05(self):
        return self.cs05
    
    @property
    def cs06(self):
        return self.cs06
    
    @property
    def cs07(self):
        return self.cs07
    
    @property
    def cs08(self):
        return self.cs08
    
    @property
    def cs09(self):
        return self.cs09
    
    @property
    def cs10(self):
        return self.cs10
    
    @property
    def cs11(self):
        return self.cs11
    
    @property
    def cs12(self):
        return self.cs12
    
    @property
    def cs13(self):
        return self.cs13
    
    @property
    def cs14(self):
        return self.cs14
    
    @property
    def cs15(self):
        return self.cs15
    
    @property
    def cs16(self):
        return self.cs16
    
    @property
    def cs17(self):
        return self.cs17
    
    @property
    def cs18(self):
        return self.cs18


class SchoolGrouping(models.Model):
    school = models.CharField(max_length=50, choices=SCHOOLS)
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=5)
    unit_percentage = models.FloatField(default=0.0)

    def __str__(self):
        return self.code + ' - ' + self.school

    @property
    def code(self):
        return self.code

    @property
    def unitPerc(self):
        return self.unit_percentage

class SchoolUnit(models.Model):

    school = models.CharField(max_length=50, choices=SCHOOLS)
    semester = models.FloatField(max_length=50, choices=SEMESETERS)
    name = models.CharField(max_length=50)
    elective = models.BooleanField(default=False)
    elective_group = models.CharField(max_length=50, null=True)
    grouping_name = models.JSONField(default=list)
    grouping_code = models.JSONField(default=list)
    unit_percentages = models.JSONField(default=list)
    grade = models.CharField(max_length=1, null=True, choices=GRADES)
    mark = models.FloatField(default=0.0)

    def __str__(self):
        return self.name

    @property
    def schoolUnitId(self):
        return self.id


class StudentUnit(models.Model):

    ac_profile = models.ForeignKey(
        AcademicProfile, null=True, on_delete=models.CASCADE)
    school_unit = models.OneToOneField(
        SchoolUnit, null=True, on_delete=models.CASCADE)
    grade = models.CharField(max_length=1, null=True, choices=GRADES)
    mark = models.FloatField(default=0.0)

    def __str__(self):
        return self.grade

    @property
    def mark(self):
        return self.mark

    @property
    def unitSem(self):
        return self.school_unit.semester

    @property
    def groupCodes(self):
        return self.school_unit.grouping_code

    @property
    def unitPercentages(self):
        return self.school_unit.unit_perc
