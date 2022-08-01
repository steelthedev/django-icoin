from django.urls import path,include
from . import views
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path('signup', views.RegisterView, name="register"),
    path('api/v1/', include('djoser.urls.authtoken')),
    path('api/password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    path('profile', views.ProfileView),
    path('profile-edit', views.ProfileEdit),
    path('change-picture', views.ProfilePictureEdit),
]
