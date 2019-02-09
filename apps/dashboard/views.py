from django.shortcuts import render,redirect,HttpResponse
from django.urls import reverse
from django.contrib import messages
from django.http import JsonResponse
import random
import string
# Create your views here.
from .models import Cart,Order
from..LoginAndRegister.models import User
from ..AdminDashboard.models import Product

def dashboard(request):

    # check if their is a user_id, basically checking if a user is logged in
    if 'user_id' not in request.session:
        return redirect(reverse("userLG:login"))

    # remember some information about the search history
    if 'productInfo' not in request.session:
        request.session['productInfo']={
            'categories':"None",
            'price':"None",
            'brand':"None",
            'searchedProduct':'None'
        }

    # those information was used to help the user be able to click on the suggestion product and be able to show the correct information about that specific product. We delete it here becuase we do not need it in this page.
    if "product_id" in request.session:
        del request.session['product_id']
        request.session.modified = True

    # miscelleneous information to make the dashboard page better
    itemsInCart=User.objects.get(id=request.session['user_id']).cart.all().count() 
    userLevel=User.objects.get(id=request.session['user_id']).user_level
    # print(dir(random))
    return render(request,"ecommerce/dashboard.html",{'itemsInCart':itemsInCart,'user_level':userLevel})



def product_page(request,product_id,product_brand):
    if 'user_id' not in request.session:
        return redirect(reverse("userLG:login"))

    product_list={}

    if 'product_id' not in request.session:
        print("product_id Initialized <<<<<<<-------")
        request.session['product_id']=None
 
    # if request.session['product_id'] != str(product_id):
    request.session['product_id']=product_id
    request.session.modified = True

    output=Product.objects.get(id=product_id)

    print("*#"*50)
    print(output.upload)
    print(request.session['product_id'])
    print("*"*80)

    product_list={
        'product_name':output.itemName,
        'product_brand':output.brand,
        'product_price':output.price,
        'product_image':output.upload.url,
        'product_description':output.description 
    }
    

    # changing the brand filter in the session
    request.session['productInfo']['brand']=product_brand
    request.session.modified = True

    suggestion_list=sendingRequest(request,catergories=request.session['productInfo']['categories'],brand=product_brand,price_range=request.session['productInfo']['price'],searchedProduct="None")

    itemsInCart=User.objects.get(id=request.session['user_id']).cart.all()  
    for index in itemsInCart:
        index.price=index.price*index.quantity

    return render(request,"ecommerce/productPage.html",{'product_list':product_list,'suggested_product':suggestion_list,'itemsInCart':itemsInCart})
   



def checkout(request):
    cart=User.objects.get(id=request.session['user_id']).cart.all()
    totalCost=0
    discount=10
    for index in cart:
        index.price=index.price*index.quantity
        totalCost+=index.price


    context={
        'products':cart,
        'totalCost':totalCost-discount,
        'discount':discount,
        'totalItems':cart.count()
    }
    
    return render(request,"ecommerce/checkout.html",context)


def payementProcess(request):
    # Save Order
    print(request.POST)
    try:
        current_user=request.session['user_id']
    except:
        return redirect(reverse("userLG:login"))

    cart=Cart.objects.filter(user_id=request.session['user_id'])
    # order_id=''.join(random.choices(string.ascii_uppercase + string.digits,k=10))
    order_id=''.join(random.sample(string.ascii_uppercase + string.digits,k=10))
    print(">>>>>>>>>>>>>>>" ,order_id)

    for index in cart:
        Order.objects.create(
            user=User.objects.get(id=current_user),
            order_id=order_id,
            brand=index.brand,
            itemName=index.itemName,
            price=index.price,
            quantity=index.quantity,
            totalCost=(index.price) * (index.quantity),
            OrderStatus='Order In'
        )

    # Delete Cart Items after purchase is done
    Cart.objects.filter(user_id=request.session['user_id']).delete()


    return redirect(reverse("dashboard:thankYou"))


def thankYou(request):
    context={
       'user':User.objects.get(id=request.session['user_id']).first_name
    }
    return render(request,"ecommerce/thankYou.html",context)



def add_to_cart(request):
    print(request.POST)
    try:
        current_user=request.session['user_id']
    except:
        return redirect(reverse("userLG:login"))

    Cart.objects.create(user=User.objects.get(id=current_user),product_id=request.session['product_id'],brand=request.POST['brand'],itemName=request.POST['productName'],price=request.POST['price'],quantity=request.POST['quantity'])

    ItemsInCart=User.objects.get(id=request.session['user_id']).cart.all().count() 
    return JsonResponse({'numberOfItems': ItemsInCart})


