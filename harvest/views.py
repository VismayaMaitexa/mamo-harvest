from django.shortcuts import render
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import  authenticate,login
from django.shortcuts import render,redirect,reverse
from .import forms,models
from django.contrib.auth.models import Group
from .models import Quantities


# Create your views here.
def index(request):
    return render(request,'index.html')




        #LOGIN PAGE OF ADMIN , FARMER , USER
#farmer register /login  
def farmerclick_view(request):
    return render(request,'farmerclick.html')
#user register /login
def userclick_view(request):
    return render(request,'userclick.html')
#admin register
def adminclick_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username == 'Admin' and password == '12345':
            user = User.objects.filter(username=username).first()

            if user is None:
                user = User.objects.create_user(username=username, password=password)
                
            login(request, user)
            return redirect('admin-home')
        else:
            return render(request, "adminclick.html", {'error_message': 'Invalid username or password'})

    return render(request, 'adminclick.html')





#farmer register
def farmerregister(request):
    userForm = forms.FarmerUserForm()
    farmerForm = forms.FarmerForm()
    mydict = {'userForm': userForm, 'farmerForm': farmerForm}
    
    if request.method == 'POST':
        userForm = forms.FarmerUserForm(request.POST)
        farmerForm = forms.FarmerForm(request.POST, request.FILES)  
        
        if userForm.is_valid() and farmerForm.is_valid():
            try:
                user = userForm.save(commit=False)
                user.set_password(user.password) 
                user.save()
                
                farmer = farmerForm.save(commit=False)
                farmer.user = user
                farmer.save()
                
                my_farmer_group, created = Group.objects.get_or_create(name='FARMER')
                my_farmer_group.user_set.add(user)

                return redirect('farmerlogin')  
            
            except IntegrityError:
                userForm.add_error('username', 'This username is already taken. Please choose a different one.')
    
    return render(request, 'farmerregister.html', context=mydict)






#farmer edit

from django.db import IntegrityError
from .models import Farmer  
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required


from django.shortcuts import render, redirect

from django.http import Http404
@login_required

def update_farmer(request, pk):
    try:
        farmer = models.Farmer.objects.get(id=pk)
        user = models.User.objects.get(id=farmer.user_id)
    except models.Farmer.DoesNotExist:
        raise Http404("Farmer not found")
    except models.User.DoesNotExist:
        raise Http404("User not found")

    userForm = forms.FarmerUserForm(instance=user)
    farmerForm = forms.FarmerForm(request.FILES, instance=farmer)  

    mydict = {'userForm': userForm, 'farmerForm': farmerForm}

    if request.method == 'POST':
      
        userForm = forms.FarmerUserForm(request.POST, instance=user)
        farmerForm = forms.FarmerForm(request.POST, request.FILES, instance=farmer)  

       
        if userForm.is_valid() and farmerForm.is_valid():
            user = userForm.save(commit=False) 
            
            if userForm.cleaned_data.get('password'):
                user.set_password(userForm.cleaned_data['password']) 
            user.save()  
       
            farmerForm.save()

            return redirect('farmer') 
        else:
           
            print("User Form Errors:", userForm.errors)
            print("Farmer Form Errors:", farmerForm.errors)

    return render(request, 'admin_edit_farmer.html', context=mydict)


 




#farmer login

