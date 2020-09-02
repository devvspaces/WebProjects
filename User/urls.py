from django.urls import path
from .views import Logout, Authentication, ChangePasswordView, ResetPasswordView
from django.contrib.auth.views import PasswordResetView,PasswordResetDoneView,PasswordResetConfirmView,PasswordResetCompleteView

urlpatterns = [
	path('auth/<str:type>/', Authentication, name='authentication'),
	path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('logout/', Logout, name='logout'),
	path("password-reset-confirm/<uidb64>/<token>/",PasswordResetConfirmView.as_view(template_name="User/password_reset_confirm.html"), name="password_reset_confirm"),
	path("password-reset-complete",PasswordResetCompleteView.as_view(template_name="User/password_reset_complete.html"), name="password_reset_complete")
]