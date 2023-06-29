from django.shortcuts import render,redirect
from django.http import HttpResponse
from app.models import Product,Cart,Order,Order_History,Profile
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Q
import datetime
import random
import razorpay
from django.contrib.auth import authenticate,login,logout
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages



# Create your views here.

def home(request):
    #data=Product.objects.all() #select *from ecommapp_product;
    data=Product.objects.filter(status=1) #fetch only active products
    #print(data)
    content={}
    content['products']=data
    return render(request,'index.html',content)


def register(request):
#fetch data from POST request 
    if request.method=="POST":
        content={}
        uname=request.POST['umail']
        mb=request.POST['umobile']
        upass=request.POST['upass']
        cpass=request.POST['cpass']
        
        # print(uname)
        # print(mb)
        # print(upass)
        # print(cpass)
        #validation
        if uname=='' or mb=='' or upass=='' or cpass=='':
            content['errmsg']="Field cannot be Empty"
        elif not(mb.isdigit() and len(mb)==10):
            content['errmsg']="Invaild mobile number. It must be 10 digits"                
        elif upass!=cpass:
                content['errmsg']="password and confirmed password didn't match"
        else:
            
            try:
                u=User.objects.create(username=uname,password=upass,email=uname,is_active=1,date_joined=datetime.datetime.now())
                u.set_password(upass)
                u.save()
                
            except Exception:
                content['errmsg']="Username Already Exists!!!"

            try:
                p=Profile.objects.create(uid=u,mobile=mb)
                # print(p)
                p.save()
            except Exception:
                content['errmsg']="Mobile Number Already Exists!!"
            
            if u and p:
                 url='/verifyscreen/'+str(u.id)
                 return redirect(url)
            
        return render(request,'register.html',content)
    else:
        return render(request,'register.html')
        
def user_login(request):
    if request.method=='POST':
        dataobj=AuthenticationForm(request=request,data=request.POST)
        #print(dataobj)
        if dataobj.is_valid():
            uname=dataobj.cleaned_data['username']
            upass=dataobj.cleaned_data['password']
            #print("Username:",uname)
            #print("password",upass)
            u=authenticate(username=uname,password=upass)
            #print(u)
            if u:
                login(request,u)
                return redirect("/")
    else:
        logobj=AuthenticationForm()
        content={}
        content['loginform']=logobj
        return render(request,'login.html',content)
    

def verifyscreen(request,rid):
    u=User.objects.filter(id=rid)
    r=u[0].email
    otp=str(random.randrange(1000,9999))
    msg="OTP for Email Verification: "+str(otp)
    s="Email verification" 
    request.session[r]=otp
    send_mail(
            s,
            msg,
            settings.EMAIL_HOST_USER,
            [r],
            fail_silently=False,
            )  
    content={}
    content['user_id']=rid
     #store otp in the database
    return render(request,'verifyscreen.html',content)


def verifyotp(request,rid):
    otp=request.POST['uotp']
    u=User.objects.filter(id=rid)
    uemail=u[0].email
    sess_otp=request.session[uemail]
    # print("session otp:",sess_otp)
    # print("User otp:",otp)
    # print("userid:",rid)
    if int(otp)==int(sess_otp):
        return render(request,'gmailsuccess.html')

def user_logout(request):
    logout(request)
    return redirect('/login')
    
def product_details(request,pid):
    #print("Id of the product",pid)
    data=Product.objects.filter(id=pid)
    content={}
    content['products']=data
    return render(request,'product_details.html',content)

def reuse(request):
    return render(request,'base.html')

def addproduct(request):
    #print("method is:",request.method)
    if request.method=="POST":
        # print("insert record in database")
        # insert record in database table product
        n=request.POST['pname']
        c=request.POST['pcat']
        amt=request.POST['pprice']
        s=request.POST['status']
        #print(n)
        #print(cat)
        #print(amt)
        #print(s)
        p=Product.objects.create(name=n,cat=c,price=amt,status=s)
        #print(p)
        p.save()
        #return render(request,'addproduct.html')
        return redirect('/addproduct')
    else:
        #print("in else part")
        p=Product.objects.all()
        content={}
        content['products']=p
        return render(request,'addproduct.html',content)

def delproduct(request,rid):
   # print("id to be deleted:",rid)
   p=Product.objects.filter(id=rid)
   p.delete()
   return redirect('/addproduct')

def editproduct(request,rid):
    #print("Id to be deleted",rid)
    if request.method=='POST':
        upname=request.POST['pname']
        ucat=request.POST['pcat']
        uprice=request.POST['pprice']
        ustatus=request.POST['status']
        
        #print(upname)
        #print(ucat)
        #print(uprice)
        #print(ustatus)
        p=Product.objects.filter(id=rid)
        p.update(name=upname,cat=ucat,price=uprice,status=ustatus)
        return redirect('/addproduct')


     #return redirect('/editproduct')
    else:
        p=Product.objects.filter(id=rid)
        content={}
        content['products']=p
        return render(request,'editproduct.html',content)

