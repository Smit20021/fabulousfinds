from django.urls import path
from adminapp import views

app_name = 'adminapp'
urlpatterns = [
      path('', views.AdminLogin.as_view(), name='login'),
    path('register/', views.AdminCreation.as_view(), name='register'),
    path('dashboard/', views.Home, name='home'),
    path('logout', views.Logout, name='logout'),
    path('addcity/', views.ManageCity.as_view(), name='city'),
    path('editcity/<int:id>/',views.ManageCity.as_view(),name='EditCity'),
    path('deletecity/<int:cityid>/',views.ManageCity.as_view(),name='DeleteCity'),
    path('addarea/', views.ManageArea.as_view(), name='area'),
    path('editarea/<int:id>/',views.ManageArea.as_view(),name='EditArea'),
    path('deletearea/<int:areaid>/',views.ManageArea.as_view(),name='DeleteArea'),
    path('bindareas/', views.load_areasbyCity, name='load_areas'),
    path('addemployee/', views.ManageEmployee.as_view(), name='employee'),
    path('editemployee/<int:id>/',views.ManageEmployee.as_view(),name='EditEmployee'),
    path('deleteemployee/<int:employeeid>/',views.ManageEmployee.as_view(),name='DeleteEmployee'),
    path('employeetask/',views.EmployeeTask.as_view(),name='Task'),
    path('bindcustomerdata/', views.load_CustomerData, name='load_data'),
    path('binddelivereddata/', views.DeliveryOrderDetails.as_view(), name='delivery'),
]
