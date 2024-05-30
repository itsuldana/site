from django.urls import path

from webapp.views import IndexView, CoursesView, CourseView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('courses', CoursesView.as_view(), name='courses'),
    path('course', CourseView.as_view(), name='course'),
    # path('photos/', IndexView.as_view(), name='photo_list'),
    # path('photos/create', PhotoCreateView.as_view(), name='photo_create'),
    # path('photos/<int:pk>/detail', PhotoDetailView.as_view(), name='photo_detail'),
    # path('photos/<int:pk>/update', PhotoUpdateView.as_view(), name='photo_update'),
    # path('photos/<int:pk>/delete', PhotoDeleteView.as_view(), name='photo_delete'),
]
