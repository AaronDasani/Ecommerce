from django.shortcuts import render,redirect,HttpResponse
from django.urls import reverse
from django.contrib import messages
from django.http import JsonResponse
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from ..LoginAndRegister.models import User
from ..dashboard.models import Order
from .models import Product,Category
import json
# Create your views here.


def admin(request):
    # if there is no 'user_id' in request.session send the user to the login page
    if 'user_id' not in request.session:
        return redirect(reverse("userLG:login"))

    # if we get an error trying to get the user_level, send the user to the login page
    try:
        current_user=User.objects.get(id=request.session['user_id'])  
    except:
        return redirect(reverse("userLG:login"))
    # if user_level not 1, [number 1 being the admin] send the user to the login page
    if current_user.user_level  != 1:
        return redirect(reverse("userLG:login"))


    orders_list=Order.objects.raw("SELECT * FROM dashboard_order GROUP BY order_id ORDER BY created_at DESC")  

# the pagination works on Django 2.1 and above

    # paginator = Paginator(orders_list, 3) 
    # page = request.GET.get('page')
    # orders = paginator.get_page(page)
 
    # context={
    #     'orders':orders,
    #     'user':current_user
    # }
    context={
        'orders':orders_list,
        'user':current_user
    }

    return render(request, "admin/adminDashboard.html",context)


def searchOrders(request):

    orders=Order.objects.raw("Select * from dashboard_order group by order_id")
    MatchOrder=[]
    # page = request.GET.get('page')

    for index in orders:
        if((request.POST['searchOrder']).lower() in (index.user.first_name).lower()):
            MatchOrder.append(index)

# the pagination works on Django 2.1 and above
    # paginator = Paginator(MatchOrder, 3) # Show speficy amount orders per page
    # orders = paginator.get_page(page)

    # if len(MatchOrder)>0:
    #     return render(request,"admin/orderList.html",{'orders':orders})

    if len(MatchOrder)>0:
        return render(request,"admin/orderList.html",{'orders':MatchOrder})

    else:
        try:
            orders=Order.objects.raw("Select * from dashboard_order group by order_id")
            for index in orders:
                if((request.POST['searchOrder']).lower() in (index.order_id).lower()):
                    MatchOrder.append(index)

            # paginator = Paginator(MatchOrder, 3) # Show speficy amount orders per page
            # orders = paginator.get_page(page)
            
            # If using Pagination with Djnago 2.1 and above change the MatchOrder below to orders
            if MatchOrder[0] is None:
                return HttpResponse("<h4 class='font-weight-light bg-danger text-white mt-3 p-3 ml-5'>No Product Found !!</h4>")

            return render(request,"admin/orderList.html",{'orders':MatchOrder})

        except:
            return HttpResponse("<h4 class='font-weight-light bg-danger text-white mt-3 p-3 ml-5'>No Product Found !!</h4>")


def viewProduct(request,order_id):
    products=Order.objects.filter(order_id=order_id)
    totalCost=0
    discount=10
    for index in products:
        price=index.price*index.quantity
        totalCost+=price

    context={
        'products':products,
        'order': Order.objects.filter(order_id=order_id)[0],
        'subCost':str(round(totalCost,2)),
        'totalCost':str(round(totalCost-discount,2)),
        'discount':discount
    }

    return render(request,"admin/OrderDetails.html",context)

def create(request):
    print(request.POST) 
    if request.POST is False:
        return redirect(reverse("userLG:logoff"))

   
    valid,response=Product.objects.validate(request.POST,request.FILES,request.session["user_id"])

    if valid==False:
        request.session['color']="danger"
        for error in response:
            messages.error(request, error)
    else:
        request.session['color']="success"
        messages.success(request, "Successfully Added Product to Store")

    return redirect(reverse("adminDashboard:productsInStock"))



def productsInStock(request):

    context={
        'Products':Product.objects.all(),
        'category':Category.objects.all()
    }


    return render(request,"admin/InStock.html",context)



def edit(request):

    valid,response=Product.objects.validate(request.POST,request.FILES,request.session["user_id"])
    if valid==False:
        request.session['color']="danger"
        for error in response:
            messages.error(request, error)
    else:
        request.session['color']="success"
        messages.success(request, "Product Successfully Edited ")

    return redirect(reverse("adminDashboard:productsInStock"))


def fetchProductInfo(request):
    try:
        product=Product.objects.get(id=request.GET['product_id'])
    except:
        return redirect(reverse("adminDashboard:productsInStock"))
    context={
        'product':product,
        'category':Category.objects.all()
    }
   
    return render(request,"admin/editProductInfo.html",context)



def delete(request):
    print(request.POST)
    try:
        Product.objects.get(id=request.POST['product_id']).delete()
        messages.success(request, "Product Successfully Deleted ")
    except:
        request.session['color']="danger"
        messages.error(request, "Product Was not delete, Please contact your Supervisor")

    context={
        'Products':Product.objects.all()
    }
    

    return render(request,"admin/inStockProduct.html",context)

def changingProductStatus(request):
    print(request.POST)
    status=request.POST["select"]
    order_id=request.POST["orderId"]

    Order.objects.filter(order_id=order_id).update(OrderStatus=status)

    return JsonResponse({'status':status})


def searchProduct(request):
    ProductName= request.POST['searchProduct'].lower()
   
    products=Product.objects.filter(itemName__contains=ProductName)
    if not products:
        return HttpResponse("<h4 class='font-weight-light bg-danger text-white mt-3 p-3 text-center shadow rounded'>No Product Found !!</h4>")
            
    return render(request,"admin/inStockProduct.html",{'Products':products})

    
# def ajax_pagination(request):

#     orders_list=Order.objects.raw("SELECT * FROM dashboard_order GROUP BY order_id ")
#     paginator = Paginator(orders_list, 2)

#     orders = paginator.get_page(request.GET['page'])

#     return render(request,"admin/orderList.html",{'orders':orders})
  
