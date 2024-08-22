from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView # type: ignore
from . import views


urlpatterns = [
    path("", views.index, name="index"),

    # API endpoints
    path('upload-lld-api/', views.upload_lld_api, name='upload_lld_api'),
    path('upload-lld-Co-Trans-api/', views.upload_lld_Co_Trans_api, name='upload_lld_Co_Trans_api'),
    path('download-script-api/', views.download_script_api, name='download_script_api'),
    path('edit-script/', views.edit_script, name='edit_script'),

    path("user/register/", views.CreateUserView.as_view(), name="register"),
    path("token/", TokenObtainPairView.as_view(), name="get_token"),
    path("token/refresh/", TokenRefreshView.as_view(), name="refresh"),
    path("api-auth/", include("rest_framework.urls")),
]
