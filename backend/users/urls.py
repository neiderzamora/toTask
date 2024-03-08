from django.urls import path
from .views import ManualTokenObtainView, CustomUserDetail, CustomUserList
from . import views

urlpatterns = [
    path('sign-in', ManualTokenObtainView.as_view(), name='api-login'),
    path('user', CustomUserList.as_view(), name='create_get_user'),
    path('user/<uuid:pk>', CustomUserDetail.as_view(), name='user_detail')
]