def sort(request,sv):
    if sv=='0':
       param='price'
        
    else:
         param='-price'
    data=Product.objects.order_by(param).filter(status=1)
    content={}
    content['products']=data
    return render(request,'index.html',content)

#filters

def catfilter(request,catv):
    q1=Q(cat=catv)
    q2=Q(status=1)
    data=Product.objects.filter(q1 & q2)
    content={}
    content['products']=data
    return render(request,'index.html',content)

def pricefilter(request,pv):
    q1=Q(status=1)
    if pv=='0':
        q2=Q(price__lt=5000)
    else:
        q2=Q(price__gte=5000)

    data=Product.objects.filter(q1 & q2)
    content={}
    content['products']=data
    return render(request,'index.html',content)

def pricerange(request):
    
    low=request.GET['min']
    high=request.GET['max']
    #print(low)
    #print(high)
    q1=Q(status=1)
    q2=Q(price__gte=low)
    q3=Q(price__lte=high)

    data=Product.objects.filter(q1 & q2 & q3)
    content={}
    content['products']=data
    return render(request,'index.html',content)
    
def addtocart(request,pid):
    
    if request.user.is_authenticated:
        userid=request.user.id
        #check whether user already added product in the cart
        q1=Q(pid=pid)
        q2=Q(uid=userid)
        c=Cart.objects.filter(q1 & q2)#0 or 1 or more than 1
        p=Product.objects.filter(id=pid)
        content={}
        content['products']=p

        if c:
            content['msg']="Product Already Exists in the cart"
            return render(request,'product_details.html',content)
        else:
            #print("User ID:",uid)
            #print("Product Id",pid)
            u=User.objects.filter(id=userid)
            #print(u[0])
            #print(p[0])
            c=Cart.objects.create(uid=u[0],pid=p[0])
            c.save()
            content['success']="Product Added in Cart"
            return render(request,'product_details.html',content)

            #return HttpResponse("product added to card")
            #return HttpResponse("userid and product id fetched")
    else:
        return redirect('/login')

def user_logout(request):
    logout(request)
    return redirect('/login')

def viewcart(request):
    userid=request.user.id
    c=Cart.objects.filter(uid=userid)
    #print(c)
    #print(c[0])
    #print(c[0].pid)
    #print(c[0].uid)
    #calculatetortalproduct price 
    sum=0
    for x in c:
        
        #print(x.qty)
        #print(x.pid.price)
        sum=sum+(x.qty*x.pid.price)
    print("Total Product price",sum)

    content={}
    content['products']=c
    content['nitems']=len(c)
    content['total']=sum
    print(len(c))
    return render(request,'viewcart.html',content)

def changeqty(request,pid,f):
    content={}
    c=Cart.objects.filter(pid=pid)
    if f== '1':
        x=c[0].qty+1  #c.qty+=1
    else:
        x=c[0].qty-1

    if x>0:
        c.update(qty=x)
        
    return redirect('/viewcart')

def placeorder(request):
    oid=random.randrange(1000,9999)
    #print(oid)
    user_id=request.user.id 
    c=Cart.objects.filter(uid=user_id)#user_id=5
    #print(c)
    for x in c:
        o=Order.objects.create(order_id=oid,pid=x.pid,uid=x.uid,qty=x.qty)
        o.save()
        x.delete()
    o=Order.objects.filter(uid=user_id)
    sum=0
    for x in o:
        sum=sum+(x.qty*x.pid.price)

    content={}
    content['products']=o
    content['nitems']=len(o)
    content['total']=sum
    return render(request,'placeorder.html',content)

def makepayment(request):
    userid=request.user.id
    client = razorpay.Client(auth=("rzp_test_gbyB82ghkyZT1k", "dlVi7mneKiix5IJxtt9jvVZs"))
    o=Order.objects.filter(uid=userid)
    sum=0
    oid=str(o[0].id)
    for x in o:
        sum=sum+(x.qty*x.pid.price)
    sum=sum*100 #conversion of Rs into paise 
    data = { "amount": sum, "currency": "INR", "receipt":oid }
    payment = client.order.create(data=data)
    print(payment)
    content={}
    content['payment']=payment
    return render(request,"pay.html",content)


def storedetails(request):
    pay_id=request.GET['pid']
    order_id=request.GET['oid']
    sign=request.GET['sign']
    userid=request.user.id
    u=User.objects.filter(id=userid)
    oh=Order_History.objects.create(order_id=order_id,pay_id=pay_id,sign=sign,uid=u[0])

    # print(u[0])
    # print(u[0].email)
    # print(pay_id)
    # print(order_id)
    # print(sign)
    email=u[0].email
    msg="Order Placed Successfully.Details are Payment Id:"+pay_id+"and Order Id is:"+order_id
    send_mail(
        "Order Status-The Decor Kart",
         msg,
        settings.EMAIL_HOST_USER,
        ["shraddhanangare963@gmail.com"],
        fail_silently=False,
    )
    
    return render(request,"final.html")