import datetime
from django.test import TestCase, Client
from django.urls import reverse
from .models import Products, Category, Customer, Order, Todo
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import User


class CategoryModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Shoes")

    def test_category_creation(self):
        self.assertTrue(isinstance(self.category, Category))
        self.assertEqual(str(self.category), "Shoes")


class ProductsModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Shoes")
        self.product = Products.objects.create(
            name="Running Shoes",
            price=100.00,
            description="High-quality running shoes",
            category=self.category,
            image= "Eshop\media\uploadedimages\kid2.jpg"
        )

    def test_product_creation(self):
        self.assertTrue(isinstance(self.product, Products))
        self.assertEqual(str(self.product), "Running Shoes")

    def test_imageURL_property(self):
        self.assertEqual(self.product.imageURL, "Eshop\media\uploadedimages\kid2.jpg")

    def test_get_all_products_by_id(self):
        products = Products.get_all_products_by_id(self.category.id)
        self.assertIn(self.product, products)

    def test_det_product_by_id(self):
        product = Products.det_product_by_id([self.product.id])
        self.assertIn(self.product, product)


class CustomerModelTest(TestCase):
    def setUp(self):
        self.customer = Customer.objects.create(
            first_name="John",
            last_name="Doe",
            phone="1234567890",
            email="john@example.com",
            password="hashedpassword123"
        )

    def test_customer_creation(self):
        self.assertTrue(isinstance(self.customer, Customer))
        self.assertEqual(str(self.customer), "John")

    def test_register(self):
        customer = Customer.objects.create(
            first_name="Jane",
            last_name="Doe",
            phone="0987654321",
            email="jane@example.com",
            password="hashedpassword321"
        )
        customer.register()
        self.assertTrue(Customer.objects.filter(email="jane@example.com").exists())

    def test_isExist(self):
        self.assertTrue(self.customer.isExist())

    def test_get_customer_by_email(self):
        customer = Customer.get_customer_by_email("john@example.com")
        self.assertEqual(customer.email, "john@example.com")


class OrderModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Shoes")
        self.product = Products.objects.create(
            name="Running Shoes",
            price=100.00,
            description="High-quality running shoes",
            category=self.category,
            image="uploadedimages/shoes.jpg"
        )
        self.customer = Customer.objects.create(
            first_name="John",
            last_name="Doe",
            phone="1234567890",
            email="john@example.com",
            password="hashedpassword123"
        )
        self.order = Order.objects.create(
            product=self.product,
            customer=self.customer,
            quantity=2,
            price=200,
            adress="123 Street, City",
            phone="1234567890",
            status=False,
            date=datetime.datetime.today()
        )

    def test_order_creation(self):
        self.assertTrue(isinstance(self.order, Order))
        self.assertEqual(str(self.order), "John")

    def test_place_order(self):
        self.order.place_order()
        self.assertTrue(Order.objects.filter(customer=self.customer).exists())

    def test_get_orders(self):
        orders = Order.get_orders(self.customer.id)
        self.assertIn(self.order, orders)


class TodoModelTest(TestCase):
    def setUp(self):
        self.customer = Customer.objects.create(
            first_name="John",
            last_name="Doe",
            phone="1234567890",
            email="john@example.com",
            password="hashedpassword123"
        )
        self.todo = Todo.objects.create(
            customer=self.customer,
            title="Finish project",
            description="Finish Django project",
            status=False,
            date=datetime.datetime.today()
        )

    def test_todo_creation(self):
        self.assertTrue(isinstance(self.todo, Todo))
        self.assertEqual(str(self.todo), "John")

    def test_get_todos(self):
        todos = Todo.get_todos(self.customer.id)
        self.assertIn(self.todo, todos)



class IndexViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(name="Shoes")
        self.product = Products.objects.create(name="Casual Shoes", category=self.category, price=50)

    def test_index_get(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_index_post_add_to_cart(self):
        session = self.client.session
        session['cart'] = {}
        session.save()
        
        response = self.client.post(reverse('index'), {'product': str(self.product.id)})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.client.session['cart'][str(self.product.id)], 1)



class MaleCategoryViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(name="Male Category")
        self.product = Products.objects.create(name="Male Shoes", category=self.category, price=100)

    def test_male_get(self):
        response = self.client.get(reverse('male'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'male.html')

    def test_male_post_add_to_cart(self):
        session = self.client.session
        session['cart'] = {}
        session.save()

        response = self.client.post(reverse('male'), {'product': str(self.product.id)})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.client.session['cart'][str(self.product.id)], 1)



class FemaleCategoryViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(name="Female Category")
        self.product = Products.objects.create(name="Female Shoes", category=self.category, price=80)

    def test_female_get(self):
        response = self.client.get(reverse('female'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'female.html')

    def test_female_post_add_to_cart(self):
        session = self.client.session
        session['cart'] = {}
        session.save()

        response = self.client.post(reverse('female'), {'product': str(self.product.id)})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.client.session['cart'][str(self.product.id)], 1)



class KidCategoryViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(name="Kid Category")
        self.product = Products.objects.create(name="Kid Shoes", category=self.category, price=60)

    def test_kid_get(self):
        response = self.client.get(reverse('kid'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'kid.html')

    def test_kid_post_add_to_cart(self):
        session = self.client.session
        session['cart'] = {}
        session.save()

        response = self.client.post(reverse('kid'), {'product': str(self.product.id)})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.client.session['cart'][str(self.product.id)], 1)


class SignupViewTest(TestCase):
    def test_signup_get(self):
        """
        Test that the GET request to the signup page returns the correct template.
        """
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'signup.html')

    def test_signup_post_valid(self):
        """
        Test the signup POST request with valid data.
        """
        response = self.client.post(reverse('signup'), {
            'firstname': 'John123',
            'lastname': 'Doe123',
            'phone': '1234567890',
            'email': 'john@example.com',
            'password': 'password123'
        })
        
        # Check for redirection to the login page after successful signup
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))

        # Verify that the customer was successfully created
        customer = Customer.objects.get(email='john@example.com')
        self.assertEqual(customer.first_name, 'John123')
        self.assertEqual(customer.last_name, 'Doe123')
        self.assertEqual(customer.phone, '1234567890')
        self.assertTrue(check_password('password123', customer.password))  # Check if the password is hashed

    def test_signup_post_invalid(self):
        """
        Test the signup POST request with invalid data (e.g., missing required fields).
        """
        response = self.client.post(reverse('signup'), {
            'firstname': '',  # Invalid first name
            'lastname': 'Doe',
            'phone': '1234567890',
            'email': 'john@example.com',
            'password': 'password123'
        })
        
        # The response should not redirect, meaning the form failed validation
        self.assertEqual(response.status_code, 200)
        
        # Check that the error message is present in the response
        self.assertContains(response, 'First name is required')

    def test_signup_post_existing_email(self):
        """
        Test the signup POST request with an existing email, which should return an error.
        """
        # Create an existing customer
        Customer.objects.create(
            first_name='Existing',
            last_name='User',
            phone='1234567890',
            email='john@example.com',
            password=make_password('password123')  # Already hashed password
        )

        # Attempt to create a new user with the same email
        response = self.client.post(reverse('signup'), {
            'firstname': 'John123',
            'lastname': 'Doe123',
            'phone': '1234567890',
            'email': 'john@example.com',  # Existing email
            'password': 'password123'
        })

        # The response should not redirect, meaning the form failed validation
        self.assertEqual(response.status_code, 200)
        
        # Check that the error message is present in the response
        self.assertContains(response, 'This Email ID already exists')



class LoginViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.customer = Customer.objects.create(
            first_name='John',
            last_name='Doe',
            phone='1234567890',
            email='john@example.com',
            password=make_password('password')
        )

    def test_login_get(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

    def test_login_post(self):
        response = self.client.post(reverse('login'), {'email': 'john@example.com', 'password': 'password'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.client.session['customer_id'], self.customer.id)





class CartViewTest(TestCase):
    
    def setUp(self):
        # Create a test customer
        self.client = Client()
        self.customer = Customer.objects.create(
            first_name="Test",
            last_name="User",
            email="testuser@example.com",
            phone="1234567890",
            password=make_password("testpassword")
        )

        # Log in the test customer
        login = self.client.post(reverse('login'), {
            'email': 'testuser@example.com',
            'password': 'testpassword'
        })
        self.assertEqual(login.status_code, 302)  # Ensure login was successful

        # Create a test category and products
        self.category = Category.objects.create(name="Test Category")
        self.product1 = Products.objects.create(name="Product 1", category=self.category, price=100)
        self.product2 = Products.objects.create(name="Product 2", category=self.category, price=150)
        
        # Simulate adding products to the cart in session
        session = self.client.session
        session['cart'] = {str(self.product1.id): 1, str(self.product2.id): 2}
        session.save()

    def test_cart_get_request(self):
        # Perform GET request to the cart view
        response = self.client.get(reverse('cart'))

        # Check if the status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Check if the products in the cart are returned correctly
        cartproducts = response.context['cartproducts']
        self.assertEqual(len(cartproducts), 2)
        self.assertIn(self.product1, cartproducts)
        self.assertIn(self.product2, cartproducts)

        # Check if the cart data is rendered correctly
        self.assertContains(response, self.product1.name)
        self.assertContains(response, self.product2.name)
   



class CartViewPostTest(TestCase):

    def setUp(self):
        # Create a test customer and log in
        self.client = Client()
        self.customer = Customer.objects.create(
            first_name="Test",
            last_name="User",
            email="testuser@example.com",
            phone="1234567890",
            password=make_password("testpassword")
        )

        # Log in the test customer
        login = self.client.post(reverse('login'), {
            'email': 'testuser@example.com',
            'password': 'testpassword'
        })
        self.assertEqual(login.status_code, 302)  # Ensure login was successful

        # Create a test category and products
        self.category = Category.objects.create(name="Test Category")
        self.product1 = Products.objects.create(name="Product 1", category=self.category, price=100)
        self.product2 = Products.objects.create(name="Product 2", category=self.category, price=150)
        
        # Simulate the initial cart state in session
        session = self.client.session
        session['cart'] = {str(self.product1.id): 1}  # 1 quantity of product1
        session.save()

    def test_add_product_to_cart(self):
        # Simulate adding a new product to the cart
        response = self.client.post(reverse('cart'), {
            'product': str(self.product2.id)  # Adding product2 to the cart
        })

        # Check if redirected back to the cart page
        self.assertEqual(response.status_code, 302)

        # Check if the product was added to the cart in the session
        session = self.client.session
        cart = session.get('cart')
        self.assertIn(str(self.product2.id), cart)  # Ensure product2 is in the cart
        self.assertEqual(cart[str(self.product2.id)], 1)  # Ensure quantity is set to 1

    def test_increase_product_quantity_in_cart(self):
        # Simulate increasing the quantity of an existing product (product1)
        response = self.client.post(reverse('cart'), {
            'product': str(self.product1.id)  # Increasing quantity of product1
        })

        # Check if redirected back to the cart page
        self.assertEqual(response.status_code, 302)

        # Check if the quantity of the product in the cart increased
        session = self.client.session
        cart = session.get('cart')
        self.assertEqual(cart[str(self.product1.id)], 2)  # Ensure quantity is now 2

    def test_remove_product_from_cart(self):
        # Simulate removing a product (product1) from the cart by reducing its quantity
        response = self.client.post(reverse('cart'), {
            'product': str(self.product1.id),
            'remove': True  # Remove one quantity of product1
        })

        # Check if redirected back to the cart page
        self.assertEqual(response.status_code, 302)

        # Check if the product was removed from the cart (since its quantity was 1)
        session = self.client.session
        cart = session.get('cart')
        self.assertNotIn(str(self.product1.id), cart)  # Ensure product1 was removed from the cart

    def test_remove_one_quantity_of_product_in_cart(self):
        # Add a product with quantity 2 first
        session = self.client.session
        session['cart'][str(self.product1.id)] = 2  # Set quantity of product1 to 2
        session.save()

        # Simulate removing one quantity of product1 (should remain in the cart with 1 quantity)
        response = self.client.post(reverse('cart'), {
            'product': str(self.product1.id),
            'remove': True  # Remove one quantity
        })

        # Check if redirected back to the cart page
        self.assertEqual(response.status_code, 302)

        # Check if the quantity of the product in the cart is reduced
        session = self.client.session
        cart = session.get('cart')
        self.assertEqual(cart[str(self.product1.id)], 1)  # Ensure quantity is now 1   


# class CheckoutViewTest(TestCase):

    
#     def setUp(self):
#         # Create a customer for testing
#         self.customer = Customer.objects.create(
#             first_name="John",
#             last_name="Doe",
#             phone="1234567890",
#             email="john@example.com",
#             password="testpassword"
#         )

#         # Create a category for the product
#         self.category = Category.objects.create(name="Test Category")

#         # Create a product for testing
#         self.product = Products.objects.create(
#             name="Test Product",
#             price=100.00,
#             description="A test product",
#             category=self.category,
#             image="path/to/image.jpg"
#         )

#         # Set up session data for the cart
#         self.client.session['cart'] = {str(self.product.id): 2}  # 2 units of the product
#         self.client.session['customer_id'] = self.customer.id
#         self.client.session.save()

#     def test_checkout_post(self):
#         # Make a POST request to the checkout view
#         response = self.client.post(reverse('checkout'), {
#             'adress': '123 Test Street',
#             'phone': '1234567890',
#         })

#         # Check that the response is a redirect to the orders page
#         self.assertRedirects(response, reverse('orders'))

#         # Check that an order was created
#         orders = Order.objects.filter(customer=self.customer, product=self.product)
#         self.assertEqual(orders.count(), 1)

#         # Check the order details
#         order = orders.first()
#         self.assertEqual(order.adress, '123 Test Street')
#         self.assertEqual(order.phone, '1234567890')
#         self.assertEqual(order.quantity, 2)  # Should match the cart quantity
#         self.assertEqual(order.price, self.product.price)