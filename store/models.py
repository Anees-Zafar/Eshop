from django.db import models
import datetime
# Create your models here.

class Category(models.Model):
    name=models.CharField(max_length=50)
    
    def __str__(self):
        return str(self.name)


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

	
class Order(models.Model):
    product=models.ForeignKey(Products, on_delete=models.CASCADE)
    customer=models.ForeignKey(Customer, on_delete=models.CASCADE)
    quantity=models.IntegerField(default=1)
    price=models.IntegerField()
    adress=models.CharField(max_length=500 , default="")
    phone=models.CharField( max_length=50, default="")
    status=models.BooleanField(default=False)

    date=models.DateField(default=datetime.datetime.today)


    def __str__(self):
        return str(self.customer)
    

    def place_order(self):
        return self.save()
    
    @staticmethod
    def get_orders(customer_id):
        return Order.objects.filter(customer = customer_id).order_by('-date')





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