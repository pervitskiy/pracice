from . import views
from django.urls import path

urlpatterns = [
    path('create', views.FormView.as_view(), name='create'),
    path('', views.show_the_list_of_students, name='list_student'),
    path('<int:student_id>/', views.detail_student, name='detail_student')
]
