from django.urls import path
from django.contrib.auth import views as auth_views
from accounts.views import (
    RegisterView, LoginView, logout_view, activate, UserDetailView, UserUpdateView, UserEmailChangeView,
    confirm_email_change, CustomPasswordChangeView,
)

urlpatterns = [
    # auth and registration urls
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('activate/<uidb64>/<token>/', activate, name='activate'),
    path('logout/', logout_view, name='logout'),

    # password reset urls
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='password_reset/password_reset.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset/password_reset_complete.html'), name='password_reset_complete'),

    # user profile and edit urls
    path('profile/<int:pk>/', UserDetailView.as_view(), name='user_detail'),
    path('profile/<int:pk>/update/', UserUpdateView.as_view(), name='user_update'),
    path('profile/<int:pk>/change_email/', UserEmailChangeView.as_view(), name='change_email'),
    path('profile/confirm_email_change/<uidb64>/<token>/<new_email_encoded>/', confirm_email_change,
         name='confirm_email_change'),
    path('profile/<int:pk>/change_password/', CustomPasswordChangeView.as_view(), name='change_password'),
]
