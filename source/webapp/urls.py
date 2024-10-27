from django.urls import path
from webapp.views.course import CourseCreateView, CourseDetailView, CourseUpdateView, CourseListView, CoursesView
from webapp.views.lessons import LessonCreateView, LessonUpdateView, LessonDeleteView, LessonDetailView
from webapp.views.module import ModuleCreateView, ModuleUpdateView
from webapp.views.purchase import purchase_course, purchase_success, purchase_failure
from webapp.views.main_test import test_main_page
from webapp import views


urlpatterns = [
    # index url
    path('', CourseListView.as_view(), name='index'),

    path('courses/', CoursesView.as_view(), name='course_list'),

    # urls для курсов
    path('courses/create/', CourseCreateView.as_view(), name='course_create'),
    path('courses/<int:pk>/detail/', CourseDetailView.as_view(), name='course_detail'),
    path('courses/<int:pk>/edit/', CourseUpdateView.as_view(), name='course_edit'),
    path('courses/list', CourseListView.as_view(), name='course_list'),

    # urls для модулей
    path('courses/<int:pk>/modules/create/', ModuleCreateView.as_view(), name='module_create'),
    path('modules/<int:pk>/edit/', ModuleUpdateView.as_view(), name='module_edit'),

    # urls для курсов
    path('modules/<int:pk>/lessons/create/', LessonCreateView.as_view(), name='lesson_create'),
    path('lessons/<int:pk>/edit/', LessonUpdateView.as_view(), name='lesson_edit'),
    path('lessons/<int:pk>/', LessonDetailView.as_view(), name='lesson_detail'),
    path('lessons/<int:pk>/delete/', LessonDeleteView.as_view(), name='lesson_delete'),

    #urls для оплатыj
    path('purchase/<int:course_id>/', purchase_course, name='purchase_course'),
    path('purchase/success/', purchase_success, name='purchase_success'),
    path('purchase/failure/', purchase_failure, name='purchase_failure'),

    path('test_main/', test_main_page, name='test_main_page'),

    #urls для тестов от модуля
    path('test_module/<int:module_id>/test/', views.TestModuleDetailView.as_view(), name='test_view'),
    path('test_module/<int:test_module_id>/submit/', views.TestSubmitView.as_view(), name='test_submit'),
]
