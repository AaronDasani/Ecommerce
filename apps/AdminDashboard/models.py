from __future__ import unicode_literals

from django.db import models

# Create your models here.
from ..LoginAndRegister.models import User
class ProductManager(models.Manager):

   def validate(self,form,image,user_id):
        errors=[]

        # brand validation
        if len(form['brand'])<1:
            errors.append("brand should not be blank")
        if len(form['brand'])>30:
            errors.append("brand should ne less than 30 characters")
    
        # Name validation
        if len(form['name'])<1:
            errors.append(" Product name should not be blank")
        if len(form['name'])>30:
            errors.append("Product name should ne less than 30 characters")

        # product Description
        if len(form['description'])<1:
            errors.append(" Product description should not be blank")

        # product Price
        if len(form['price'])<1:
            errors.append(" Please provide a Price")
        if form['price'].isdigit() is False:
            errors.append("Price should contain only numbers")

        # Category validation
        if len(form["addNewCategory"])<1:
            if len(form["category"])<1:
                errors.append("Please provide an category")
            else:
                new_category=False
                category=form["category"]
        else:
            if form["category"]:
                errors.append("Please include only one category")
            else:
                if len(form["addNewCategory"])<1:
                    errors.append("Please provide an category")
                elif len(form["addNewCategory"])<3:
                    errors.append("category should be atleast 3 characters")
                else:
                    new_category=True
                    category=form["addNewCategory"]

        # product Inventory:
        if len(form['inventory'])<1:
            errors.append(" Please provide an inventory")
        if form['inventory'].isdigit() is False:
 
            errors.append("Inventory should be a numbers")

        # product Amount Sold
        if len(form['sold'])<1:
            errors.append(" Please provide a sold amount")
        if form['sold'].isdigit() is False:
            errors.append("Sold Amount should be a numbers")
        

        if errors:
            return(False,errors)
        else:
            # >>>>>>EDITING PRODUCT<<<<<<<<
            if 'editForm' in form:
                product=Product.objects.get(id=form['product_id'])

                try:
                    product_image=image['image']
                    product.upload=product_image
                    product.save()
                except:
                    pass

                product.brand=form['brand']
                product.itemName=form['name']
                product.price=form['price']
                product.description=form['description']
                product.inventory.inventory=form['inventory']
                product.inventory.quantitySold=form['sold']
    
                if new_category==True:
                    print("create category")
                    # create category
                    category=Category.objects.create(category=category)
                else:
                    category=Category.objects.get(category=category)

                # add relationship 
                product.inventory.category_id=category.id
                product.save()
                product.inventory.save()

                print("Editing form right now<<<<<<<---------")

            else:
                # >>>>>>>>>>>CREATING PRODUCT<<<<<<<<<<<
                try:
                    product_image=image['image']
                except:
                    product_image="image/default.jpg"


                product=Product.objects.create(
                    brand=form['brand'],
                    itemName=form['name'],
                    price=form['price'],
                    description=form['description'],
                    origin="inventory",
                    upload=product_image,
                    user=User.objects.get(id=user_id)
                )
                
                if new_category==True:
                    # create category
                    category=Category.objects.create(category=category)

                else:
                    category=Category.objects.get(category=category)

                ProductInventory.objects.create(
                    inventory=form['inventory'],
                    quantitySold=form['sold'],
                    product=Product.objects.get(id=product.id),
                    category=Category.objects.get(id=category.id)
                )
               

                print("Creating Produt right now<<<<<<<---------")


            return(True,errors)


class Product(models.Model):
    brand=models.CharField(max_length=40)
    itemName=models.CharField(max_length=255)
    price=models.FloatField()
    description=models.TextField()
    origin=models.CharField(max_length=20)
    upload = models.ImageField(default='default.jpg', blank=True,upload_to='image/')
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    user=models.ForeignKey(User,related_name="product",on_delete=models.CASCADE)
    objects=ProductManager()

class Category(models.Model):
    category=models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    

class ProductInventory(models.Model):
    inventory=models.IntegerField()
    quantitySold=models.IntegerField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    product=models.OneToOneField(Product,related_name="inventory",on_delete=models.CASCADE)
    category=models.ForeignKey(Category,related_name="inventory_category",on_delete=models.CASCADE)


