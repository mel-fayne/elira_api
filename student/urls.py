from django.urls import path

from student.views.academicViews import AcademicProfileView, StudentTranscript, StudentUnitView, SchoolUnitView, UnitGroupsView
from student.views.authViews import AllStudentsView, ForgotPasswordView, LoginView, CrudUserView
from student.views.classifierViews import ClassifierModelView
from student.views.softskillsViews import SoftSkillProfileView
from student.views.technicalViews import TechnicalProfileView
from student.views.workexpViews import WorkExpProfileView, WorkExperienceView

urlpatterns = [
    # ---------- auth endpoints ------------
    path('register', CrudUserView.as_view()),
    path('user_account/<int:student_id>', CrudUserView.as_view()),
    path('login', LoginView.as_view()),
    path('confirm_user/<str:email>', LoginView.as_view()),
    path('reset_password/<str:email>', ForgotPasswordView.as_view()),
    path('all_students', AllStudentsView.as_view()),

    # ---------- AcademicProfile endpoints ----------
    path('academic_profile/<int:student_id>', AcademicProfileView.as_view()),
    path('academic_profile', AcademicProfileView.as_view()),
    path('student_units/<int:student_id>', StudentUnitView.as_view()),
    path('student_units', StudentUnitView.as_view()),
    path('student_transcript/<int:student_id>/<str:new_sem>', StudentTranscript.as_view()),
    path('school_units/<str:groupBy>/<str:school>', SchoolUnitView.as_view()),
    path('school_units', SchoolUnitView.as_view()),
    path('unit_groupings', UnitGroupsView.as_view()),

    # ---------- TechProfile endpoints ------------
    path('tech_profile/<int:student_id>', TechnicalProfileView.as_view()),
    path('tech_profile', TechnicalProfileView.as_view()),

    # ---------- WorkExpProfile endpoints ------------
    path('wx_profile/<int:student_id>', WorkExpProfileView.as_view()),
    path('wx_profile', WorkExpProfileView.as_view()),
    path('workexp/<int:wxId>', WorkExperienceView.as_view()),
    path('workexp', WorkExperienceView.as_view()),

    # ---------- SoftSkillProfile endpoints ------------
    path('softskill_profile/<int:student_id>', SoftSkillProfileView.as_view()),
    path('softskill_profile', SoftSkillProfileView.as_view()),


    # ---------- Classifier endpoints ------------
    path('classifier/<int:student_id>', ClassifierModelView.as_view())
]
