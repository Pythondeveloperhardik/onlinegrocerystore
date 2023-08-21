from django.shortcuts import render,HttpResponse,redirect
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login , logout

from gapp.models import Product,Cart,Order,contactrecords
from django.db.models import Q
from django.http import HttpResponseServerError
import random












# Create your views here.

def home(request):
    context={}
    #kid=request.user.id
    #print("id of logged in user:",kid)
    #print('result',request.user.is_authenticated) #this session_login authentication notice for privcy purpose
    
    
               #-----------#
  
   #this code filiter all active product of backend means backend la jepan active product ahet te user la display karte hi queary ok



    p=Product.objects.filter(is_active=True)
    context['availableProductinfo']=p
    return render(request,'index.html',context)
                #-----------#



def product_detail(request,pid):

    context={}
    k=Product.objects.filter(id=pid)
    context['availableProductinfo']=k
    return render(request,'product_details.html',context)   

                #-------------------- 

def p_cart(request):
    return render(request,'cart.html')

                 #----------------------

def place_order(request):
    #return render(request,'placeorder.html')
    userid=request.user.id
    c=Cart.objects.filter(uid=userid)
    oid=random.randrange(1000,9999)
    for x in c:
        o=Order.objects.create(order_id=oid,pid=x.pid,uid=x.uid,qty=x.qty)
        o.save()
        #x.delete()


    orders=Order.objects.filter(uid=request.user.id)

    np=len(orders)
    s=0
    for x in orders:
        #print(x)
        #print(x.pid.price)
        #s=s+x.pid.price*x.qty  #s=0+2200=2200 | s=2200+600=2800
        s=s+x.pid.price*x.qty  #s=0+2200=2200 | s=2200+600=2800

     
      # Define the discount percentage based on the cart total value
    if s >= 1000:
        discount_percentage = 30  # 10% discount for cart value >= 1000
    else:
        discount_percentage = 15  # 5% discount for cart value < 1000

    # Calculate the discount amount based on the cart total and discount percentage
    discount_amount = (discount_percentage / 100) * s

    # Calculate the discounted total
    discounted_total = s - discount_amount


    context={}
    context['availableProductinfo']=orders
    context['total']=s
    context['discounted_total'] = discounted_total
    context['discount_amount'] = discount_amount
    context['quantity']=np


    return render(request,'placeorder.html',context)    
    

#############################################################################
                 #register start

def register(request):

    context={}

    if request.method=="POST":
        uname=request.POST['uname']
        upass=request.POST['upass']
        ucpass=request.POST['ucpass']

        if uname=="" or upass=="" or ucpass=="":  #if user not inserted any information then what ? < so this is what happen then ok
            context['errmsg']="field cannot be empty"
            return render(request,'register.html',context)
        
        elif upass!=ucpass:
            context['errmsg']="Password Must Be Same"
            return render(request,'register.html',context)



        else:
            try:
               u=User.objects.create(username=uname,email=uname)
               u.set_password(upass)# this is very imp < this set ur password to be not visible to developer means increapted format
               u.save()
               context['success']="User Created Succefully"    
               return render(request,'register.html',context)
            except Exception:
                context['errmsg']='USER ALREADY EXISTS'
                return render(request,'register.html',context)
         

    
    else:

        return render(request,'register.html')
    
      
                #register ends
    
 #############################################################################   

def contact(request):
    if request.method=='GET':
        return render(request,'contact.html')
    
    else:
        n=request.POST['fname']
        m=request.POST['fnumber']
        e=request.POST['femail']
        msg=request.POST['fmsg']


        r=contactrecords.objects.create(name=n,mobile=m,email=e,message=msg)
        r.save()

        return redirect('/contact')
    
    #return render(request,'contact.html')
    


def about(request):
    return render(request,'about.html')



 #############################################################################
 #                                login start   

def u_login(request):
    context={}
    if request.method=="POST":
        uname=request.POST['uname']
        upass=request.POST['upass']

        if uname=='' or upass=='':
            context["errmsg"]="Filed cannot be empty"
            return render(request,'login.html',context)
        else:
            u=authenticate(username=uname,password=upass)
            if u is not None:
               
               #####################
               # login session part

               login(request,u)#  // start login function and store id of authenticated user into django_session table
               
               ####################


               return redirect('/home')
            else:
                context["errmsg"]="user name and password incorrect"
                return render(request,'login.html',context)


    else:
        return render(request,'login.html')
    
                                   # LOGIN END
     #############################################################################   



def u_logout(request):
    logout(request)
    return redirect('/home')

def catfilter(request,cdv):
    context={}
    c1=Q(is_active=True)
    c2=Q(cat=cdv)

    p=Product.objects.filter(c1 & c2)
    context['availableProductinfo']=p

    return render(request,'index.html',context)



def sort(request,sortvalue):
    context={}
    if sortvalue=='0':
        col='price'
    else:
        col='-price'


    p=Product.objects.filter(is_active=True).order_by(col)
    context['availableProductinfo']=p
    return render(request,'index.html',context)        




