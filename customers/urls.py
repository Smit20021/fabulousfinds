from django.urls import path
from customers import views

app_name = 'customers'
urlpatterns = [
    path('', views.ShowShopes.as_view(), name='home'),
    path('about/', views.About, name='aboutus'),
    path('contact/', views.Contact, name='contactus'),
    path('login/',views.CustomerLogin.as_view(), name='login'),
    path('custlogout',views.CustomerLogout.as_view(), name='customerlogout'),
    path('register/',views.CustomerRegistration.as_view(), name='registration'),
    path('bindareas/', views.load_areasbyCity, name='load_areas'),
    path('showproducts/<int:id>/',views.ShowProductsByShopes.as_view(), name='showproducts'),
    path('showcart/',views.ShowCartItems.as_view(), name='showcarts'),
    path('updatecarts',views.PlusMinusItems.as_view(), name='updatecart'),
    path('removecarts/<int:id>/',views.RemoveItems.as_view(), name='removecart'),
    path('checkoutcart/',views.CheckOut.as_view(), name='checkout'),
    path('orders/',views.CustomerHistory.as_view(), name='orderdetails'),
   
    # path('addtocart/',views.AddtoProducts.as_view(), name='addproduct'),

]
