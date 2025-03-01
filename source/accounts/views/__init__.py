from .user import (
    LoginView, RegisterView,
    activate, logout_view,
    UserDetailView, UserUpdateView, UserEmailChangeView,
    confirm_email_change, CustomPasswordChangeView, set_language, EmailConfirmView
)

from .teacher import (
    TeacherListView, TeacherDetailView, become_teacher
)
