from django.contrib import admin

from student.models.authModels import Student
from student.models.academicModels import AcademicProfile, SchoolUnit, StudentUnit
from student.models.technicalModels import TechnicalProfile
from student.models.workExpModels import WorkExpProfile, WorkExperience


admin.site.register(Student)

admin.site.register(AcademicProfile)
admin.site.register(SchoolUnit)
admin.site.register(StudentUnit)

admin.site.register(TechnicalProfile)

admin.site.register(WorkExpProfile)
admin.site.register(WorkExperience)
