from django.urls import path

from .views import (
    UserCreateView,
    UserRetrieveView,
    UserUpdateView,
    Confirmation,
    check_token,
    AuthToken,
    # reset_password,
    # ResetPasswordToken,
    GetMeView,
    PartnerCreateView,
    SecretKeyRetrieveView,
    ResetPasswordView,
    SecretKeysListView,
    SecretKeyGetView,
    SecretKeyUpdateView,
    SecretKeyCreateView,
    SecretKeyDeleteView,
)


urlpatterns = [
    path('user/create/', UserCreateView.as_view()),
    path('user-personal-data/get/<int:pk>', UserRetrieveView.as_view()),
    path('user-personal-data/update/<int:pk>', UserUpdateView.as_view()),
    path('user/confirm/', Confirmation.as_view()),
    # path('user/reset-password/', reset_password),
    path('user/reset-password/', ResetPasswordView.as_view()),
    # path('user/request-reset-password/', ResetPasswordToken.as_view()),
    path('check-token/', check_token),
    path('token-auth/', AuthToken.as_view()),
    path('get-me/', GetMeView.as_view()),
    path('get-key/', SecretKeyRetrieveView.as_view()),
    path('keys/', SecretKeysListView.as_view()),
    path('key/get/<int:pk>/', SecretKeyGetView.as_view()),
    path('key/update/<int:pk>/', SecretKeyUpdateView.as_view()),
    path('key/delete/<int:pk>/', SecretKeyDeleteView.as_view()),
    path('key/create/', SecretKeyCreateView.as_view()),
    path('partner/create/', PartnerCreateView.as_view()),
]
