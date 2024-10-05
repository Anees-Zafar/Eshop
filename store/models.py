from django.db import models
import datetime
from datetime import timedelta
from django.utils import timezone

class Category(models.Model):
    name=models.CharField(max_length=50)
    
    def __str__(self):
        return str(self.name)
    
class Color(models.Model):
    title=models.CharField(max_length=50)
    color_code=models.CharField(max_length=50)
    
    def __str__(self):
        return str(self.title)
    
class Size(models.Model):
    title=models.CharField(max_length=50)
    
    def __str__(self):
        return str(self.title)    

class Products(models.Model):
    name=models.CharField(max_length=50)
    price=models.DecimalField(max_digits=6, decimal_places=2)
    description=models.TextField()
    category=models.ForeignKey(Category , on_delete=models.CASCADE)
    image=models.ImageField(upload_to='uploadedimages/')

    def __str__(self):
        return str(self.name)

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url
    


    @staticmethod
    def get_all_products_by_id(category_id):
        if category_id:
            return Products.objects.filter(category=category_id)
        else:
            return Products.objects.all()

    @staticmethod
    def det_product_by_id(ids):
        return Products.objects.filter(id__in=ids)
       
		
class ProductAttribute(models.Model):
    product=models.ForeignKey(Products, on_delete=models.CASCADE)
    color=models.ForeignKey(Color, on_delete=models.CASCADE)
    size=models.ForeignKey(Size, on_delete=models.CASCADE)
    price=models.DecimalField(max_digits=6, decimal_places=2)
    # image=models.ImageField(upload_to='uploadedimages/' ,blank=True, null=True)


    def __str__(self):
        return str(self.product.name)

        
class Customer(models.Model):
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    phone=models.CharField(max_length=11)
    email=models.EmailField()
    password=models.CharField(max_length=600)

    def __str__(self):
        return str(self.first_name)	

    
    def register(self):
        self.save()	



    def isExist(self):
        return Customer.objects.filter(email=self.email).exists()   



    @staticmethod
    def get_customer_by_email(email):
        try:
            return Customer.objects.get(email=email)
        except:
            return False    
        


# Order
status_choice=(
        ('process','In Process'),
        ('shipped','Shipped'),
        ('delivered','Delivered'),
        ('canceled', 'Canceled')
    )
class CartOrder(models.Model):
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE)
    total_price = models.IntegerField(blank=True, null=True)
    paid_status=models.BooleanField(default=False)
    date=models.DateField(default=datetime.datetime.today)
    order_status=models.CharField(choices=status_choice,default='process',max_length=150)

    def __str__(self):
        return str(self.customer)	
    
      # Check if the order can be canceled (within 24 hours and status is 'process')
    @property
    def can_cancel(self):
        cancel_time_limit = timedelta(hours=24)  # Time limit for order cancellation (24 hours)
        return timezone.now().date() <= (self.date + cancel_time_limit) and self.order_status == 'process'


	
class Order(models.Model):
    order=models.ForeignKey(CartOrder,on_delete=models.CASCADE , null=True)
    product=models.ForeignKey(Products, on_delete=models.CASCADE)
    customer=models.ForeignKey(Customer, on_delete=models.CASCADE)
    quantity=models.IntegerField(default=1)
    price=models.IntegerField()
    adress=models.CharField(max_length=500 , default="")
    phone=models.CharField( max_length=50, default="")
    color = models.CharField(max_length=30, blank=True, null=True)
    size = models.CharField(max_length=30, blank=True, null=True)
    total_price = models.IntegerField(blank=True, null=True)
    status=models.BooleanField(default=False)

    date=models.DateField(default=datetime.datetime.today)


    def __str__(self):
        return str(self.customer)
    

    def place_order(self):
        return self.save()
    
    @staticmethod
    def get_orders(customer_id):
        return Order.objects.filter(customer = customer_id).order_by('-date')


class Profile(models.Model):
    customer=models.ForeignKey(Customer, on_delete=models.CASCADE)
    cover_photo=models.ImageField(upload_to='uploadedimages/')
    profile_photo=models.ImageField(upload_to='uploadedimages/')
    address = models.CharField(max_length=255, blank=True, null=True)
    about = models.CharField(max_length=500,blank=True, null=True)

    def __str__(self):
        return str(self.customer)


class Todo(models.Model):
    customer=models.ForeignKey(Customer, on_delete=models.CASCADE)
    title=models.CharField(max_length=500 , default="")
    description=models.CharField(max_length=500 , default="")
    status=models.BooleanField(default=False)
    date=models.DateField(default=datetime.datetime.today)



    def __str__(self):
        return str(self.customer)
    

    @staticmethod
    def get_todos(customer_id):
        return Todo.objects.filter(customer = customer_id).order_by('-date')
    


class Reviews(models.Model):
    customer=models.ForeignKey(Customer, on_delete=models.CASCADE)
    product=models.ForeignKey(Products, on_delete=models.CASCADE)
    title=models.CharField(max_length=800 , default="")
    stars = models.IntegerField(blank=True, null=True)
    date=models.DateField(default=datetime.datetime.today)

    def __str__(self):
        return str(self.customer)