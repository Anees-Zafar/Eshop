from django.shortcuts import render ,redirect , HttpResponseRedirect
from django.http import HttpResponse, JsonResponse
from .models import *
from django.contrib.auth.hashers import check_password, make_password
from django.views import View
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import requires_csrf_token
import json



@method_decorator(csrf_protect, name='dispatch')
class Index(View):
    def post(self , request):
        productcome=request.POST.get('product')
        removecome=request.POST.get('remove')
        cart=request.session.get('cart')
        if cart:
            quantity=cart.get(productcome)
            if quantity:
                if removecome:
                    if quantity<=1:
                        cart.pop(productcome)
                    else:
                        cart[productcome] =quantity-1    
                    

                else:
                    cart[productcome] =quantity+1    
                  
            else:
                cart[productcome] =1     
        else:
            cart={}
            cart[productcome]=1  

        request.session['cart']=cart     
        print ( cart)
        return redirect(f'/#{productcome}')



    def get(self , request):
        if 'cart' not in request.session:
            request.session['cart'] = {}
        product = None
        collection=Category.objects.all()
        collectionid=request.GET.get('category')
        if collectionid:
            product=Products.get_all_products_by_id(collectionid)
        else:
            product=Products.objects.all()   

        print ('you are:', request.session.get('email'))
        print(request.session['cart'])
        context = {'product': product , 'category':collection}
        return render(request, 'index.html', context)
    


@method_decorator(csrf_protect, name='dispatch')
class Malecatageory(View):
    def post(self , request):
        productcome=request.POST.get('product')
        removecome=request.POST.get('remove')
        cart=request.session.get('cart')
        if cart:
            quantity=cart.get(productcome)
            if quantity:
                if removecome:
                    if quantity<=1:
                        cart.pop(productcome)
                    else:
                        cart[productcome] =quantity-1    
                    

                else:
                    cart[productcome] =quantity+1    
                  
            else:
                cart[productcome] =1     
        else:
            cart={}
            cart[productcome]=1  

        request.session['cart']=cart     
        print ( cart)
        return redirect('male')

    def get(self , request):
        items=Products.get_all_products_by_id(1)
        
        return render(request, 'male.html', {'items':items})
    




@method_decorator(csrf_protect, name='dispatch')
class Femalecatageory(View):
    def post(self , request):
        productcome=request.POST.get('product')
        removecome=request.POST.get('remove')
        cart=request.session.get('cart')
        if cart:
            quantity=cart.get(productcome)
            if quantity:
                if removecome:
                    if quantity<=1:
                        cart.pop(productcome)
                    else:
                        cart[productcome] =quantity-1    
                    

                else:
                    cart[productcome] =quantity+1    
                  
            else:
                cart[productcome] =1     
        else:
            cart={}
            cart[productcome]=1  

        request.session['cart']=cart     
        print ( cart)
        return redirect('female')

    def get(self , request):
        items=Products.get_all_products_by_id(2)
       
        return render(request, 'female.html', {'items':items})



@method_decorator(csrf_protect, name='dispatch')
class Kidcatageory(View):
    def post(self , request):
        productcome=request.POST.get('product')
        removecome=request.POST.get('remove')
        cart=request.session.get('cart')
        if cart:
            quantity=cart.get(productcome)
            if quantity:
                if removecome:
                    if quantity<=1:
                        cart.pop(productcome)
                    else:
                        cart[productcome] =quantity-1    
                    

                else:
                    cart[productcome] =quantity+1    
                  
            else:
                cart[productcome] =1     
        else:
            cart={}
            cart[productcome]=1  

        request.session['cart']=cart     
        print ( cart)
        return redirect('kid')

    def get(self , request):
        items=Products.get_all_products_by_id(3)
        return render(request, 'kid.html', {'items':items})




@requires_csrf_token
def Signup(request):
    if request.method=='GET':
        return render(request, 'signup.html')
    else:
        first_name=request.POST.get('firstname')
        last_name=request.POST.get('lastname')
        phone=request.POST.get('phone')
        email=request.POST.get('email')
        password=request.POST.get('password')
        customer=Customer(
                first_name=first_name,
                last_name=last_name,
                phone=phone,
                email=email,
                password=password,
            )

        values={
            'first_name':first_name,
            'last_name':last_name,
            'phone':phone,
            'email':email,
        }

    # #  Form validation 
        error=None 

    #     if not first_name:
    #         error='First name is required'
    #     elif len(first_name)<4 :
    #         error='First name is must be grater than 4 digits'
    #     elif not last_name:
    #         error='Last name is required'
    #     elif len(last_name)<4 :
    #         error='Last name is must be grater than 4 digits'    
    #     elif not phone:
    #         error='Phone number is required'
    #     elif len(phone)<10 :
    #         error='Phone number is must be grater than 11 digits'
    #     elif not email:
    #         error='Email is required'  
    #     elif customer.isExist():  
    #         error = 'This Email ID already exists'          

        if not error:
            customer.password=make_password(customer.password)
            customer.register()
            return redirect('login')
        else:
            return render (request , 'signup.html', {'error': error , 'values':values})


