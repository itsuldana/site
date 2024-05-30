from django.urls import path

from webapp.views.course import CourseCreateView, CourseDetailView, CourseUpdateView, CourseListView

urlpatterns = [
    # index url
    path('', CourseListView.as_view(), name='course_list'),

    # urls для курсов
    path('courses/create/', CourseCreateView.as_view(), name='course_create'),
    path('courses/<int:pk>/detail/', CourseDetailView.as_view(), name='course_detail'),
    path('courses/<int:pk>/edit/', CourseUpdateView.as_view(), name='course_edit'),
    path('courses/', CourseListView.as_view(), name='course_list'),
]
