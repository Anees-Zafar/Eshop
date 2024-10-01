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
from django.template.loader import render_to_string
from django.db.models import Min , Max
import hashlib
from django.utils.html import strip_tags

@method_decorator(csrf_protect, name='dispatch')
class Index(View):
    def post(self , request):
        pass

    def get(self , request):
        if 'cartdata' not in request.session:
            request.session['cartdata'] = {}
       
                  
        male=Products.get_all_products_by_id(1)       
        female=Products.get_all_products_by_id(2) 
        kid=Products.get_all_products_by_id(3)
        customer_id = request.session.get('customer_id')
        profile=Profile.objects.filter(customer=customer_id)
               
        print ('you are:', request.session.get('email'))
        print(request.session['cartdata'])
        context = {'male': male , 'female':female , 'kid':kid , 'profile':profile }
        return render(request, 'index.html', context)


# shop view 
def shop(request):
    product =  Products.objects.all()
    collection=Products.objects.distinct().values('category__name', 'category__id')
    color=ProductAttribute.objects.distinct().values('color__title', 'color__id' , 'color__color_code')
    size=ProductAttribute.objects.distinct().values('size__title', 'size__id')
    minmaxprice=ProductAttribute.objects.aggregate(Min('price'), Max('price'))
    customer_id = request.session.get('customer_id')
    profile=Profile.objects.filter(customer=customer_id)
    # collection=Category.objects.all()
        
    collectionid=request.GET.get('category')
    if collectionid:
        product=Products.get_all_products_by_id(collectionid)
    # else:
    # product=Products.objects.all()

    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price:
        product = product.filter(price__gte=min_price)
        

    if max_price:
        product = product.filter(price__lte=max_price) 
                  
    # male=Products.get_all_products_by_id(1)       
    # female=Products.get_all_products_by_id(2) 
    # kid=Products.get_all_products_by_id(3)       
    print ('you are:', request.session.get('email'))
    print(request.session['cartdata'])
    context = {'product': product , 'category':collection , 'color':color , 'size':size , 'minmaxprice':minmaxprice , 'profile':profile}
    return render(request, 'shop.html', context)    
        
    
def base(request):
    customer_id = request.session.get('customer_id')
    profile=Profile.objects.filter(customer=customer_id)
    print(profile)
    return render(request , 'base.html' , {'profile':profile})


def productdetail(request,product_id):
    product = Products.objects.get(id=product_id)
    color = ProductAttribute.objects.filter(product=product).values('color__id', 'color__title', 'color__color_code').distinct()
    
    size = ProductAttribute.objects.filter(product=product).values('size__id', 'size__title' , 'price' , 'color__id').distinct()
    customer_id = request.session.get('customer_id')
    profile=Profile.objects.filter(customer=customer_id)
    context = {  'detail':product , 'color':color , 'size':size , 'profile':profile}

    return render(request,'productdetail.html', context )


def filterproducts(request):
    pagecategory = request.GET.get('pagecategory', None)
    color = request.GET.getlist('color[]')
    size = request.GET.getlist('size[]')
    category = request.GET.getlist('category[]')
    minprice=request.GET['minprice']
    maxprice=request.GET['maxprice']
    print(pagecategory)
    
    if pagecategory == '1':  # Ensure you compare with string '1' since GET parameters are strings
        allproducts = Products.objects.filter(category__id=1).distinct()
    elif pagecategory == '2':  # Ensure you compare with string '1' since GET parameters are strings
        allproducts = Products.objects.filter(category__id=2).distinct()
    elif pagecategory == '3':  # Ensure you compare with string '1' since GET parameters are strings
        allproducts = Products.objects.filter(category__id=3).distinct()        
    else:
        allproducts = Products.objects.all().distinct()


    allproducts=allproducts.filter(productattribute__price__gte=minprice)
    allproducts=allproducts.filter(productattribute__price__lte=maxprice)

    if len(color)>0:
        allproducts=allproducts.filter(productattribute__color__id__in=color).distinct()
    if len(size)>0:
        allproducts=allproducts.filter(productattribute__size__id__in=size).distinct()
    if len(category)>0:
        allproducts=allproducts.filter(category__id__in=category).distinct()    

    # if color:
    #     allproducts = allproducts.filter(color__id__in=color)
    # if size:
    #     allproducts = allproducts.filter(size__id__in=size)
    # if category:
    #     allproducts = allproducts.filter(category__id__in=category)

    t = render_to_string('productlist.html', {'data': allproducts})

    return JsonResponse({'data': t})