def check_email(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        if Customer.objects.filter(email=email).exists():
            return JsonResponse({'emailExists': True})
        else:
            return JsonResponse({'emailExists': False})

        
    

@method_decorator(csrf_protect, name='dispatch')
class Login(View):
    return_url = None

    def get(self , request):
        Login.return_url = request.GET.get('return_url')
        return render(request, 'login.html')
        
    def post(self , request):
        if request.method == 'POST':
            email = request.POST.get('email')
            password = request.POST.get('password')

            customer = Customer.get_customer_by_email(email)
            if customer:
                if check_password(password, customer.password):
                    request.session['customer_id'] = customer.id
                    request.session['email'] = customer.email
                    if Login.return_url:
                        # response= HttpResponseRedirect(Login.return_url)
                        return JsonResponse({'success': True, 'redirect_url': Login.return_url})
                    
                    else:
                        Login.return_url = None
                        # return redirect("index")
                        return JsonResponse({'success': True, 'redirect_url': '/'})  # Redirect to home on success
                else:
                    return JsonResponse({'success': False, 'error': 'Invalid email or password.'})
            else:
                return JsonResponse({'success': False, 'error': 'Invalid email or password.'})
        return JsonResponse({'success': False, 'error': 'Invalid request.'})



   
# def check_login(request):
#     if request.method == 'POST':
#         email = request.POST.get('email')
#         password = request.POST.get('password')

#         customer = Customer.get_customer_by_email(email)
#         if customer:
#             if check_password(password, customer.password):
#                 request.session['customer_id'] = customer.id
#                 request.session['email'] = customer.email
#                 if Login.return_url:
#                     return HttpResponseRedirect(Login.return_url)
#                 else:
#                     Login.return_url = None
#                     return redirect("index")  # Redirect to home on success
#             else:
#                 return JsonResponse({'success': False, 'error': 'Invalid email or password.'})
#         else:
#             return JsonResponse({'success': False, 'error': 'Invalid email or password.'})
#     return JsonResponse({'success': False, 'error': 'Invalid request.'})
        
   
        
            



def logout(request):
    request.session.clear()
    return redirect('login')


@requires_csrf_token
def cart(request):
    if request.method=='GET':
        ids=list(request.session.get('cart').keys())
        cartproducts=Products.det_product_by_id(ids)
        return render(request,'cart.html' , {'cartproducts': cartproducts}  )
    else:
        productcome=request.POST.get('product')
        removecome=request.POST.get('remove')
        cart=request.session.get('cart')
        if cart:
            quantity=cart.get(productcome)
            if quantity:
                if removecome:
                    if quantity<=1:
                        cart.pop(productcome)
                    else:
                        cart[productcome] =quantity-1    
                    

                else:
                    cart[productcome] =quantity+1    
                  
            else:
                cart[productcome] =1     
        else:
            cart={}
            cart[productcome]=1  

        request.session['cart']=cart     
        print ( cart)
        return redirect('cart')



    











@requires_csrf_token
def checkout(request):
    

    if request.method == 'POST':
        adress = request.POST.get('adress')
        phone = request.POST.get('phone')
        customer_id = request.session.get('customer_id')
        cart = request.session.get('cart')
        products = Products.det_product_by_id(list(cart.keys()))

        print(adress, phone, customer_id, cart, products)

        
        for product in products:
            order = Order(
                customer=Customer(id=customer_id),
                product=product,
                price=product.price,
                adress=adress,
                phone=phone,
                quantity=cart.get(str(product.id))
            )
            order.save()
        request.session['cart'] = {} 
        if request.session.modified:
             print (True)  

       
        return redirect('orders')  
      
    
        

        





            
       
def orders(request):
    customerlogin = request.session.get('customer_id')
    orderitems = Order.get_orders(customerlogin)
    return render(request, 'orders.html', {'orderitems': orderitems})



def paypalpage(request):
    return render(request , 'paypal.html')



def paypal_success(request):
    return HttpResponse("Payment completed successfully!")

def paypal_failed(request):
    return HttpResponse("Payment failed. Please try again.")



def todo(request):
    if request.method=='GET':
        customerlogin = request.session.get('customer_id')
        todoitems=Todo.get_todos(customerlogin)
        return render(request , 'todo.html' , {'todoitems':todoitems})
    else:
        title=request.POST.get('title')
        description=request.POST.get('description')
        customer_id = request.session.get('customer_id')
       
        todo=Todo(
                title=title,
                description=description,
                customer_id=customer_id,
                
            )
        todo.save()
        return redirect('todo') 
    


def delete(request , id ):
    Todo.objects.get(pk=id).delete()
    return redirect('todo')



def change(request , id ):
    todo=Todo.objects.get(pk=id)
    todo.status = True
    todo.save()
    print(todo.status)
    return redirect('todo')

