from django.urls import path
from . import views
urlpatterns = [
    path('',views.index,name="back"),
    path('register',views.index),
    #html page
    path('farmerclick',views.farmerclick_view,name='farmerclick'),
    path('userclick',views.userclick_view,name='userclick'),
    path('adminclick',views.adminclick_view,name='adminclick'),
    #farmclick_register
    path('farmerregister',views.farmerregister,name='farmerregister'),
    path('farmerlogin',views.farmerloginview,name='farmerlogin'),
    #userclick_register
    path('userregister',views.userregisterview,name='userregister'),
    path('userlogin',views.userloginview,name='userlogin'),

    path('admin-home',views.adminlogin,name='admin-home'),
    #admin_login_page
   
    path('orde/',views.order,name='order'),
    path('farm/',views.farmer,name='farmer'),
    path('registerfmrdlt/<int:pk>/',views.delete_farmer_from_event_view,name='delete-farmer'),
    #farner update
    path('update_farmer/<int:pk>/', views.update_farmer, name='update_farmer'),
    


    path('usr/',views.user,name='user'),
    path('registerusrdlt/<int:pk>/',views.delete_user_from_event_view,name='delete-user'),
   #user update
    path('update_user/<int:pk>/', views.update_user, name='update_user'),
    

    path('feedback/',views.Feedbacks,name='feedbacks'),
    path('log/',views.log_out,name='logout'),
    #user login page
    path('user_dashboard',views.user_dashboardview,name='user_dashboard'),
    #famermer login page
    path('farmer_dashboard',views.farmer_dashboardview,name='farmer_dashboard'),
    #farmerdashboard page
    path('frmrprfl/',views. farmer_profile,name='farmer_profile'),
#profile update of farmer

    path('farmer/update/', views.update_farmer_profile, name='update_farmer_profile'),

    path('mangcrp/',views.managecrops,name='managecrops'),
    path('farmer/<int:farmer_id>/orders/', views.orders, name='farmer_orders'),
    path('prod/',views.products,name='products'),
    path('product/<int:id>/feedback/', views.product_feedback, name='product-feedback'),
    path('logt/',views.log_out,name='logout'),
    #userdashboard page
    path('myodrs/',views.myorders,name='myorders'),
    path('prdt',views.product,name='product'),
    path('ordtrk/',views.ordertracking,name='ordertracking'),

    #profile for user
    path('prfl/',views.profile,name='profile'),
    #edit for profile
    path('update-profile/', views.update_profile, name='update_profile'),

    path('feedback-form/<int:product_id>/', views.feedback_form, name='feedback_form'),


    path('logt/',views.log_out,name='logout'),

#farmer_product_addprdt
    path('addproduct/', views.add_product, name='addproduct'),

#farmer_product_viewprdt    
    path('viewproduct/', views.view_products, name='viewproduct'),

#farmer_product_view_delet    

    path('delete-product/<int:pk>/', views.delete_product_view, name='delete-product'),

#farmer_product_view_edit

     path('edit-product/<int:pk>/', views.edit_product_view, name='edit-product'),

#add_cart
     path('add-cart/<int:pk>/', views.add_cart, name='addcart'),


#view_cart      
     path('cart/', views.view_cart, name='view_cart'),
     path('remove_from_cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),


    
#booking
    # path('payment',views.confirm_payment,name='payments'),
    path('payment', views.confirm_payment, name='payments'),

    path('cofirm payment/', views.credit_payment, name='credits_payment_done'), 
    path('proceed button/', views.proced_user_checkout, name='proceed button'),




#wishlist
    path('wishlist/add_remove/<int:product_id>/', views.add_to_wishlist, name='add_remove_wishlist'),
    path('wishlist/', views.view_wishlist, name='view_wishlist'),
    path('addfeedback/',views.add_feedback,name='add_feedback'),

    path('update-cart/', views.update_cart, name='update_cart'),

    path('update_status/<int:order_id>/', views.update_order_status, name='update_order_status')




  
]