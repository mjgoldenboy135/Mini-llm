from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView
from .views import RegisterView, LoginView, OTPRequestView, OTPVerifyView, MeView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("otp/request/", OTPRequestView.as_view(), name="otp_request"),
    path("otp/verify/", OTPVerifyView.as_view(), name="otp_verify"),
    path("me/", MeView.as_view(), name="me"),
]
