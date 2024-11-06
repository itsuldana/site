from django.urls import path
from api.v1.views import ProgressApiView, ProgressUpdateApiView, PurchaseCreateApiView
from api.v1.views.feedback_view import FeedbackApiView

urlpatterns=[
    path('lesson-progress/create/', ProgressApiView.as_view(), name='progress-create'),
    path('lesson-progress/<int:lesson_id>/', ProgressUpdateApiView.as_view(), name='progress-update'),

    path('purchase/create/', PurchaseCreateApiView.as_view(), name='purchase-create'),

    path('feedback/create/', FeedbackApiView.as_view(), name='feedback-create'),
]