def addtocart(request):
    # del request.session['cartdata']
    product_id = request.GET['id']
    size = request.GET['size']
    color = request.GET['color']
    
    # Generate a unique key by hashing the product ID, size, and color
    unique_key = hashlib.md5(f"{product_id}_{size}_{color}".encode()).hexdigest()

    # Prepare the product data
    cart_p = {
        unique_key: {
            'title': request.GET['title'],
            'qty': int(request.GET['qty']),
            'price':float(request.GET['price'].replace('$', '')), 
            'color': color,
            'size': size,
        }
    }
    print(cart_p)
    # If there is existing cart data in the session
    if 'cartdata' in request.session:
        cart_data = request.session['cartdata']

        # If the exact product variation is already in the cart, update the quantity
        if unique_key in cart_data:
            cart_data[unique_key]['qty'] += int(cart_p[unique_key]['qty'])
        else:
            # Add the new variation to the cart
            cart_data.update(cart_p)

        request.session['cartdata'] = cart_data
    else:
        # If there is no cart data in the session, create a new cart
        request.session['cartdata'] = cart_p

    # Return the updated cart data and total items count
    return JsonResponse({'data': request.session['cartdata'], 'totalitems': len(request.session['cartdata'])})
        

def deletefromcart(request):
    id = request.POST.get('id')  # Use POST instead of GET
    if 'cartdata' in request.session:
        cart_data = request.session['cartdata']

        # Check if the item exists in the cart and delete it
        if id in cart_data:
            del cart_data[id]  # Delete the item from the cart

            # Update the session data
            request.session['cartdata'] = cart_data
            
    # Return the updated total items count
    return JsonResponse({'totalitems': len(request.session.get('cartdata', {}))})


def updatecartqty(request):
    if request.method == 'POST':
        unique_key = request.POST.get('product')
        removecome = request.POST.get('remove')  # This will be 'true' if it's a remove action
        
        if 'cartdata' in request.session:
            cart_data = request.session['cartdata']
            
            if unique_key in cart_data:
                if removecome:
                    # If the quantity is 1 or less, remove the item from the cart
                    if cart_data[unique_key]['qty'] <= 1:
                        cart_data.pop(unique_key)
                    else:
                        # Decrement the quantity
                        cart_data[unique_key]['qty'] -= 1
                
                else:
                    # Increment the quantity
                    cart_data[unique_key]['qty'] += 1

                # Update the session cart data
                request.session['cartdata'] = cart_data

                # Prepare response data
                updated_quantity = cart_data.get(unique_key, {}).get('qty', 0)
                cart_length = len(cart_data)  # Total items in cart


                if unique_key in cart_data:
                    item_price = cart_data[unique_key]['price']
                    item_total_price = updated_quantity * item_price

                    # Initialize total_price variable
                    total_price = 0
                    
                    # Recalculate the overall cart total price
                    for item in cart_data.values():
                        total_price += item['qty'] * item['price']

                    return JsonResponse({
                        'product_id': unique_key,
                        'quantity': updated_quantity,
                        'cart_length': cart_length,
                        'item_total_price': item_total_price,
                        'total_price': total_price,
                    })

           

        # Return an empty response if the product is not found in the cart
        return JsonResponse({'error': 'Product not found in cart.'}, status=400)

    return JsonResponse({'error': 'Invalid request method.'}, status=400)
            
             
        

    

