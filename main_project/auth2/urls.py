from django.urls import path
from .views import SignUpView
from . import views

urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path('', views.index, name='index'),
    path('extract_text/', views.extract_text, name='extract_text'),
    path('download_text/', views.download_text, name='download_text')
]