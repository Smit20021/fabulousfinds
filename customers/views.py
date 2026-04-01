from django.shortcuts import render, redirect
from django.views import View
from giftkeepers.models import Product, Giftkeeper
from adminapp.models import City,Area
from customers.forms import CustomersForm,OrderForm
from django.contrib import messages
from django.contrib.auth import logout
from giftkeepers.models import Customertbl,CustomerOrders
from giftkeepers.forms import CheckoutForm
from django.contrib.sessions.models import Session

# Create your views here.
class ShowShopes(View):
    def get(self, request):
        storage = messages.get_messages(request)
        for message in storage:
            message = None
        storage.used = False
        bindShopes = Giftkeeper.objects.all().order_by('-id')
        context={
            'shopesData' : bindShopes
        }
        if request.session.get('InvNo') is None:
            return render(request, 'customers/index.html', context)    
        else:    
            TotalCost = CustomerOrders.objects.filter(invno = request.session['InvNo']).first()
            if TotalCost is None:
                request.session['totalamount'] = 0
            else:
                request.session['totalamount'] =TotalCost.totalcost
        return render(request, 'customers/index.html', context)    
        # else:
        #     return render(request, 'customers/login.html')    
       

class ShowCartItems(View):
    def get(self, request,id=None):
        storage = messages.get_messages(request)
        for message in storage:
            message = None
        storage.used = False
        CartItems = CustomerOrders.objects.filter(invno = request.session['InvNo']).count()
        request.session['CartItems'] = CartItems 
        bindProducts = CustomerOrders.objects.select_related('productid').filter(invno = request.session['InvNo']).all()
      
        context={
            'productData' : bindProducts          
        }
        TotalCost = CustomerOrders.objects.filter(invno = request.session['InvNo']).first()
        if TotalCost is None:
            request.session['totalamount'] = 0
        else:    
            request.session['totalamount'] =TotalCost.totalcost
        return render(request, 'customers/cart.html', context)

class ShowProductsByShopes(View):
    def get(self, request,id=None):
        storage = messages.get_messages(request)
        for message in storage:
            message = None
        storage.used = False
        if request.session.get('InvNo') is not None:
            CartItems = CustomerOrders.objects.filter(invno = request.session['InvNo'] ).count()
            request.session['CartItems'] = CartItems 
           
        bindProducts = Product.objects.all().filter(giftKeeperId_id = id)
        context={
            'productData' : bindProducts          
        }
      
        return render(request, 'customers/show_products.html', context)
    def post(self, request, id=None):
        PId = request.POST.get('pid')
        gId = request.POST.get('gid')
        Price = request.POST.get('price')
        checkExistItems = CustomerOrders.objects.filter(invno = request.session['InvNo'],productid_id=PId).exists()
        if checkExistItems:
            messages.success(request,'Product is already added in the Cart!')
            return redirect('customers:showproducts',id=gId)
        else:
        
            form = OrderForm(request.POST)
                   
            if form.is_valid():
                data = form.save(commit=False)
                data.invno = request.session['InvNo']
                data.customerid_id=request.session['Cid']
                data.giftkeeperid_id=gId
                data.productid_id = PId
                data.qty = 1
                data.price = Price
                data.totalprice  = (data.qty * data.price)
                data.status = 0
                data.active = 0
                data.empid = 0
                data.save()
              
                CartData = CustomerOrders.objects.filter(invno = request.session['InvNo']).values_list('id',flat=True)
                         
                for x in list(CartData):
                    items = CustomerOrders.objects.filter(invno = request.session['InvNo']).all()
                    total_price = sum(items.values_list('price', flat=True))
                    UpdateCost = CustomerOrders.objects.get(pk = x)
                    UpdateCost.totalcost =total_price
                    UpdateCost.save(update_fields= ['totalcost'])    
               
                  
            messages.success(request,'Product is Added to Cart!')
            return redirect('customers:showproducts',id=gId)


class RemoveItems(View):
    def get(self, request,id=None):
        if id is not None:
            if CustomerOrders.objects.filter(pk = id).exists():
                data = CustomerOrders.objects.get(pk = id)
                data.delete()
                CartDataItem = CustomerOrders.objects.filter(invno = request.session['InvNo']).values_list('id',flat=True)
                for x in list(CartDataItem):
                    items = CustomerOrders.objects.filter(invno = request.session['InvNo']).all()
                    total_price = sum(items.values_list('totalprice', flat=True))
                    UpdateCost = CustomerOrders.objects.get(pk = x)
                    UpdateCost.totalcost =total_price
                    UpdateCost.save(update_fields= ['totalcost'])  

                CartItems = CustomerOrders.objects.filter(invno = request.session['InvNo']).count()
                request.session['CartItems'] = CartItems 
                bindProducts = CustomerOrders.objects.select_related('productid').filter(invno = request.session['InvNo']).all()
                TotalCost = CustomerOrders.objects.filter(invno = request.session['InvNo']).first()
              
                if TotalCost is None:
                    request.session['totalamount'] = 0
                else:
                    request.session['totalamount'] =TotalCost.totalcost
                context={
                   'productData' : bindProducts          
                }
                messages.info(request,'Product is Removed!')
                return render(request, 'customers/cart.html', context)
            else:    
                return redirect('customers:showcarts')

