from . import views
from django.urls import path,include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('users/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('users/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('',views.user),
    path('register/',views.users),
    path('forgotPassword/',views.forgot_password),
    path('password_reset/',include('django_rest_passwordreset.urls',namespace='password_reset')),
    path('addUser/',views.addUser),
    path('addStudent/',views.addStudent),
    path('getDetails/',views.getDetails),
]