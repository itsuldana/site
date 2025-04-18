from django.urls import path
from django.contrib.auth import views as auth_views
import accounts.views as views

urlpatterns = [
    # change language url
    path('set_language/', views.set_language, name='set_language'),

    # auth and registration urls
    path('login/', views.LoginView.as_view(), name='login'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('logout/', views.logout_view, name='logout'),
    path('email_confirm/', views.EmailConfirmView.as_view(), name='email_confirm'),

    # password reset urls
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='password_reset/password_reset.html'),
         name='password_reset'),
    path('password_reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='password_reset/password_reset_done.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='password_reset/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(template_name='password_reset/password_reset_complete.html'),
         name='password_reset_complete'),

    # user profile and edit urls
    path('profile/<int:pk>/', views.UserDetailView.as_view(), name='user_detail'),
    path('profile/<int:pk>/update/', views.UserUpdateView.as_view(), name='user_update'),
    path('profile/<int:pk>/change_email/', views.UserEmailChangeView.as_view(), name='change_email'),
    path('profile/confirm_email_change/<uidb64>/<token>/<new_email_encoded>/', views.confirm_email_change,
         name='confirm_email_change'),
    path('profile/<int:pk>/change_password/', views.CustomPasswordChangeView.as_view(), name='change_password'),

    # Teachers URLS
    path('teachers/', views.TeacherListView.as_view(), name='teacher_list'),
    path('teachers/<int:pk>/', views.TeacherDetailView.as_view(), name='teacher_detail'),
    path('teachers/<int:pk>/update', views.TeacherUpdateView.as_view(), name='teacher_update'),
    path('teachers/create/', views.become_teacher, name='become_teacher'),
    path('teachers/confirm/', views.TeacherConfirmView.as_view(), name='teacher_confirm'),
    path('teachers/<int:pk>/payment/', views.TeacherPaymentView.as_view(), name='teacher_payment'),

    # manage urls
    # path('manage/courses/', views.ManageCoursesView.as_view(), name='manage_courses'),
    # path('manage/courses/<int:pk>/modules/}', views.ManageModulesView.as_view(), name='manage_modules'),
    # path('manage/modules/<int:pk>/lessons/}', views.ManageLessonsView.as_view(), name='manage_lessons'),
]
