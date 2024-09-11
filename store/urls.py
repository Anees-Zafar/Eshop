from django.urls import path , include
from . import views
from .middleware.auth import auth_middleware
urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('signup', views.Signup , name='signup'),
    path('login', views.Login.as_view() , name='login'),
    path('logout', views.logout , name='logout'),
    path('cart', auth_middleware(views.cart) , name='cart'),
    path('checkout', views.checkout , name='checkout'),
    path('orders', views.orders , name='orders'),
    path('male', views.Malecatageory.as_view() , name='male'),
    path('female', views.Femalecatageory.as_view() , name='female'),
    path('kid', views.Kidcatageory.as_view() , name='kid'),
    path('paypalpage', views.paypalpage , name='paypalpage'),
    path('paypal/success/', views.paypal_success, name='paypal_success'),
    path('paypal/failed/', views.paypal_failed, name='paypal_failed'),
    # path('paypal/', include("paypal.standard.ipn.urls")),
    path('todo', views.todo, name='todo'),
    path('delete/<int:id>', views.delete, name='delete'),



]