class CheckOut(View):
    def get(self, request):
        storage = messages.get_messages(request)
        for message in storage:
            message = None
        storage.used = False
        return render(request, 'customers/checkout.html')
    def post(self, request):
        form = CheckoutForm(request.POST)
                   
        if form.is_valid():
            data = form.save(commit=False)
            data.invno = request.session['InvNo']
            data.name=request.POST.get('name')
            data.contact=request.POST.get('contact')
            data.landmark = request.POST.get('landmark')
            data.pmode  = request.POST.get('pmode')
            data.save()
                
        return redirect('customers:customerlogout')  

class PlusMinusItems(View):
  
    def post(self, request):
  
        data = CustomerOrders.objects.filter(invno = request.session['InvNo']).filter(productid_id=request.POST.get('product'))
       
        if(data and request.POST.get('remove')=='True'):

            CartData = CustomerOrders.objects.get(invno = request.session['InvNo'],productid_id=request.POST.get('product'))
           
            if(int(request.POST.get('qty'))==1):
                CartData.qty  = 1
            else:
                CartData.qty  = CartData.qty - 1

              
            CartData.totalprice  = int(request.POST.get('tprice')) * int(CartData.qty)
           
            CartData.save(update_fields= ['qty','totalprice'])  
        else:    
            CartData = CustomerOrders.objects.get(invno = request.session['InvNo'],productid_id=request.POST.get('product'))
            print(CartData.price)
            CartData.qty  = CartData.qty + 1
            print(int(request.POST.get('tprice'))* int(CartData.qty))
            CartData.totalprice  = int(request.POST.get('tprice')) * int(CartData.qty)
            CartData.save(update_fields= ['qty','totalprice'])     
        
        CartDataItem = CustomerOrders.objects.filter(invno = request.session['InvNo']).values_list('id',flat=True)
        for x in list(CartDataItem):
            items = CustomerOrders.objects.filter(invno = request.session['InvNo']).all()
            total_price = sum(items.values_list('totalprice', flat=True))
            UpdateCost = CustomerOrders.objects.get(pk = x)
            UpdateCost.totalcost =total_price
            UpdateCost.save(update_fields= ['totalcost'])   
        
        CartItems = CustomerOrders.objects.filter(invno = request.session['InvNo']).count()
        request.session['CartItems'] = CartItems 
        
        bindProducts = CustomerOrders.objects.select_related('productid').filter(invno = request.session['InvNo']).all()
        
        TotalCost = CustomerOrders.objects.filter(invno = request.session['InvNo']).first()
        request.session['totalamount'] =TotalCost.totalcost
        context={
            'productData' : bindProducts          
        }
        return render(request, 'customers/cart.html', context)
       

def About(request):
     return render(request, 'customers/about.html')

def Contact(request):
     return render(request, 'customers/contact.html')

class CustomerLogout(View):
    def get(self, request):
        storage = messages.get_messages(request)
        for message in storage:
            message = None
        storage.used = False
        logout(request)
        Session.objects.all().delete()
        invoice = increment_invoice_number()
        return render(request, 'customers/index.html')

def increment_invoice_number():
    last_invoice = CustomerOrders.objects.all().order_by('id').last()
    if not last_invoice:
         return 'INV1'
    invoice_no = last_invoice.invno

    invoice_int = int(invoice_no.split('INV')[-1])
    new_invoice_int = invoice_int + 1
    new_invoice_no = 'INV' + str(new_invoice_int)
    return new_invoice_no

class CustomerLogin(View):
    def get(self,request):
        storage = messages.get_messages(request)
        for message in storage:
            message = None
        storage.used = False
        form = CustomersForm()
        context={
            'form' : form
        }
        return render(request, 'customers/login.html',context)

    def post(self, request):    
        invoice = increment_invoice_number()
        scontact = request.POST.get('contactno')
        spassword = request.POST.get('password')
      
        try:
            checkusername = Customertbl.objects.get(contactNo = scontact)
        except:
            checkusername = None   
                     
        if checkusername is not None:
            checkcontactpasswordboth = Customertbl.objects.filter(contactNo=scontact,password=spassword).exists()
            if checkcontactpasswordboth:
                #loggedname = CustomerModel.objects.only('name').get(contactno=scontact)
                loggedname = Customertbl.objects.filter(contactNo=scontact).values('id','name')
                request.session['CName'] =loggedname[0]['name']
                request.session['Cid'] =loggedname[0]['id']
                request.session['InvNo'] =invoice
                print(invoice)
                return redirect('customers:home')
            else:
                messages.info(request,'Invalid Password')                
        else:
            messages.info(request,'Invalid Contact Number')

        return render(request,'customers/login.html')    
   

class CustomerRegistration(View):
    def get(self,request):
        storage = messages.get_messages(request)
        for message in storage:
            message = None
        storage.used = False
        citylist = City.objects.all().order_by('-id')
        form = CustomersForm()
        context ={
                'form': form,
                'CityData' : citylist,
           
        }    
        return render(request,'customers/register.html',context)
              
    def post(self, request):
        form = CustomersForm(request.POST)
        if form.is_valid():
         
            form.save()
            form = CustomersForm()
            messages.info(request,'Registration Success!')            
        return redirect('customers:login')  

def load_areasbyCity(request):
  
    city_id = request.GET.get('city_id')
    print(city_id)
    #request.GET.get('cityid')
    areas = Area.objects.filter(cityId_id=city_id).order_by('areaName')
    return render(request, 'customers/citytoareaddl.html', {'arealist': areas})        

class CustomerHistory(View):
    def get(self, request):
        data = CustomerOrders.objects.select_related('productid').filter(customerid_id=request.session.get('Cid')).all().order_by('-id')
        context={ 
            'DeliveredData' : data,

        }
        return render(request,'customers/orderhistory.html',context) 


