from dj_rest_auth.registration.views import (
    ResendEmailVerificationView,
    VerifyEmailView,
)
from dj_rest_auth.views import (
    PasswordResetConfirmView,
    PasswordResetView,
)
from .views import email_confirm_redirect, password_reset_confirm_redirect
from dj_rest_auth.registration.views import RegisterView
from dj_rest_auth.views import LoginView, LogoutView, UserDetailsView
from django.urls import path

urlpatterns = [
    # Registration Related
    
    path('register/', RegisterView.as_view(), name='register'), # For registration
    path('register/verify-email/', VerifyEmailView.as_view(), name='verify-email'), # For email verification
    path('register/resend-email/', ResendEmailVerificationView.as_view(), name='resend-email'), # For resending email verification
    path('account-confirm-email/<str:key>/', email_confirm_redirect, name='account_confirm_email'), # For email confirmation redirect
    path('account-confirm-email/', VerifyEmailView.as_view(), name='account_email_verification_sent'), # For email confirmation

    # Login Related
    path('login/', LoginView.as_view(), name='login'), # For login
    path('logout/', LogoutView.as_view(), name='logout'), # For logout

    # User Related
    path('user/', UserDetailsView.as_view(), name='user'), # For user details
    path('password/reset/', PasswordResetView.as_view(), name='password-reset'), # For password reset
    path( # For password reset confirmation redirect
        'password/reset/confirm/<uidb64>/<token>/', 
        password_reset_confirm_redirect, 
        name='password_reset_confirm'
    ), 
    path('password/reset/confirm/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'), # For password reset confirmation
]