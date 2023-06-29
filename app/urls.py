from django.urls import path
from app import views


urlpatterns = [
    path('',views.home),
    path('register',views.register),
    path('login',views.user_login),
    path('verifyscreen/<rid>',views.verifyscreen),
    path('verifyotp/<rid>',views.verifyotp),
    path('base',views.reuse),
    path('addproduct',views.addproduct),
    path('delproduct/<rid>',views.delproduct),
    path('editproduct/<rid>',views.editproduct),
    path('sort/<sv>',views.sort),
    path('catfilter/<catv>',views.catfilter),
    path('pricefilter/<pv>',views.pricefilter),
    path('pricerange',views.pricerange),
    path('product_details/<pid>',views.product_details),
    path('cart/<pid>',views.addtocart),
    path('logout',views.user_logout),
    path('viewcart',views.viewcart),
    path('changeqty/<pid>/<f>',views.changeqty),
    path('placeorder',views.placeorder),
    path('payment',views.makepayment),
    path('store',views.storedetails),

]
