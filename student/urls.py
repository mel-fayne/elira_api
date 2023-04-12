from django.urls import path
from student.views.auth_views import ForgotPasswordView, LoginView, ResetOTPView, VerifyUserView, CrudUserView
from student.views.views import StudentView, AllStudentsView, TechnicalProfileView, WorkExpProfileView

urlpatterns = [
    # ---------- Student endpoints ------------
    path('student/<int:student_id>', StudentView.as_view()),
    path('all_students', AllStudentsView.as_view()),

    # ---------- TechProfile endpoints ------------
    path('tech_profile/<int:student_id>', TechnicalProfileView.as_view()),
    path('tech_profile', TechnicalProfileView.as_view()),

    # ---------- WorkExpProfile endpoints ------------
    path('workexp_profile/<int:student_id>', WorkExpProfileView.as_view()),
    path('workexp_profile', WorkExpProfileView.as_view()),

    # ---------- auth endpoints ------------
    path('register', CrudUserView.as_view()),
    path('user_account/<int:student_id>', CrudUserView.as_view()),
    path('login', LoginView.as_view()),
    path('verify_user/<int:student_id>', VerifyUserView.as_view()),
    path('verify_user', VerifyUserView.as_view()),
    path('forgot_password', ForgotPasswordView.as_view()),
    path('reset_password', ResetOTPView.as_view())
]
