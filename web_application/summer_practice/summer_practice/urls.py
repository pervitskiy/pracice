from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('profile/', include('questionary.urls')),
    path('', include('attestation.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('account.urls'))
]
