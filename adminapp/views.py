from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib.auth import logout
from adminapp.models import City,Area, Employee,Admintbl
from .forms import  CityForm, AreaForm, EmployeeForm, AdminForm
from django.views import  View
from giftkeepers.models import CustomerOrders
from django.contrib.sessions.models import Session

# Create your views here.
class AdminCreation(View):
    def get(self, request):
        storage = messages.get_messages(request)
        for message in storage:
            message = None
        if request.session.get('CName') is None:
          return redirect('adminapp:adminlogin') 
        adminData = Admintbl.objects.all().order_by('-id')
        form = AdminForm()
        context={
            'form' : form,
            'adminData' : adminData
        }
        return render(request, 'adminapp/register.html',context)
    
    def post(self, request):
        form = AdminForm(request.POST)
        messages.info(request,'New Admin Inserted Success!')
        form.save()
        adminData = Admintbl.objects.all().order_by('-id')
        form = AdminForm()
        context={
            'form' : form,
            'adminData' : adminData
        }
        return render(request, 'adminapp/register.html',context)


def Home(request):
    storage = messages.get_messages(request)
    for message in storage:
        message = None
    if request.session.get('CName') is None:
        return redirect('adminapp:login') 
    return render(request,'adminapp/home.html')

def Logout(request):
    storage = messages.get_messages(request)
    for message in storage:
        message = None
    storage.used = False
    logout(request)
    Session.objects.all().delete()
    return redirect('adminapp:login')

class AdminLogin(View):
    def get(self, request):  

        return render(request, 'adminapp/login.html')
    
    def post(self, request):
        storage = messages.get_messages(request)
        for message in storage:
            message = None
        scontact = request.POST.get('username')
        spassword = request.POST.get('password')
      
        try:
            checkusername = Admintbl.objects.get(username = scontact)
        except:
            checkusername = None   
                     
        if checkusername is not None:
            checkcontactpasswordboth = Admintbl.objects.filter(username=scontact,password=spassword).exists()
            if checkcontactpasswordboth:
                #loggedname = CustomerModel.objects.only('name').get(contactno=scontact)
                loggedname = Admintbl.objects.filter(username=scontact).values('username')
                request.session['CName'] =loggedname[0]['username']
                return redirect('adminapp:home')
            else:
                messages.info(request,'Invalid Password')                
        else:
            messages.info(request,'Invalid Username')

        return render(request,'adminapp/login.html') 


# def register(request):
#     if request.method == 'POST':
#         first_name = request.POST['first_name']
#         last_name = request.POST['last_name']
#         username = request.POST['username']
#         email = request.POST['email']
#         password = request.POST['password']
#         confirm_password = request.POST['confirm_password']

#         if password==confirm_password:
#             if User.objects.filter(username=username).exists():
#                 messages.info(request, 'Username is already taken')
#                 return redirect('adminapp:register')
#             elif User.objects.filter(email=email).exists():
#                 messages.info(request, 'Email is already taken')
#                 return redirect('adminapp:register')
#             else:
#                 user = User.objects.create_user(username=username, password=password, 
#                                         email=email, first_name=first_name, last_name=last_name)
#                 user.save()
#                 messages.info(request, 'New admin registered success!')
#                 return render(request, 'adminapp/register.html')
#         else:
#             messages.info(request, 'Both passwords are not matching')
#             return redirect('adminapp:register')
            

#     else:
#         if not request.user.is_authenticated:
#             return redirect('adminapp:login') 
#         return render(request, 'adminapp/register.html')

class ManageCity(View):
    def get(self, request,id=None,cityid=None):
        if request.session.get('CName') is None:
            return redirect('adminapp:login') 

        if cityid is not None:
            data = City.objects.get(pk = cityid)
            data.delete()
            cityid = None
            messages.info(request,'City Deleted Success!')
            return redirect('adminapp:city') 
        if id is not None:
            data = City.objects.get(pk = id)
            form = CityForm(instance  = data)   
        else:    
            form = CityForm()

        cityData = City.objects.all().order_by('-id')
        context={
            'form' : form,
            'citydata' : cityData
        }
        return render(request, 'adminapp/city.html',context)    

    def post(self, request,id=None):
        if 'btnreset' in request.POST and request.method == 'POST':
            form = CityForm()
            return redirect('adminapp:city')

        cityName = request.POST["cityName"]
        if City.objects.filter(cityName=cityName).exists():
            messages.info(request, 'This city is already taken!')
            return redirect('adminapp:city')

        if  id is not None:  # Update Record
            data = City.objects.get(pk = id)
            form = CityForm(request.POST ,instance  = data)
            messages.info(request,'City Updated Success!')
        else:               # Insert Record
            form = CityForm(request.POST)
            messages.info(request,'City Inserted Success!')
        form.save()
        return redirect('adminapp:city')

class ManageArea(View):
    def get(self, request, id=None, areaid=None):
        if request.session.get('CName') is None:
         return redirect('adminapp:login') 

        if areaid is not None:
            data = Area.objects.get(pk = areaid)
            data.delete()
            areaid = None
            messages.info(request,'Area Deleted Success!')
            return redirect('adminapp:area')   
              
        form = AreaForm()
        bindCity  = City.objects.all().order_by('-id')
        bindData = Area.objects.select_related("cityId").all().order_by('-id')
        if id is not None:
            data = Area.objects.get(pk = id)
            form = AreaForm(instance  = data)
            selectedCity = data.cityId
            context={
                'cityData' : bindCity,
                'form' : form,
                'areaData' : bindData,
                'selectedCity' : selectedCity
            }
        else:
            form = AreaForm()    
            context={
                'cityData' : bindCity,
                'form' : form,
                'areaData' : bindData
            }
        return render(request,'adminapp/area.html',context)

    def post(self, request, id=None):
        if 'btnreset' in request.POST and request.method == 'POST':
            form = AreaForm()
            return redirect('adminapp:area')
        if id is not None:
            data = Area.objects.get(pk = id)
            form = AreaForm(request.POST, instance  = data)
            messages.info(request,'Area Updated Success!')
        else:            
            form = AreaForm(request.POST)
            messages.info(request,'Area Inserted Success!')
        form.save()
        return redirect('adminapp:area')

