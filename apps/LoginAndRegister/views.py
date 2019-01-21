from django.shortcuts import render,redirect
from django.urls import reverse
from django.contrib import messages
from .models import User
# Create your views here.

def home(request):

    return render(request,'logAndreg/home.html')

def register(request):
     
    return render(request,'logAndreg/register.html')

    
def create(request):

    valid,response=User.objects.validator(request.POST)

    request.session['tempUserData']={
        'firstname':request.POST['firstname'],
        'lastname':request.POST['lastname'],
        'email':request.POST['email']
    }

   

    if validateResponse(request,valid,response):
        del request.session['tempUserData']

        request.session['user_id']=response
        request.session['color']="success"
        messages.success(request, "Successfully Registered")
        return redirect(reverse("dashboard:dashboard"))
    else:
        request.session['color']="danger"
        return redirect(reverse("userLG:registration"))
    

def login(request):
    return render(request,'logAndreg/login.html')
    
def proccess(request):

    valid,response=User.objects.loginValidation(request.POST)

    if validateResponse(request,valid,response):
        request.session['user_id']=response
        user_level=User.objects.get(id=response).user_level
        
        if user_level ==1:
            return redirect(reverse("adminDashboard:admin"))
        else:
            return redirect(reverse("dashboard:dashboard"))
    else:
        return redirect(reverse("userLG:login"))
    
def logoff(request):
    del request.session['user_id']
    del request.session["productInfo"]
    if "product_id" in request.session:
        del request.session['product_id']
        
    return redirect(reverse("userLG:login"))


def validateResponse(request,valid,response):
    if valid==False:
        for error in response:
            messages.error(request, error)
        return False

    else:
        return True