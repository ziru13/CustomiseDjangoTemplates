from django.urls import path
from . import views

app_name = 'courses'

# make our variable, a list, in the old Django, it didn't use to be a list, now it's just a list
urlpatterns = [
    path('', views.course_list, name='course_list'),
    path('<int:course_pk>/<int:step_pk>/', views.step_detail, name='step_detail'),
    path('<int:pk>/', views.course_detail, name='course_detail'),
]