@method_decorator(csrf_protect, name='dispatch')
class Malecatageory(View):
 
    def get(self , request):
        product = Products.get_all_products_by_id(1)
        collection=Products.objects.distinct().values('category__name', 'category__id')
        color=ProductAttribute.objects.distinct().values('color__title', 'color__id' , 'color__color_code')
        size=ProductAttribute.objects.distinct().values('size__title', 'size__id')
        minmaxprice=ProductAttribute.objects.aggregate(Min('price'), Max('price'))
        customer_id = request.session.get('customer_id')
        profile=Profile.objects.filter(customer=customer_id)
        # collection=Category.objects.all()
        
        collectionid=request.GET.get('category')
        if collectionid:
            product=Products.get_all_products_by_id(collectionid)
        # else:
        #     product=Products.objects.all()

        min_price = request.GET.get('min_price')
        max_price = request.GET.get('max_price')
        if min_price:
                product = product.filter(price__gte=min_price)
        

        if max_price:
                product = product.filter(price__lte=max_price) 
                  
           
        print ('you are:', request.session.get('email'))
        print(request.session['cartdata'])
        context = {'product': product , 'category':collection , 'color':color , 'size':size , 'minmaxprice':minmaxprice , 'profile':profile}
        
        return render(request, 'male.html', context)
    




@method_decorator(csrf_protect, name='dispatch')
class Femalecatageory(View):
    def get(self , request):
        product = Products.get_all_products_by_id(2)
        collection=Products.objects.distinct().values('category__name', 'category__id')
        color=ProductAttribute.objects.distinct().values('color__title', 'color__id' , 'color__color_code')
        size=ProductAttribute.objects.distinct().values('size__title', 'size__id')
        minmaxprice=ProductAttribute.objects.aggregate(Min('price'), Max('price'))
        customer_id = request.session.get('customer_id')
        profile=Profile.objects.filter(customer=customer_id)
        # collection=Category.objects.all()
        
        collectionid=request.GET.get('category')
        if collectionid:
            product=Products.get_all_products_by_id(collectionid)
        # else:
        #     product=Products.objects.all()

        min_price = request.GET.get('min_price')
        max_price = request.GET.get('max_price')
        if min_price:
                product = product.filter(price__gte=min_price)
        

        if max_price:
                product = product.filter(price__lte=max_price) 
                  
              
        print ('you are:', request.session.get('email'))
        print(request.session['cartdata'])
        context = {'profile':profile ,'product': product , 'category':collection , 'color':color , 'size':size , 'minmaxprice':minmaxprice}
        
        return render(request, 'female.html', context)



@method_decorator(csrf_protect, name='dispatch')
class Kidcatageory(View):
    

    def get(self , request):
        product = Products.get_all_products_by_id(3)
        collection=Products.objects.distinct().values('category__name', 'category__id')
        color=ProductAttribute.objects.distinct().values('color__title', 'color__id' , 'color__color_code')
        size=ProductAttribute.objects.distinct().values('size__title', 'size__id')
        minmaxprice=ProductAttribute.objects.aggregate(Min('price'), Max('price'))
        customer_id = request.session.get('customer_id')
        profile=Profile.objects.filter(customer=customer_id)
        # collection=Category.objects.all()
        
        collectionid=request.GET.get('category')
        if collectionid:
            product=Products.get_all_products_by_id(collectionid)
        # else:
        #     product=Products.objects.all()

        min_price = request.GET.get('min_price')
        max_price = request.GET.get('max_price')
        if min_price:
                product = product.filter(price__gte=min_price)
        

        if max_price:
                product = product.filter(price__lte=max_price) 
                  
              
        print ('you are:', request.session.get('email'))
        print(request.session['cartdata'])
        context = {'profile':profile , 'product': product , 'category':collection , 'color':color , 'size':size , 'minmaxprice':minmaxprice}
        
        return render(request, 'kid.html', context)




@requires_csrf_token
def Signup(request):
    if request.method=='GET':
        customer_id = request.session.get('customer_id')
        profile=Profile.objects.filter(customer=customer_id)
        return render(request, 'signup.html' , {'profile':profile})
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

        error=None 

        

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
        customer_id = request.session.get('customer_id')
        profile=Profile.objects.filter(customer=customer_id)
        Login.return_url = request.GET.get('return_url')
        return render(request, 'login.html' , {'profile':profile})
        
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



   

        
   


