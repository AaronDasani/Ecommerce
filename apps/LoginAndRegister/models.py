from __future__ import unicode_literals

from django.db import models
import re
import bcrypt
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
UpperCasePassword_REGEX=re.compile(r'^(?=.*?[A-Z])')
NumericValue_REGEX=re.compile(r'^(?=.*?[0-9])')

date_REGEX=re.compile(r'^(194[0-9]|195[0-9]|196[0-9]|197[0-9]|198[0-9]|199[0-9])[-](0?[1-9]|1[012])[-](0?[1-9]|[12][0-9]|3[01])$')


# Create your models here.
class UserManager(models.Manager):
    def validator(self,form):
        error=[]

        # check if email already taken
        if self.filter(email=form['email']):
            error.append("Email already used")
            return (False,error)

        # first name validation
        if len(form['firstname'])<1:
            error.append("First name cannot be blank!!")
        if form['firstname'].isalpha()==False:
            error.append("Only letters in the first name")
        if len(form['firstname'])<2:
            error.append("First name should be atleat 2 characters")

        # last name validation
        if len(form['lastname'])<1:
            error.append("last name cannot be blank!!")
        if form['lastname'].isalpha()==False:
            error.append("Only letters in the last name")
        if len(form['lastname'])<2:
            error.append("last name should be atleat 2 characters")

        # email validation
        if len(form['email']) < 1:
            error.append("Email cannot be blank!")
        if not EMAIL_REGEX.match(form['email']):
            error.append("Invalid Email Address!")
            
        # birthday validation
        if not date_REGEX.match(form['birthday']) :
            error.append("invalid date")


        #password validation
        if len(form['password'])<1:
            error.append("please provide a password")
        if len(form['password'])<8:
            error.append("password is too short. Should be atleast 8 characters")
        if not UpperCasePassword_REGEX.match(form['password']) :
            error.append("at least one uppercase letter")
        if not NumericValue_REGEX.match(form['password']) :
            error.append("at least one number")

        # confirm password validation
        if form["confirmpassword"]!=form["password"]:
            error.append("Password does not match")

        if error:
            return(False,error)
        else:
            if User.objects.all().count()<1:
                user_level=1
            else:
                user_level=0
                
            hashPassword=bcrypt.hashpw(form['password'].encode(),bcrypt.gensalt())
            Users=self.create(first_name=form['firstname'],last_name=form['lastname'], email=form['email'],password=hashPassword, birthday=form['birthday'],user_level=user_level,description="I am a programmer and ......")
            current_user={"user_id":Users.id, "user_level":user_level}
            return (True,current_user)

    def loginValidation(self,form):
        error=[]
        try:
            User=self.get(email=form['email'])
        except:
            error.append("invalid email or password")
            return (False,error)
        
        print(form['password'].encode())
        print(User.password.encode())


        if bcrypt.checkpw(form['password'].encode(),User.password.encode()):
            return (True,User.id)
        else:
            error.append("invalid email or password")
            return (False,error)

class User(models.Model):
    first_name=models.CharField(max_length=255)
    last_name=models.CharField(max_length=255)
    email=models.CharField(max_length=255)
    password=models.CharField(max_length=255)
    birthday=models.DateField(auto_now=False, auto_now_add=False)
    description=models.TextField()
    user_level=models.IntegerField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects=UserManager()
