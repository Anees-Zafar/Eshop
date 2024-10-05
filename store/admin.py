from django.contrib import admin
from .models import Category, Products,Customer,Order , Todo ,Profile , Color , Size , ProductAttribute , Reviews ,CartOrder

class AdminProducts(admin.ModelAdmin):
    list_display = ['name', 'price', 'category','image']

class AdminCategory(admin.ModelAdmin):
    list_display = ['id','name']

class AdminCustomer(admin.ModelAdmin):
    list_display = ['id', 'first_name' , 'last_name' , 'phone' , 'email' , 'password']

class AdminOrder(admin.ModelAdmin):
    list_display=['id', 'order', 'product', 'customer' , 'quantity' , 'price' ,'adress', 'phone','size','color','total_price', 'status', 'date']
        
class AdminCartOrder(admin.ModelAdmin):
    list_display=['id','customer' , 'total_price' , 'date' , 'paid_status', 'order_status' ]

class AdminTodo(admin.ModelAdmin):
    list_display=['id','customer' , 'title', 'description' , 'status' , 'date']

class AdminProfile(admin.ModelAdmin):
    list_display=['id', 'customer' , 'cover_photo' , 'profile_photo' , 'about' , 'address']

class AdminProductAttribute(admin.ModelAdmin):
    list_display=['id', 'product' , 'color' , 'size' , 'price' ]

class AdminColor(admin.ModelAdmin):
    list_display=['id' , 'title' , 'color_code'] 


class AdminReviews(admin.ModelAdmin):
    list_display=['id','customer' ,'product' , 'title',  'stars' , 'date']       

admin.site.register(Products, AdminProducts)  
admin.site.register(Category,AdminCategory)  
admin.site.register(Customer,AdminCustomer)
admin.site.register(Order , AdminOrder)
admin.site.register(Todo , AdminTodo)
admin.site.register(Profile , AdminProfile)
admin.site.register(Color , AdminColor)
admin.site.register(Size)
admin.site.register(ProductAttribute, AdminProductAttribute)
admin.site.register(Reviews, AdminReviews)
admin.site.register(CartOrder,AdminCartOrder)