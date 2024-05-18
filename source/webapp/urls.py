from django.urls import path

from webapp.views import IndexView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    # path('photos/', IndexView.as_view(), name='photo_list'),
    # path('photos/create', PhotoCreateView.as_view(), name='photo_create'),
    # path('photos/<int:pk>/detail', PhotoDetailView.as_view(), name='photo_detail'),
    # path('photos/<int:pk>/update', PhotoUpdateView.as_view(), name='photo_update'),
    # path('photos/<int:pk>/delete', PhotoDeleteView.as_view(), name='photo_delete'),
]
