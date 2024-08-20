from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('Trans-dediers/', views.upload_lld, name='upload_lld'),
    path('Co-Trans/', views.upload_lld_Co_Trans, name='upload_lld_Co_Trans'),
    path('download-script/', views.download_script, name='download_script'),
]