from django.urls import path
from .auth_views import LoginView, ResetPasswordView, UserView
from .views import AllUsersView

urlpatterns = [
    path('login', LoginView.as_view()),
    path('user', UserView.as_view()),
    path('user/<int:user_id>', UserView.as_view()),
    path('all_users', AllUsersView.as_view()),
    path('reset_password', ResetPasswordView.as_view())
]