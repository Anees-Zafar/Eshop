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
    path('showorderconfirm', views.showorderconfirm , name='showorderconfirm'),
    
    # path('orders', views.orders , name='orders'),
    path('male', views.Malecatageory.as_view() , name='male'),
    path('female', views.Femalecatageory.as_view() , name='female'),
    path('kid', views.Kidcatageory.as_view() , name='kid'),
   
    path('todo', views.todo, name='todo'),
    path('delete/<int:id>', views.delete, name='delete'),
    path('change/<int:id>', views.change, name='change'),
    path('check-email', views.check_email, name='check_email'),
    path('sendingemail', views.sendingemail, name='sendingemail'),
    path('infoemailsend', views.infoemailsend, name='infoemailsend'),
    path('resetpassform/<int:id>', views.resetpassform, name='resetpassform'),
    path('customerprofile', views.customerprofile, name='customerprofile'),
    path('profileeditpage', views.profileeditpage , name='profileeditpage'),
    path('addreview' , views.addreview , name='addreview'),
    path('profiledeletepage', views.profiledeletepage , name='profiledeletepage'),
    path('search', views.search , name='search'),
    path('<int:product_id>' , views.productdetail , name='productdetail'),
    path('filterproducts' , views.filterproducts , name='filterproducts'),
    path('addtocart', views.addtocart , name='addtocart'),
    path('deletefromcart' , views.deletefromcart , name='deletefromcart'),
    path('updatecartqty' , views.updatecartqty , name='updatecartqty'),
    path('shop' , views.shop , name='shop'),
    path('base', views.base , name='base'),


    path('dashboard', views.dashboard , name='dashboard'),
    path('cartorder', views.cartorder , name='cartorder'),
    path('my_order_items/<int:id>',views.my_order_items,name='my_order_items'),
    path('cancelorder' , views.cancelorder , name='cancelorder'),
    path('reviewspage' , views.reviewspage , name='reviewspage'),
    path('contact',views.contact , name='contact')
 ]