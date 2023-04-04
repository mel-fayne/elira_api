from django.urls import path
from student.auth_views import LoginView, ResetPasswordView, UserView
from student.views import AllStudentsView

urlpatterns = [
    # ---------- GET endpoints ------------
    path('student/<int:student_id>', UserView.as_view()),
    path('all_students', AllStudentsView.as_view()),

    # ---------- auth endpoints ------------
    path('register', UserView.as_view()),
    path('login', LoginView.as_view()),
    path('reset_password', ResetPasswordView.as_view())
]