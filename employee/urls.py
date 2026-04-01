from django.urls import path
from employee import views

app_name = 'employee'
urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('login/', views.EmployeeLogin.as_view(), name='emplogin'),
    path('work/', views.ManageTask.as_view(), name='empwork'),
    path('logout/', views.EmployeeLogout.as_view(), name='logout'),
    path('bindcustomerdata/', views.load_CustomerData, name='load_data'),
    path('bindcustomerpersonal/', views.load_CustomerPersonalInfo, name='loadcustomerdata'),
]
