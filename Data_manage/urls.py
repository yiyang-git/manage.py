from django.urls import path
from Data_manage import views


urlpatterns = [
    path('table/', views.show_table),
    path('del_data/', views.del_data),
    path('add_task/', views.add_task),
    path('edit_task/', views.edit_task),
    path('scan_process/', views.show_process),
    path('spot_table/', views.show_spot_table),
    path('del_spot/', views.del_spot),
]