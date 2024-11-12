from django.urls import path

from webapp import views

urlpatterns = [
    # Лэндинг (он же О нас или About Us)
    path('', views.IndexView.as_view(), name='index'),

    # Help Page
    path('contact_us/', views.ContactUsView.as_view(), name='contact_us'),
    path('send_email/', views.send_email, name='send_email'),

    path('courses/', views.CoursesView.as_view(), name='course_list'),

    # urls для курсов
    path('courses/create/', views.CourseCreateView.as_view(), name='course_create'),
    path('courses/<int:pk>/detail/', views.CourseDetailView.as_view(), name='course_detail'),
    path('courses/<int:pk>/edit/', views.CourseUpdateView.as_view(), name='course_edit'),
    path('courses/list', views.CourseListView.as_view(), name='course_list'),
    path('courses/paid_list/', views.CoursePaidListView.as_view(), name='course_paid_list'),

    # urls для модулей
    path('courses/<int:pk>/modules/create/', views.ModuleCreateView.as_view(), name='module_create'),
    path('modules/<int:pk>/edit/', views.ModuleUpdateView.as_view(), name='module_edit'),

    # urls для уроков
    path('modules/<int:pk>/lessons/create/', views.LessonCreateView.as_view(), name='lesson_create'),
    path('lessons/<int:pk>/edit/', views.LessonUpdateView.as_view(), name='lesson_edit'),
    path('lessons/<int:pk>/', views.LessonDetailView.as_view(), name='lesson_detail'),
    path('lessons/<int:pk>/delete/', views.LessonDeleteView.as_view(), name='lesson_delete'),

    # urls для оплаты
    path('purchase/<int:course_id>/', views.purchase_course, name='purchase_course'),
    path('purchase/success/', views.purchase_success, name='purchase_success'),
    path('purchase/failure/', views.purchase_failure, name='purchase_failure'),

    # urls для тестов от модуля
    path('start-test/<int:module_id>/', views.StartTestView.as_view(), name='start_test'),
    path('next-test/<int:test_id>/', views.NextTestView.as_view(), name='next_test'),
    path('result-test/<int:test_id>/', views.ResultView.as_view(), name='result'),
    path('history-result-test/<int:module_id>/', views.TestModuleResultView.as_view(), name='test_history'),

    path('test-case-description/<int:course_id>/', views.TestCaseDescriptionDetailView.as_view(),
         name='test_case_description_detail'),
    path('test_modules/<int:cours>/cours/', views.TestModulesList.as_view(), name='test_models'),
    path('pricces-test/<int:test_id>/', views.TestDetailView.as_view(), name='test_detail'),

    path('dashboard/<int:cours_id>/', views.DashboardView.as_view(), name='dashboard'),
]
