from django.contrib import admin

from student.models.authModels import Student
from student.models.academicModels import AcademicProfile, SchoolUnit, StudentUnit


admin.site.register(Student)
admin.site.register(AcademicProfile)
admin.site.register(SchoolUnit)
admin.site.register(StudentUnit)