def load_areasbyCity(request, cityid=None):
    if cityid is not None:
        city_id = cityid
        areas = Area.objects.filter(cityId=city_id).order_by('areaName')
        return areas
    else:     
        city_id = request.GET.get('city_id')
        areas = Area.objects.filter(cityId=city_id).order_by('areaName')
        return render(request, 'adminapp/citytoareaddl.html', {'arealist': areas})        

class ManageEmployee(View):
    def get(self, request, id=None, employeeid=None):
        if request.session.get('CName') is None:
           return redirect('adminapp:login') 
        
        if employeeid is not None:
            data = Employee.objects.get(pk = employeeid)
            data.delete()
            employeeid = None
            messages.info(request,'Employee Deleted Success!')
            return redirect('adminapp:employee')
               
        bindCity = City.objects.all().order_by('-id')
        bindData = Employee.objects.select_related("cityId").select_related("areaId").all().order_by('-id')
        if id is not None:
            data = Employee.objects.get(pk = id)
            form = EmployeeForm(instance = data)  
            selectedCity = data.cityId
            bindArea = load_areasbyCity(request,data.cityId)
            selectedArea = data.areaId
            context={
                'employeeData' : bindData,
                'cityData' : bindCity,
                'form' : form,
                'areaData' : bindArea,
                'selectedCity' : selectedCity,
                'selectedArea' : selectedArea
            }  
            return render(request, 'adminapp/employee.html',context)
        else:
            form = EmployeeForm()
            context={
                'employeeData' : bindData,
                'cityData' : bindCity,
                'form' : form
            }
            return render(request, 'adminapp/employee.html',context)
    def post(self, request, id =None):
        if 'btnreset' in request.POST and request.method == 'POST':
            form = EmployeeForm()
            return redirect('adminapp:employee')
        if id is not None:
            data = Employee.objects.get(pk = id)
            form = EmployeeForm(request.POST, instance  = data)
            messages.info(request,'Employee Updated Success!')
        else:            
            form = EmployeeForm(request.POST)
            messages.info(request,'Employee Inserted Success!')
        form.save()
        return redirect('adminapp:employee')



class EmployeeTask(View):
    def get(self, request):
        bindInvoiceNo  = CustomerOrders.objects.filter(active=0).all().values('invno').distinct()
        bindOrderProfile = CustomerOrders.objects.all().values('invno')
        data = CustomerOrders.objects.filter(invno = bindOrderProfile[0]['invno']).first()
        bindOrders = load_CustomerData(request,data.invno)
        bindEmployees = Employee.objects.all()
        SelectedInvoice = data.invno
     
        context={
            'InvoiceNo' : bindInvoiceNo,
            'OrderData' : bindOrders,
            'EmployeeData' : bindEmployees,
            'SelectedInvoiceNo' : SelectedInvoice
        }
        return render(request,'adminapp/employeetask.html',context)   

    def post(self, request):
        InvoiceData = CustomerOrders.objects.filter(invno = request.POST.get('invno')).values_list('id',flat=True)
                         
        for x in list(InvoiceData):
            # items = CustomerOrders.objects.filter(invno = request.session['invno']).all()
            # total_price = sum(items.values_list('price', flat=True))
            data = CustomerOrders.objects.get(pk = x)
            data.empid =request.POST.get('EmpId')
            data.active = 1
            data.save(update_fields= ['empid','active']) 
            

        bindInvoiceNo  = CustomerOrders.objects.filter(active=0).all().values('invno').distinct()
        bindOrderProfile = CustomerOrders.objects.all().values('invno')
        data = CustomerOrders.objects.filter(invno = bindOrderProfile[0]['invno']).first()
        bindOrders = load_CustomerData(request,data.invno)
        bindEmployees = Employee.objects.all()
        SelectedInvoice = data.invno
     
        context={
            'InvoiceNo' : bindInvoiceNo,
            'OrderData' : bindOrders,
            'EmployeeData' : bindEmployees,
            'SelectedInvoiceNo' : SelectedInvoice
        }
        messages.info(request,'Task is assign to staff!') 
        return render(request,'adminapp/employeetask.html',context)       
            

def load_CustomerData(request, invno=None):
  
    if invno is not None:
        inv_no = invno
        data = CustomerOrders.objects.select_related('productid').filter(invno = inv_no, active=0).all()
        return data
    else: 
        inv_no = request.GET.get('invno')
        if inv_no is not None:
            data = CustomerOrders.objects.select_related('productid').filter(invno=inv_no,active=0).all()
            return render(request, 'adminapp/loadcustomerdata.html', {'orderlist': data})        

class DeliveryOrderDetails(View):
    def get(self, request):
        data = CustomerOrders.objects.select_related('productid').all().order_by('-id')
        context={ 
            'DeliveredData' : data,

        }
        return render(request,'adminapp/successorders.html',context) 