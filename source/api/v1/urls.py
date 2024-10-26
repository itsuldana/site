from django.urls import path
from api.v1.views import ProgressApiView, ProgressUpdateApiView, PurchaseCreateApiView


urlpatterns=[
    path('lesson-progress/create/', ProgressApiView.as_view(), name='progress-create'),
    path('lesson-progress/<int:lesson_id>/', ProgressUpdateApiView.as_view(), name='progress-update'),

    path('purchase/create/', PurchaseCreateApiView.as_view(), name='purchase-create')
]