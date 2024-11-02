from django.urls import path
from webapp.views.course import (
    CourseCreateView, CourseDetailView, CourseUpdateView, CourseListView, CoursesView, CoursePaidListView
)
from webapp.views.lessons import LessonCreateView, LessonUpdateView, LessonDeleteView, LessonDetailView
from webapp.views.module import ModuleCreateView, ModuleUpdateView
from webapp.views.purchase import purchase_course, purchase_success, purchase_failure
from webapp.views.main_about_us import MainView

urlpatterns = [
    # Лэндинг (он же О нас или About Us)
    path('', MainView.as_view(), name='main_about_us'),

    path('', CourseListView.as_view(), name='index'),

    path('courses/', CoursesView.as_view(), name='course_list'),

    # urls для курсов
    path('courses/create/', CourseCreateView.as_view(), name='course_create'),
    path('courses/<int:pk>/detail/', CourseDetailView.as_view(), name='course_detail'),
    path('courses/<int:pk>/edit/', CourseUpdateView.as_view(), name='course_edit'),
    path('courses/list', CourseListView.as_view(), name='course_list'),
    path('courses/paid_list/', CoursePaidListView.as_view(), name='course_paid_list'),

    # urls для модулей
    path('courses/<int:pk>/modules/create/', ModuleCreateView.as_view(), name='module_create'),
    path('modules/<int:pk>/edit/', ModuleUpdateView.as_view(), name='module_edit'),

    # urls для уроков
    path('modules/<int:pk>/lessons/create/', LessonCreateView.as_view(), name='lesson_create'),
    path('lessons/<int:pk>/edit/', LessonUpdateView.as_view(), name='lesson_edit'),
    path('lessons/<int:pk>/', LessonDetailView.as_view(), name='lesson_detail'),
    path('lessons/<int:pk>/delete/', LessonDeleteView.as_view(), name='lesson_delete'),

    # urls для оплаты
    path('purchase/<int:course_id>/', purchase_course, name='purchase_course'),
    path('purchase/success/', purchase_success, name='purchase_success'),
    path('purchase/failure/', purchase_failure, name='purchase_failure'),
]
