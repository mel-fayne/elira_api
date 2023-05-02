from django.urls import path

from student.views.authViews import LoginView, CrudUserView
from student.views.softskills_views import SoftSkillProfileView
from student.views.views import StudentView, AllStudentsView, TechnicalProfileView
from student.views.workexp_views import WorkExpProfileView

urlpatterns = [
     # ---------- auth endpoints ------------
    path('register', CrudUserView.as_view()),
    path('user_account/<int:student_id>', CrudUserView.as_view()),
    path('login', LoginView.as_view()),
    path('confirm_user/<str:email>', LoginView.as_view()),

    # ---------- Student endpoints ------------
    path('student/<int:student_id>', StudentView.as_view()),
    path('all_students', AllStudentsView.as_view()),

    # ---------- TechProfile endpoints ------------
    path('tech_profile/<int:student_id>', TechnicalProfileView.as_view()),
    path('tech_profile', TechnicalProfileView.as_view()),

    # ---------- WorkExpProfile endpoints ------------
    path('workexp_profile/<int:student_id>', WorkExpProfileView.as_view()),
    path('workexp_profile', WorkExpProfileView.as_view()),

    # ---------- SoftSkillProfile endpoints ------------
    path('softskill_profile/<int:student_id>', SoftSkillProfileView.as_view()),
    path('softskill_profile', SoftSkillProfileView.as_view())
]
