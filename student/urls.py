from django.urls import path
from student.views.auth_views import ForgotPasswordView, LoginView, ResetOTPView, UserView
from student.views.views import AllStudentsView

urlpatterns = [
    # ---------- GET endpoints ------------
    path('student/<int:student_id>', UserView.as_view()),
    path('all_students', AllStudentsView.as_view()),

    # ---------- auth endpoints ------------
    path('register', UserView.as_view()),
    path('login', LoginView.as_view()),
    path('forgot_password', ForgotPasswordView.as_view()),
    path('reset_password', ResetOTPView.as_view()),
]