def lookAtCart(request):
    itemsInCart=User.objects.get(id=request.session['user_id']).cart.all()  
    for index in itemsInCart:
        index.price=index.price*index.quantity
    return render(request,"ecommerce/cart_Items.html",{'itemsInCart':itemsInCart})

def deleteCartItem(request,itemId):
    Cart.objects.filter(user_id=request.session['user_id']).filter(id=itemId).delete()
    return (lookAtCart(request))

def NumberOfItemInCart(request):
    ItemsInCart=User.objects.get(id=request.session['user_id']).cart.all().count() 
    return JsonResponse({'numberOfItems': ItemsInCart})


def PriceRange(request):
    print("price Range")
    request.session['productInfo']['price']=request.POST['maxPrice']
    request.session.modified = True
    product_list=sendingRequest(request,price_range=request.POST['maxPrice'], catergories= request.session['productInfo']['categories'], brand=request.session['productInfo']['brand'],searchedProduct=request.session['productInfo']['searchedProduct'])
    if len(product_list)<1:
        print("product list empty")
        return render(request,"ecommerce/notFound.html")

    return render(request,"ecommerce/product_list.html",{'product_list':product_list})


def searchProducts(request):
    if request.method=='POST':
        request.session['productInfo']['searchedProduct']=request.POST['searchedProduct']
        request.session.modified = True
        product_list=sendingRequest(request,catergories= request.session['productInfo']['categories'],brand=request.session['productInfo']['brand'],price_range=request.session['productInfo']['price'],searchedProduct=request.session['productInfo']['searchedProduct'])
    
        if len(product_list)<1:
            print("product list empty")
            return render(request,"ecommerce/notFound.html")

        return render(request,"ecommerce/product_list.html",{'product_list':product_list})
    else:
        return redirect(reverse("dashboard:dashboard"))

def searchCategory(request,category="Shorts"):
    print("searchCategory")
    request.session['productInfo']['categories']=category
    request.session.modified = True
    product_list=sendingRequest(request,catergories=category,brand=request.session['productInfo']['brand'],price_range=request.session['productInfo']['price'],searchedProduct=request.session['productInfo']['searchedProduct'])
        
    if len(product_list)<1:
        print("product list empty")
        return render(request,"ecommerce/notFound.html")

    
    return render(request,"ecommerce/product_list.html",{'product_list':product_list})
	

def searchBrand(request):
    print("searchbrand")
    request.session['productInfo']['brand']=request.POST['searchBrand']
    request.session.modified = True
    product_list=sendingRequest(request,brand=request.POST['searchBrand'],catergories= request.session['productInfo']['categories'],price_range=request.session['productInfo']['price'],searchedProduct=request.session['productInfo']['searchedProduct'])
    
    if len(product_list)<1:
        print("product list empty")
        return render(request,"ecommerce/notFound.html")
        
    return render(request,"ecommerce/product_list.html",{'product_list':product_list})

def searchAllProducts(request):
    print("searchAllProducts")
    product_list=sendingRequest(request,catergories=request.session['productInfo']['categories'],brand=request.session['productInfo']['brand'],price_range=request.session['productInfo']['price'],searchedProduct=request.session['productInfo']['searchedProduct'])

    return render(request,"ecommerce/product_list.html",{'product_list':product_list})

def removeTags(request,tagKey):
   
    request.session['productInfo'][tagKey]="None"
    request.session.modified = True
    return redirect(reverse("dashboard:dashboard"))




def sendingRequest(request,brand,catergories,price_range,searchedProduct):
    product_list=[]
    print("sending Request <<<<<<<<<<<<---------||||")

    print("*"*60)
    print(brand)
    print(catergories)
    print(price_range)
    print(searchedProduct)
    print("*"*60)

    if price_range !="None":
        Inventory_products=Product.objects.filter(price__lt=price_range)
    else:
        Inventory_products=Product.objects.all()


    for index in Inventory_products:
        if (( brand.lower() in index.brand.lower() or brand.lower()=="none") and (catergories.lower() in index.inventory.category.category.lower() or catergories.lower()=="none") and (searchedProduct.lower() in index.itemName.lower() or searchedProduct.lower()=="none")):
            product_list.append(
                    {
                        'product_price':index.price,
                        'product_image':index.upload.url,
                        'product_id':index.id,
                        'product_brand':index.brand,
                    }
                )
    return (product_list)