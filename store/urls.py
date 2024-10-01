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
    path('change/<int:id>', views.change, name='change'),
    path('check-email', views.check_email, name='check_email'),
    # path('check-login', views.check_login, name='check_login'),
    # path('update_cart/', views.update_cart, name='update_cart'),
    path('sendingemail', views.sendingemail, name='sendingemail'),
    path('infoemailsend', views.infoemailsend, name='infoemailsend'),
    path('resetpassform/<int:id>', views.resetpassform, name='resetpassform'),
    path('customerprofile', views.customerprofile, name='customerprofile'),
    path('profileeditpage', views.profileeditpage , name='profileeditpage'),
    path('profiledeletepage', views.profiledeletepage , name='profiledeletepage'),
    path('search', views.search , name='search'),
    path('<int:product_id>' , views.productdetail , name='productdetail'),
    path('filterproducts' , views.filterproducts , name='filterproducts'),
    path('addtocart', views.addtocart , name='addtocart'),
    path('deletefromcart' , views.deletefromcart , name='deletefromcart'),
    path('updatecartqty' , views.updatecartqty , name='updatecartqty'),
    path('shop' , views.shop , name='shop'),
    path('base', views.base , name='base')

 ]