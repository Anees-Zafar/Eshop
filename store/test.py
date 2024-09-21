from django.test import TestCase
from .models import Category, Products, Customer, Order, Todo
import datetime

class CategoryModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Shoes")

    def test_category_creation(self):
        self.assertTrue(isinstance(self.category, Category))
        self.assertEqual(str(self.category), "Shoes")


# class ProductsModelTest(TestCase):
#     def setUp(self):
#         self.category = Category.objects.create(name="Shoes")
#         self.product = Products.objects.create(
#             name="Running Shoes",
#             price=100.00,
#             description="High-quality running shoes",
#             category=self.category,
#             image= "Eshop\media\uploadedimages\kid2.jpg"
#         )

#     def test_product_creation(self):
#         self.assertTrue(isinstance(self.product, Products))
#         self.assertEqual(str(self.product), "Running Shoes")

#     def test_imageURL_property(self):
#         self.assertEqual(self.product.imageURL, "Eshop\media\uploadedimages\kid2.jpg")

#     def test_get_all_products_by_id(self):
#         products = Products.get_all_products_by_id(self.category.id)
#         self.assertIn(self.product, products)

#     def test_det_product_by_id(self):
#         product = Products.det_product_by_id([self.product.id])
#         self.assertIn(self.product, product)


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