from django.urls import path

from accounts.views import RegisterView, LoginView, logout_view, activate

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('activate/<uidb64>/<token>/', activate, name='activate'),
    path('logout/', logout_view, name='logout'),

    # path('profile/<int:pk>/', UserDetailView.as_view(), name='user_detail'),
    # path('profile/<int:pk>/update/', UserUpdateView.as_view(), name='user_update'),
]