def range(request):
    min_value = request.GET.get('min')
    max_value = request.GET.get('max')

    # Check if both min_value and max_value are provided
    if min_value is not None and max_value is not None:
        try:
            min_value = int(min_value)
            max_value = int(max_value)
        except ValueError:
            # Handle the case when min_value or max_value is not a valid integer
            error_message = "Please enter valid numbers for min and max values."
            context = {
                'error_message': error_message
            }
            return render(request, 'index.html', context)

        c1 = Q(price__gte=min_value)
        c2 = Q(price__lte=max_value)
        c3 = Q(is_active=True)

        p = Product.objects.filter(c1 & c2 & c3)
        context = {
            'availableProductinfo': p
        }
        return render(request, 'index.html', context)
    else:
        # Handle the case when either min_value or max_value is missing
        min_value=''
        max_value=''
        error_message = "Please enter both min and max values."
        context = {
            'error_message': error_message
        }
        return render(request, 'index.html', context)
    

    #---------------
#def addtocart(request,pid):
    if request.user.is_authenticated:#means jya vyakti ne login kela ahe tech add to cart karu shaktil


        userid=request.user.id

        #USER ID DEFINATION : 
        #In Django, the request.user object represents the currently logged-in user, and request.user.id gives you the user ID of the authenticated user. 
        # The user ID is the primary key of the user in the auth_user table, which is a default table created by Django's authentication system.


        #print(pid)
        #print(userid)
        u=User.objects.filter(id=userid)
        #print(u[0])
        p=Product.objects.filter(id=pid)
        #print(u[0])

        c=Cart.objects.create(uid=u[0],pid=p[0])
        c.save()

        cd=Cart.objects.filter(uid=userid)

        context={}
        context['availableProductinfo']=cd
        return render(request,'cart.html',context)

    else:
        return redirect('/login')    
    
def addtocart(request,pid):
    
    if request.user.is_authenticated:
        userid=request.user.id 
        #print(pid)
        #print(userid)
        q1=Q(uid=userid)
        q2=Q(pid=pid)
        pcount=Cart.objects.filter(q1 & q2)
        l=len(pcount)
        u=User.objects.filter(id=userid)
        #print(u[0])
        p=Product.objects.filter(id=pid)
        #print(p[0])
        context={}
        context['availableProductinfo']=p

        if l==0:
            c=Cart.objects.create(uid=u[0],pid=p[0])
            c.save()
            context['success']="Product Added in the Cart!!"

        else:
            context['msg']="Product already Exists in the cart!!"
            
        return render(request,'product_details.html',context)
    else:
        return redirect('/login')




def viewcart(request):
    userid=request.user.id
    c=Cart.objects.filter(uid=request.user.id)
    np=len(c)
    s=0
    for x in c:
        #print(x)
        #print(x.pid.price)
        #s=s+x.pid.price*x.qty  #s=0+2200=2200 | s=2200+600=2800
        s=s+x.pid.price*x.qty  #s=0+2200=2200 | s=2200+600=2800

     
      # Define the discount percentage based on the cart total value
    if s >= 1000:
        discount_percentage = 30  # 10% discount for cart value >= 1000
    else:
        discount_percentage = 15  # 5% discount for cart value < 1000

    # Calculate the discount amount based on the cart total and discount percentage
    discount_amount = (discount_percentage / 100) * s

    # Calculate the discounted total
    discounted_total = s - discount_amount





     

    #print(c)
    #print(c[0].uid)
    #print(c[0].uid.is_staff)
    #print(c[0].pid.name)
    context={}
    #context['n']=np
    context['availableProductinfo']=c
    context['total']=s
    context['discounted_total'] = discounted_total
    context['discount_amount'] = discount_amount
    context['quantity']=np
    return render(request,'cart.html',context)        


def remove(request,cid):
    c=Cart.objects.filter(id=cid)
    c.delete()
    return redirect('/viewcart')



def viewcart_two(request):
    userid=request.user.id
    c=Cart.objects.filter(uid=request.user.id)
    np=len(c)
    s=0
    for x in c:
        #print(x)
        #print(x.pid.price)
        #s=s+x.pid.price*x.qty  #s=0+2200=2200 | s=2200+600=2800
        s=s+x.pid.price*x.qty  #s=0+2200=2200 | s=2200+600=2800

     
      # Define the discount percentage based on the cart total value
    if s >= 1000:
        discount_percentage = 30  # 10% discount for cart value >= 1000
    else:
        discount_percentage = 15  # 5% discount for cart value < 1000

    # Calculate the discount amount based on the cart total and discount percentage
    discount_amount = (discount_percentage / 100) * s

    # Calculate the discounted total
    discounted_total = s - discount_amount





     

    #print(c)
    #print(c[0].uid)
    #print(c[0].uid.is_staff)
    #print(c[0].pid.name)
    context={}
    #context['n']=np
    context['availableProductinfo']=c
    context['total']=s
    context['discounted_total'] = discounted_total
    context['discount_amount'] = discount_amount
    context['quantity']=np
    return render(request,'placeorder.html',context)        


def remove_place(request,cid):
    c=Cart.objects.filter(id=cid)
    c.delete()
    return redirect('/viewcart_two')







#------------------------------------------



def updateqty(request,qv,cid):

    c=Cart.objects.filter(id=cid)

    


    if qv=="1":
        t=c[0].qty+1
        c.update(qty=t)
    else:
        if c[0].qty>1:
            t=c[0].qty-1
            c.update(qty=t)
        else:
            # If quantity becomes zero, delete the cart item from the database
            c.delete()


    return redirect('/viewcart')

#---------------------------------------------


def makepayment(request):
    return HttpResponse("in make payment section")















    





    










    