# password reset process functions start

def sendingemail(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        customer = Customer.get_customer_by_email(email)
        
        if customer:
            html_message = f"""
            <html>
                <body style="font-family: Arial, sans-serif; padding: 20px;">
                    <h2 style="color: #333;">Hey Dear Customer, {customer}!</h2>
                    <p>We received a request to reset your Eshop account password. If you didn't make this request, you can safely ignore this email.</p>
                    <p>To reset your password, please click the button below:</p>
                    <a href="http://127.0.0.1:8000/resetpassform/{customer.id}" style="background-color: #007bff; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; display: inline-block; margin-top: 10px;">Reset Password</a>
                    <p>If the button doesn't work, please copy and paste the following link into your browser:</p>
                    <p><a href="http://127.0.0.1:8000/resetpassform/{customer.id}">http://127.0.0.1:8000/resetpassform/{customer.id}</a></p>
                    <p style="color: #666;">Thank you,<br>The Eshop Team</p>
                </body>
            </html>
            """

            # Fallback plain-text version for email clients that do not support HTML
            plain_message = strip_tags(html_message)

            send_mail(
                "Recover Your Account ",
                plain_message,  # Plain text version
                EMAIL_HOST_USER,
                ['aneesdeveloper038@gmail.com'],  # The recipient's email
                fail_silently=True,
                html_message=html_message
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
        cart_data = request.session.get('cartdata', {})
        total_price = 0
        updated_cart_data = {}

        for key, item in cart_data.items():
            # Get product details from the database using the product title (or use an ID if available)
            try:
                products = Products.objects.filter(name=item['title'])
                if products.exists():
                    product = products.first()
                else:
                    continue      # Assuming key is the product ID
                color = Color.objects.get(id=item['color'])  # Assuming the color ID is stored in session
                item_price = float(item['price'])
                item['total_price'] = int(item['qty']) * item_price
                total_price += item['total_price']

                # Add the product image and color to the session data
                item['image'] = product.image.url
                item['color_code'] = color.color_code
                item['color_title'] = color.title
                updated_cart_data[key] = item

            except Products.DoesNotExist:
                continue
            except Color.DoesNotExist:
                continue
        customer_id = request.session.get('customer_id')
        profile=Profile.objects.filter(customer=customer_id)
        context = {
            'cart_data': updated_cart_data,
            'total_price': total_price,
            'profile':profile
        }
        return render(request, 'cart.html', context)
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
    profile=Profile.objects.filter(customer=customerlogin)

    orderitems = Order.get_orders(customerlogin)
    return render(request, 'orders.html', {'orderitems': orderitems , 'profile':profile})



def paypalpage(request):
    return render(request , 'paypal.html')



def paypal_success(request):
    return HttpResponse("Payment completed successfully!")

def paypal_failed(request):
    return HttpResponse("Payment failed. Please try again.")



def todo(request):
    if request.method=='GET':

        customerlogin = request.session.get('customer_id')
        profile=Profile.objects.filter(customer=customerlogin)
        todoitems=Todo.get_todos(customerlogin)
        return render(request , 'todo.html' , {'todoitems':todoitems , 'profile':profile})
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
    profile=Profile.objects.filter(customer=customerlogin)
    
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
        return render(request, 'customerprofile.html', {'customer': customer , 'prodata':prodata , 'profile':profile})
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
            profile=Profile.objects.filter(customer=customerlogin)
            return render(request, 'profileeditpage.html', {'customer': customer , 'prodata':prodata , 'profile':profile})
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

@csrf_exempt
def search(request):
    product=Products.objects.all()
    search=request.POST.get('search')
    search_result=product.filter(name__icontains=search)
    customerlogin = request.session.get('customer_id')
    profile=Profile.objects.filter(customer=customerlogin)
    return render(request , 'search.html' , {'search_result':search_result , 'search':search , 'profile':profile})