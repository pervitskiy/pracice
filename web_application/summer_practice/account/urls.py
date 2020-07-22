from django.contrib.auth import views
from django.urls import path

from . import views as v

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', v.LoggedPage.as_view(), name='logout'),
    path('password-reset/', views.PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('profile/', v.ProfilePage.as_view(), name="profile"),
    path('register/', v.RegisterView.as_view(), name="register"),
]