from django.urls import path
from django.contrib.sitemaps.views import sitemap
from webapp import views
from webapp.sitemaps import StaticViewSitemap, CourseSitemap, PostSitemap

sitemaps = {
    'static': StaticViewSitemap,
    'courses': CourseSitemap,
    'posts': PostSitemap,
}

urlpatterns = [
    # Главная
    # path('', views.IndexView.as_view(), name='index'),

    path('', views.MainView.as_view(), name='index'),

    # Robots.txt
    path('robots.txt', views.robots_txt, name='robots_txt'),

    # Sitemapp
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),

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
    path('modules/manage/<int:pk>', views.ManageModulesView.as_view(), name='manage_modules'),

    # urls для уроков
    path('modules/<int:pk>/lessons/create/', views.LessonCreateView.as_view(), name='lesson_create'),
    path('lessons/<int:pk>/edit/', views.LessonUpdateView.as_view(), name='lesson_edit'),
    path('lessons/<int:pk>/', views.LessonDetailView.as_view(), name='lesson_detail'),
    path('lessons/<int:pk>/delete/', views.LessonDeleteView.as_view(), name='lesson_delete'),
    path('lessons/manage/<int:pk>', views.ManageLessonsView.as_view(), name='manage_lessons'),

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
