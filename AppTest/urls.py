from django.urls import path
from AppTest import views


urlpatterns = [
    path('apptest/', views.apptest),
    path('apptest_result_save/', views.apptest_result_save),
    path('start_app_test/', views.start_app_test),
    path('app_dataset/', views.app_dataset),
]