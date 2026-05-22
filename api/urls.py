from django.urls import path
from .views import GoogleOAuth2CallbackView

urlpatterns = [
    path('auth/google/callback/', GoogleOAuth2CallbackView.as_view(), name='google_oauth2_callback'),
]