def farmerloginview(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            
            return redirect('farmer_dashboard') 
        else:
            return render(request, 'farmerlogin.html', {'error': 'Invalid credentials'}) 
              
    return render(request,'farmerlogin.html')



#userregister dashboard
from . models import Customer       

def userregisterview(request):

    userForm = forms.CustomerUserForm()

    customerForm = forms.CustomerForm()
    mydict = {'userForm': userForm, 'customerForm': customerForm}
    
    if request.method == 'POST':
        userForm = forms.CustomerUserForm(request.POST)
        customerForm = forms.CustomerForm(request.POST, request.FILES) 
        
        if userForm.is_valid() and customerForm.is_valid():
            try:
                user = userForm.save(commit=False)
                user.set_password(user.password) 
                user.save()
                
                customer = customerForm.save(commit=False)
                customer.user = user
                customer.save()
                
                my_customer_group, created = Group.objects.get_or_create(name='CUSTOMER')
                my_customer_group.user_set.add(user)

                return redirect('userlogin')  
            
            except IntegrityError:
                userForm.add_error('username', 'This username is already taken. Please choose a different one.')
    
    return render(request, 'userregister.html', context=mydict)



#edit user

@login_required
def update_user(request, pk):
    customer = models.Customer.objects.get(id=pk)
    user = models.User.objects.get(id=customer.user_id)
    
    userForm = forms.CustomerUserForm(instance=user)
    customerForm = forms.CustomerForm(request.FILES, instance=customer) 
    
    mydict = {'userForm': userForm, 'customerForm': customerForm}

    if request.method == 'POST':
        userForm = forms.CustomerUserForm(request.POST, instance=user)
        customerForm = forms.CustomerForm(request.POST, request.FILES, instance=customer) 

        if userForm.is_valid() and customerForm.is_valid():
            user = userForm.save(commit=False) 

            if userForm.cleaned_data.get('password'):
                user.set_password(userForm.cleaned_data['password'])
            user.save() 

            customerForm.save()

            return redirect('user')  
        else:
            print("User Form Errors:", userForm.errors)
            print("Customer Form Errors:", customerForm.errors)

    return render(request, 'admin_edit_user.html', context=mydict)



    #admin login page

from django.contrib.auth import login
from django.contrib.auth.models import User

def adminlogin(request):
    return render(request, "admindashboard.html")


#admin_login_page(dashboard)


from .models import Booking

#oder history of all users to the admin


def order(request):
    orders = Booking.objects.all().order_by('-date') 
    return render(request,'order.html',{'orders': orders})



#farmer in admin dashboard 

def farmer(request):
    farmers=models.Farmer.objects.all()
    print(farmers)
    return render(request,'admindashboard-farmer.html',{'farmers':farmers})


#delet farmer
def delete_farmer_from_event_view(request,pk):
    farmers=models.Farmer.objects.get(id=pk)
    farmers.delete()
    return redirect ('farmer')

#user in admin dashboard    

def user(request):
    users=models.Customer.objects.all()
    print(users)
    return render(request,'admindashboard-user.html',{'users':users})


#delete user
def delete_user_from_event_view(request,pk):
    users=models.Customer.objects.get(id=pk)
    users.delete()
    return redirect('user')



#admin feedback view

from django.contrib.auth.decorators import login_required
@login_required
def Feedbacks(request):
    feedbacks = Feedback.objects.all().order_by('-created_at')

    return render(request, 'adminfeedback.html', {'feedbacks': feedbacks})

#home page 
   
def log_out(request):
    return render(request,'log.html')


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

#user login

def userloginview(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            
            return redirect('user_dashboard') 
        else:
            return render(request, 'userlogin.html', {'error': 'Invalid credentials'})

    return render(request, 'userlogin.html')


#userdashboard page
def user_dashboardview(request):
    return render(request,'user_dashboard.html')


#farmer dashboard page
def farmer_dashboardview(request):
    
    return render(request,'farmer_dashboard.html')

#profile of farmer
def farmer_profile(request):
    try:
        farmer = Farmer.objects.get(user=request.user)
    except Farmer.DoesNotExist:
        farmer = None
    return render(request,'farmer_profile.html', {'farmer': farmer})


#farmer profile update
from .forms import FarmerUpdateForm 

@login_required
def update_farmer_profile(request):
    try:
        farmer = Farmer.objects.get(user=request.user)
    except Farmer.DoesNotExist:
        return redirect('farmer_profile')

    if request.method == 'POST':
        form = FarmerUpdateForm(request.POST, request.FILES, instance=farmer)
        if form.is_valid():
            form.save()
            return redirect('farmer_profile')  
    else:
        form = FarmerUpdateForm(instance=farmer)

    return render(request, 'update_farmer_profile.html', {'form': form})

#crop prediction for farmers    




import numpy as np
import pickle

# Load the model and scalers at thepkl module level
model = pickle.load(open(r'D:\MY PROJECT-VISMAYA\MAMO_PROJECTS\ecomerce harvest1 (2)\ecomerce harvest1\ecomerce harvest\model.pkl','rb'))
sc = pickle.load(open(r'D:\MY PROJECT-VISMAYA\MAMO_PROJECTS\ecomerce harvest1 (2)\ecomerce harvest1\ecomerce harvest\standscaler.pkl', 'rb'))
ms = pickle.load(open(r'D:\MY PROJECT-VISMAYA\MAMO_PROJECTS\ecomerce harvest1 (2)\ecomerce harvest1\ecomerce harvest\minmaxscaler.pkl', 'rb'))

def managecrops(request):
    if request.method == 'POST':
        N = request.POST['Nitrogen']
        P = request.POST['Phosporus']
        K = request.POST['Potassium']
        temp = request.POST['Temperature']
        humidity = request.POST['Humidity']
        ph = request.POST['Ph']
        rainfall = request.POST['Rainfall']

        feature_list = [N, P, K, temp, humidity, ph, rainfall]
        single_pred = np.array(feature_list).reshape(1, -1)

        # Apply the scalers to the input features
        scaled_features = ms.transform(single_pred)
        final_features = sc.transform(scaled_features)
        prediction = model.predict(final_features)

        crop_dict = {1: "Rice", 2: "Maize", 3: "Jute", 4: "Cotton", 5: "Coconut", 6: "Papaya", 7: "Orange",
                     8: "Apple", 9: "Muskmelon", 10: "Watermelon", 11: "Grapes", 12: "Mango", 13: "Banana",
                     14: "Pomegranate", 15: "Lentil", 16: "Blackgram", 17: "Mungbean", 18: "Mothbeans",
                     19: "Pigeonpeas", 20: "Kidneybeans", 21: "Chickpea", 22: "Coffee"}

        if prediction[0] in crop_dict:
            crop = crop_dict[prediction[0]]
            result = "{} is the best crop to be cultivated right there".format(crop)
        else:
            result = "Sorry, we could not determine the best crop to be cultivated with the provided data."

        return render(request, 'manage_crops.html', {'result': result})

    return render(request, 'manage_crops.html')
 
def orders(request, farmer_id):
    product_id = request.GET.get('product_id')  # Get product_id from query parameters

    # Filter orders for the specific farmer (using the correct field name)
    if product_id:
        orders = Booking.objects.filter(product_id=product_id, customer_id=farmer_id).order_by('-date')
    else:
        orders = Booking.objects.filter(customer_id=farmer_id).order_by('-date')

    return render(request, 'farmerorders.html', {'orders': orders})



#product adding and viewing page for farmer    
def products(request):
    return render(request,'farmerproducts.html')

#feedback viewing for farmer(specified)    

def product_feedback(request, id):
    print(request.user)
    product = get_object_or_404(Product, id=id)
    farmer = get_object_or_404(Farmer,user=request.user)
    feedbacks=Feedback.objects.filter(product=product)
    return render(request, 'farmerfeedback.html', {'feedbacks': feedbacks})

#home page

def log_out(request):
    return render(request,'log.html')


#user_dashboard_page

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from . import models

@login_required
def myorders(request):
    if request.user.is_authenticated:
        # Fetch all orders for the authenticated user
        orders = models.Booking.objects.filter(customer__user=request.user).prefetch_related('products')

        # Calculate the total price for each order
        for order in orders:
            total_price = 0  # Initialize total price for the order
            # Calculate subtotal for each product in the order and add it to the total price
            for product in order.products.all():
                # Calculate the subtotal for each product (product price * product quantity)
                subtotal = product.product.price * product.quantities
                total_price += subtotal  # Add the product's subtotal to the total price

                product.subtotal = subtotal  # Store the subtotal on the product (not required to store in DB)

            order.total_price = total_price

        print("Orders:", orders)
        print("Orders with total prices:", [order.total_price for order in orders])

        context = {
            'orders': orders
        }

        return render(request, 'my_orders.html', context)
    
    else:
        return redirect('userlogin')  # Redirect to login page if user is not authenticated



#product viewing page for user

def product(request):
    query = request.GET.get('search', '')  # Get search query from the URL

    if request.user.is_authenticated:
        # Get the district of the logged-in user (Customer's district)
        try:
            user_district = request.user.customer.district  # Access the district from the Customer model
        except Customer.DoesNotExist:
            user_district = None
        
        if user_district:
            # Filter products based on the district of the farmer
            products = Product.objects.filter(user__farmer__district=user_district)  # Only products from farmers in the same district
            
            # Apply the search filter if there's a query
            if query:
                products = products.filter(name__icontains=query)
        else:
            # If the user doesn't have a district or the district is None
            products = Product.objects.none()  # Return an empty queryset if no district info is available
    else:
        # If the user is not authenticated, return no products
        products = Product.objects.none()

    return render(request, 'userproduct.html', {'product': products})



def ordertracking(request):
    

    return render(request,'ordertracking.html')



#profile of a user 
def profile(request):
    try:
        customer = Customer.objects.get(user=request.user)
    except Customer.DoesNotExist:
        customer = None  
    return render(request,'profile.html',{'customer': customer})



#profile update for user
from .forms import CustomerUpdateForm

@login_required
def update_profile(request):
    customer = Customer.objects.get(user=request.user)

    if request.method == 'POST':
        form = CustomerUpdateForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = CustomerUpdateForm(instance=customer)

    return render(request, 'update_profile.html', {'form': form})



#feed back submition for user
from .forms import FeedbackForm
from .forms import Feedback

def feedback_form(request, product_id):
    product=get_object_or_404(Product,id=product_id) 
    return render(request,'feedback_form.html',{'product':product})

def add_feedback(request):
    print('the function is working')
    if request.method == 'POST' :
        product_id=request.POST.get('product_id')
        product=Product.objects.get(id=product_id)
        comment=request.POST.get('comment')
        print(comment,'show comment;')
        data=request.POST.copy()
        data['comments']=comment

        customer = get_object_or_404(Customer,user=request.user)
        if Feedback.objects.filter(Customer=customer,product=product).exists():
            raise Http404("You have already given feedback for this product.")
        
        form = FeedbackForm(data)
        if form.is_valid():
            Feedback.objects.create(
                Customer=customer,
                product=product,
                comments=comment
            )
        else:
            print(form.errors)
    return redirect('product') 


#home page

def log_out(request):
    return render(request,'log.html')

#farmer_product_addproduct

from django.shortcuts import render, redirect
from .forms import ProductForm
@login_required  
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.user = request.user 
            product.save()  
            return redirect('viewproduct') 
    else:
        form = ProductForm()
    
    return render(request, 'add_product.html', {'form': form})


#farmer_product_viewprodt
from django.contrib.auth.decorators import login_required
from .models import Product

@login_required  
def view_products(request):
   
    products = Product.objects.filter(user=request.user)
    return render(request, 'view_products.html', {'products': products})


#delet products
def delete_product_view(request, pk):
  
    products=models.Product.objects.get(id=pk)
    
   
    products.delete()
    
    return redirect('viewproduct')





#farmer_product_view_edit

def edit_product_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('viewproduct')  
    else:
        form = ProductForm(instance=product)
    
    return render(request, 'edit_product.html', {'form': form, 'product': product})



# add to cart     
from django.contrib import messages


def add_cart(request, pk):
    if not request.user.is_authenticated:
        messages.info(request, "Please log in to add products to your cart.")
        return redirect('userproduct') 
    if 'cart' not in request.session:
        request.session['cart'] = {}

    product = models.Product.objects.get(id=pk)

    
    if str(pk) in request.session['cart']:
        request.session['cart'][str(pk)] += 1
    else:
        request.session['cart'][str(pk)] = 1

    request.session.modified = True

    product_count_in_cart = sum(request.session['cart'].values())

    messages.info(request, f"{product.name} added to cart successfully.")
    
    products = models.Product.objects.all()  
    return render(request, 'userproduct.html', {'products': products, 'product_count_in_cart': product_count_in_cart})


def view_cart(request):
    product_count_in_cart = 0
    products = []
    total = 0

    # Check if the cart exists in the session
    if 'cart' in request.session:
        cart = request.session['cart']
        product_ids = cart.keys()  # Get product IDs from the cart
        products = models.Product.objects.filter(id__in=product_ids)  # Fetch products from DB

        for p in products:
            quantity = cart.get(str(p.id), 0)  # Get quantity from cart
            total += p.price * quantity  # Calculate total
            product_count_in_cart += quantity  # Calculate product count

    return render(request, 'view_cart.html', {
        'products': products,
        'product_count_in_cart': product_count_in_cart,
        'total': total
    })


def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    if str(product_id) in cart:
        del cart[str(product_id)]
    request.session['cart'] = cart
    return redirect('view_cart')


# def update_cart_quantity(request, product_id):
#     if request.method == 'POST':
#         quantity = int(request.POST.get('quantity', 1))  # Get new quantity from the form
#         if 'cart' in request.session:
#             cart = request.session['cart']
#             if str(product_id) in cart:
#                 if quantity > 0:
#                     cart[str(product_id)] = quantity  # Update quantity
#                 else:
#                     del cart[str(product_id)]  # Remove product if quantity is 0
#                 request.session['cart'] = cart  # Save updated cart to session
#     return redirect('view_cart') 


import random
import string

def generate_order_id(prefix='ORD', length=12):
    characters = string.ascii_uppercase + string.digits  
    random_length = length - len(prefix)  # Calculate the remaining length for random characters
    order_id = prefix

    for _ in range(random_length):
        order_id += random.choice(characters)

    return order_id

#view for booking
@login_required
def proced_user_checkout(request):
    data=request.POST.copy()
    data['status']='PENDING'
    form = forms.BookingForm(data)
    customer=get_object_or_404(Customer,user=request.user)
    products=ProductsWithQuantity.objects.filter(user=request.user).first().product_with_quantity
    
    quantity_list=[]
    for key,value in products.items():
        product=Product.objects.get(id=key)
        quantity_list.append(Quantities.objects.create(product=product,quantities=value))
        if request.method == 'POST' and product:
            product.quantity=product.quantity-value if product.quantity-value>0 else 0
            product.save()
    if request.method == 'POST':
        print("Processing POST request")
        if form.is_valid():
            history=form.save()
            for item in quantity_list:
                history.products.add(item)

            order_id = generate_order_id(prefix='ORD', length=16) 
            history.customer=customer
            history.tracking_number=order_id
            history.save()
            return render(request,'confirm_pay.html')
        else:
            print("Form is invalid:", form.errors)
    return render(request, 'proced_to_checkout.html', {'form': form})


def update_order_status(request, order_id):
    order = get_object_or_404(Booking, id=order_id)

    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status:
            order.status = new_status
            order.save()

    return redirect('order') 


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import ProductsWithQuantity


@csrf_exempt
def update_cart(request):
    print('not post')
    if request.method == 'POST':
        print(request.body)
        try:
            # Parse the JSON data from the request body
            data = json.loads(request.body)
            obj,_=ProductsWithQuantity.objects.get_or_create(user=request.user)
            obj.product_with_quantity=data
            obj.save()
            
        except Exception as e:
            return JsonResponse({'status': str(e), 'message': 'Invalid JSON data.'}, status=400)

        return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=405)



#paymet page
from .forms import PaymentForm

@login_required
def confirm_payment(request):
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        
        if form.is_valid():
            form.save()
            messages.success(request, "Payment processed successfully.")
            return redirect('credits_payment_done')  
        else:
            messages.error(request, "There was an error processing the payment.")
    else:
        form = PaymentForm()

    return render(request, 'proced_to_checkout.html', {'form': form})




#payment succesful page
        
def credit_payment(request):
    return render(request,'payment_credit.html')



from .models import Wishlist
from django.http import JsonResponse

@login_required
def add_to_wishlist(request, product_id):
    product = Product.objects.get(id=product_id)
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    
    if product in wishlist.products.all():
        wishlist.products.remove(product)
        added = False
    else:
        wishlist.products.add(product)
        added = True

    wishlist.save()

    return JsonResponse({'success': True, 'added': added})


# view page of whishlist
@login_required
def view_wishlist(request):
    wishlist = Wishlist.objects.get(user=request.user)
    return render(request, 'wishlist.html', {'wishlist': wishlist})



