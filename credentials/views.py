from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.contrib import messages
from .models import userprofile,ownerprofile
from django.contrib.auth.decorators import login_required

# Create your views here.
def userlogin(request):
    if request.method=='POST':
        email=request.POST['email']
        pswd=request.POST['pswd']
        
        user=auth.authenticate(username=email,password=pswd)
        print(user)
        if user is not None:
            auth.login(request,user)
            messages.success(request,'login success')
            return redirect('/')
        else:
            messages.info(request,'invalid credentials')
            return redirect('userlogin')

    return render(request,'userlogin.html')

def userregister(request):
    if request.method=='POST':
        name=request.POST['name']
        email=request.POST['email']
        pasword=request.POST['pswd']
        try:
            if User.objects.filter(username=email).exists():
                messages.info(request,'email already registered')
                return redirect('userregister')
            else:    
                user=User.objects.create_user(username=email,password=pasword)  
                profile=userprofile.objects.create(name=name,email=email) 
                user.save()
                profile.save()
                return redirect('userlogin')
        except:
            messages.info(request,'internal server error')
            return redirect('userregister')            

    return render(request,'userregister.html')


def userlogout(request):
    auth.logout(request)
    
    return redirect('/')

def ownerlogout(request):
    auth.logout(request)
   
    return redirect('ownerlogin')

def ownerlogin (request):
    if request.method=='POST':
        email=request.POST['email']
        pswd=request.POST['pswd']
        
        user=auth.authenticate(username=email,password=pswd)
        print(user)
        if user is not None:
            auth.login(request,user)
            messages.success(request,'login success')

            return redirect('ownerhome')

        else:
            messages.info(request,'invalid credentials')
            return redirect('ownerlogin')
        
    return render(request,'ownerlogin.html')   

def ownerregister (request):
    if request.method=='POST':
        name=request.POST['name']
        email=request.POST['email']
        phone=request.POST['phone']
        pasword=request.POST['pswd']
       
        try:
            if User.objects.filter(username=email).exists():
                messages.info(request,'email already registered')
                return redirect('ownerregister')
            else:    
                user=User.objects.create_user(username=email,password=pasword)  
                profile=ownerprofile.objects.create(name=name,email=email,phone=phone) 
                user.save()
                profile.save()
                return redirect('ownerlogin')
        except:
            messages.info(request,'internal server error')
            return redirect('ownerregister')          
    return render(request,'ownerregister.html')