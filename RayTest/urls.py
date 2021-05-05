from django.urls import path
from RayTest import views


urlpatterns = [
    path('raytest/', views.raytest),
    path('raytest_result_save/', views.raytest_result_save),
]