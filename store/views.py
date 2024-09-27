from django.shortcuts import render ,redirect , HttpResponseRedirect
from django.http import HttpResponse, JsonResponse
from .models import *
from django.contrib.auth.hashers import check_password, make_password
from django.views import View
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import requires_csrf_token
import json
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from Eshop.settings import EMAIL_HOST_USER
from django.shortcuts import get_object_or_404


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
        print(collection)
        collectionid=request.GET.get('category')
        if collectionid:
            product=Products.get_all_products_by_id(collectionid)
        else:
            product=Products.objects.all()
        # male=Products.get_all_products_by_id(1)       
        # female=Products.get_all_products_by_id(2) 
        # kid=Products.get_all_products_by_id(3)       
        print ('you are:', request.session.get('email'))
        print(request.session['cart'])
        context = {'product': product , 'category':collection }
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
        
   


# password reset process functions start

def sendingemail(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        customer = Customer.get_customer_by_email(email)
        print(customer.email)
        if customer:
            send_mail(
                "Recover Your Account ",
                f"Hey Dear Customer: {customer} . For reset your Eshop Account Password Click on \n http://127.0.0.1:8000/resetpassform/{customer.id} ",
                EMAIL_HOST_USER,
                [customer.email],
                fail_silently=True,
            )
            print('successful')
            return JsonResponse({'success': True, 'redirect_url': 'infoemailsend'})
        else:
            print('Customer not found')
            return JsonResponse({'success': False, 'error': 'Invalid email or customer does not exist.'})

    else:
        return redirect('login')  


def infoemailsend(request):
    return render(request, 'infoemailsend.html')               
              
            
def resetpassform(request,id):
    if request.method == 'POST':
        new_password = request.POST.get('new_password1')
        confirm_password = request.POST.get('new_password2')
        
        # Validate passwords
        # if not new_password or not confirm_password:
        #     return JsonResponse({'success': False, 'error': 'Both password fields are required.'}, status=400)
        # if new_password != confirm_password:
        #     return JsonResponse({'success': False, 'error': 'Passwords do not match.'}, status=400)
        
        # Fetch the customer by ID
        customer = get_object_or_404(Customer, id=id)

        # Set the new password
        customer.password = make_password(new_password)
        customer.save()

        return JsonResponse({'success': True, 'message': 'Password reset successful!'}, status=200)
    else:
        print(id)
        return render(request , 'resetpassform.html',{'user_id': id})



# password reset process function ends 



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






# profile view 

def customerprofile(request):
    customerlogin = request.session.get('customer_id')
    print(f"this is customer login {customerlogin}")

    if customerlogin:
       
        customer = Customer.objects.get(id=customerlogin)  # Fetch the customer by ID
        print(customer)
        try:
            prodata = Profile.objects.get(customer=customer)
        except:
            # Handle case where profile does not exist
            prodata = None  # Or redirect to a page where the profile can be created, etc.
            print("Profile does not exist for this customer")
        # prodata=Profile.objects.get(customer=customer)
        # print(prodata.cover_photo) 
        return render(request, 'customerprofile.html', {'customer': customer , 'prodata':prodata})
    else:
        print('No customer logged in')
        return redirect('login') 
    
@csrf_exempt
def profileeditpage(request):
    if request.method == 'POST':
        customer_id = request.session.get('customer_id')  # Get the logged-in customer's ID from session
        if customer_id:
            customer = Customer.objects.get(id=customer_id)  # Fetch the customer object
        else:
            return redirect('login')

        address = request.POST.get('address')
        about = request.POST.get('about')
        cover_photo = request.FILES.get('cover_photo')
        profile_photo = request.FILES.get('profile_photo')

        # Check if the customer already has a profile
        profile, created = Profile.objects.get_or_create(customer=customer)

        # Update profile information
        profile.address = address
        profile.about = about

        if cover_photo:
            profile.cover_photo = cover_photo
        if profile_photo:
            profile.profile_photo = profile_photo

        profile.save()

        if created:
            message = "Profile created successfully"
        else:
            message = "Profile updated successfully"

        return JsonResponse({'success': True, 'message': message}) 
    else:
        customerlogin = request.session.get('customer_id')
        print(f"this is customer login {customerlogin}")

        if customerlogin:
            customer = Customer.objects.get(id=customerlogin)  # Fetch the customer by ID
            print(customer)
            try:
                prodata = Profile.objects.get(customer=customer)
            except:
            # Handle case where profile does not exist
                prodata = None  # Or redirect to a page where the profile can be created, etc.
                print("Profile does not exist for this customer")
            # prodata=Profile.objects.get(customer=customer)
            # print(prodata.address)
            return render(request, 'profileeditpage.html', {'customer': customer , 'prodata':prodata})
        else:
            print('No customer logged in')
            return redirect('login') 
        # return render(request , '')    



def profiledeletepage(request):
    if request.method == 'POST':
        customer_id = request.session.get('customer_id')
        if not customer_id:
            return redirect('login')
        customer = Customer.objects.get(id=customer_id)
        try:
            profile = Profile.objects.get(customer=customer)
            profile.delete()  # Delete the profile
            return redirect('customerprofile')
        except Profile.DoesNotExist:
            return redirect('login')
        


  # Use csrf_exempt only for testing; it should be removed in production
# def profile_edit_view(request):
#     if request.method == 'POST':
#         address = request.POST.get('address')
#         about = request.POST.get('about')
        
#         cover_photo = request.FILES.get('cover_photo')
#         profile_photo = request.FILES.get('profile_photo')

#         # Assuming you have a Profile model linked to the user
#         profile = request.user.profile
#         profile.address = address
#         profile.about = about
        
#         if cover_photo:
#             profile.cover_photo = cover_photo
#         if profile_photo:
#             profile.profile_photo = profile_photo
        
#         profile.save()

#         return JsonResponse({'success': True})    