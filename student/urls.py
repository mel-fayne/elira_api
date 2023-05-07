from django.urls import path

from student.views.academicViews import AcademicProfileView, StudentUnitView, SchoolUnitView
from student.views.authViews import AllStudentsView, LoginView, CrudUserView
from student.views.technicalViews import TechnicalProfileView

urlpatterns = [
    # ---------- auth endpoints ------------
    path('register', CrudUserView.as_view()),
    path('user_account/<int:student_id>', CrudUserView.as_view()),
    path('login', LoginView.as_view()),
    path('confirm_user/<str:email>', LoginView.as_view()),
    path('all_students', AllStudentsView.as_view()),

    # ---------- AcademicProfile endpoints ---------- 
    path('academic_profile/<int:student_id>', AcademicProfileView.as_view()),
    path('academic_profile', AcademicProfileView.as_view()),
    path('student_units/<int:ac_profileId>', StudentUnitView.as_view()),
    path('student_units', StudentUnitView.as_view()),
    path('school_units/<str:groupBy>/<str:school>', SchoolUnitView.as_view()),

    # ---------- TechProfile endpoints ------------
    path('tech_profile/<int:student_id>', TechnicalProfileView.as_view()),
    path('tech_profile', TechnicalProfileView.as_view()),

    # # ---------- WorkExpProfile endpoints ------------
    # path('workexp_profile/<int:student_id>', WorkExpProfileView.as_view()),
    # path('workexp_profile', WorkExpProfileView.as_view()),

    # # ---------- SoftSkillProfile endpoints ------------
    # path('softskill_profile/<int:student_id>', SoftSkillProfileView.as_view()),
    # path('softskill_profile', SoftSkillProfileView.as_view())
]
