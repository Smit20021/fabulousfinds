from django.shortcuts import render,redirect
from django.views  import View
from adminapp.models import Employee
from adminapp.forms import EmployeeForm
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.sessions.models import Session
from giftkeepers.models import CustomerOrders,CheckoutOrders
# Create your views here.

class EmployeeLogout(View):
    def get(self, request):
        storage = messages.get_messages(request)
        for message in storage:
            message = None
        storage.used = False
        logout(request)
        Session.objects.all().delete()
       
        return render(request, 'employee/login.html')


def load_CustomerData(request, invno=None):
  
    if invno is not None:
        inv_no = invno
        data = CustomerOrders.objects.select_related('productid').filter(invno = inv_no,active=1).all()
        return data
    else: 
        inv_no = request.GET.get('invno')
        if inv_no is not None:
            data = CustomerOrders.objects.select_related('productid').filter(invno=inv_no,active=1).all()
            return render(request, 'employee/loadcustomerdata.html', {'orderlist': data})        

def load_CustomerPersonalInfo(request, invno=None):
    if invno is not None:
        print(invno)
        inv_no = invno
        data = CheckoutOrders.objects.filter(invno=inv_no).all()
        return data
    else: 
        inv_no = request.GET.get('invno')
        if inv_no is not None:
            data = CheckoutOrders.objects.filter(invno=inv_no).all()
            return render(request, 'employee/loadcustomerpersonal.html', {'personallist': data})        


class ManageTask(View):
    def get(self, request):
      
        bindInvoiceNo  = CustomerOrders.objects.filter(empid=request.session.get('Cid'),active=1).all().values('invno').distinct()
        bindOrderProfile = CustomerOrders.objects.all().values('invno')
        
        data = CustomerOrders.objects.filter(invno = bindOrderProfile[0]['invno']).first()
       
        bindOrders = load_CustomerData(request,data.invno)
        SelectedInvoice = data.invno
     
        if bindInvoiceNo.exists():
            bindCustomerPersonal = load_CustomerPersonalInfo(request,bindInvoiceNo[0]['invno'])

            context={
                'InvoiceNo' : bindInvoiceNo,
                'OrderData' : bindOrders,
                'SelectedInvoiceNo' : SelectedInvoice,
                'CustomerPersonal' : bindCustomerPersonal
            }
        else:
            context={
                'InvoiceNo' : bindInvoiceNo,
                'OrderData' : bindOrders,
                'SelectedInvoiceNo' : SelectedInvoice
               
            }
        return render(request,'employee/managework.html',context)
    # def get(self, request):
    #     bindInvoiceNo  = CustomerOrders.objects.filter(empid=request.session.get('Cid'),active=1).all().values('invno').distinct()
    #     bindOrderProfile = CustomerOrders.objects.all().values('invno')
    #     data = CustomerOrders.objects.filter(invno = bindOrderProfile[0]['invno']).first()
    #     bindOrders = load_CustomerData(request,data.invno)
    #     SelectedInvoice = data.invno
    #     bindCustomerPersonal = load_CustomerPersonalInfo(request,bindInvoiceNo[0]['invno'])

    #     context={
    #         'InvoiceNo' : bindInvoiceNo,
    #         'OrderData' : bindOrders,
    #         'SelectedInvoiceNo' : SelectedInvoice,
    #         'CustomerPersonal' : bindCustomerPersonal
    #     }
    #     return render(request,'employee/managework.html',context)   

    def post(self, request):
        InvoiceData = CustomerOrders.objects.filter(invno = request.POST.get('invno'),active=1).values_list('id',flat=True)
                         
        for x in list(InvoiceData):
            print(x)
            data = CustomerOrders.objects.get(pk = x)
            data.active = 2
            data.save(update_fields= ['active']) 
            

        bindInvoiceNo  = CustomerOrders.objects.filter(empid=request.session.get('Cid'),active=1).all().values('invno').distinct()
        bindOrderProfile = CustomerOrders.objects.all().values('invno')
        data = CustomerOrders.objects.filter(invno = bindOrderProfile[0]['invno']).first()
        bindOrders = load_CustomerData(request,data.invno)
        SelectedInvoice = data.invno
     
        context={
            'InvoiceNo' : bindInvoiceNo,
            'OrderData' : bindOrders,
            'SelectedInvoiceNo' : SelectedInvoice
        }
        messages.info(request,'Order is delivered success!') 
        return render(request,'employee/managework.html',context)       
            

class Home(View):
    def get(self, request):
        print(request.session.get('CName'))
        if request.session.get('CName') is None:
            return redirect('employee:emplogin')
        return render(request, 'employee/index.html')
    def post(self, request):
        pass

class EmployeeLogin(View):
    def get(self, request):
        storage = messages.get_messages(request)
        for message in storage:
            message = None
        storage.used = False
        form = EmployeeForm()
        context={
            'form' : form
        }
        return render(request, 'employee/login.html',context)

    def post(self, request):
        scontact = request.POST.get('contactno')
        spassword = request.POST.get('password')
        print(scontact, spassword)
        try:
            checkusername = Employee.objects.get(contactNo = scontact)
        except:
            checkusername = None   

                  
        if checkusername is not None:
            checkcontactpasswordboth = Employee.objects.filter(contactNo=scontact,password=spassword).exists()
            if checkcontactpasswordboth:
                #loggedname = CustomerModel.objects.only('name').get(contactno=scontact)
                loggedname = Employee.objects.filter(contactNo=scontact).values('id','name')
                request.session['CName'] =loggedname[0]['name']
                request.session['Cid'] =loggedname[0]['id']
               
                return redirect('employee:home')
            else:
                messages.info(request,'Invalid Password')                
        else:
            messages.info(request,'Invalid Contact Number')

        return render(request,'employee/login.html')       
