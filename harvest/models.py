from django.db import models
from django.contrib.auth.models import User

#models for user
class Customer(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic=models.ImageField(upload_to='profile_pic/CustomerProfilePic/',null=True,blank=True)
    address=models.CharField(max_length=40)
    mobile=models.CharField(max_length=20,null=False)
    district=models.CharField(max_length=40,null=True,blank=True)

 #models for farmer   
class Farmer(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic=models.ImageField(upload_to='profile_pic/FarmerProfilePic/',null=True,blank=True)
    address=models.CharField(max_length=40)
    mobile=models.CharField(max_length=20,null=False)
    district=models.CharField(max_length=40,null=True,blank=True)
    certificate=models.ImageField(upload_to='certificate/',null=True,blank=True)

#models for product
class Product(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)
    name = models.CharField(max_length=100)  
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)  
    quantity = models.PositiveIntegerField() 
    category = models.CharField(max_length=50) 
    image = models.ImageField(upload_to='products/', null=True, blank=True)


    #models for feedback

from django.db import models
def get_default_user():
    return User.objects.get(id=1)  

  



class Wishlist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, related_name="wishlist")

    def __str__(self):
        return f"Wishlist of {self.user.username}"
    
#model for payment

class Payment(models.Model):
    card_number = models.CharField(max_length=19)  
    expiration_date = models.CharField(max_length=5)  
    cv_code = models.CharField(max_length=3)  
    card_owner = models.CharField(max_length=100)    

# models.py

from django.db import models
from django.contrib.auth.models import User
from .models import Product, Farmer
from django.db import models
from django.contrib.auth.models import User
from .models import Product

class Feedback(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,null=True,blank=True)
    Customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='feedbacks_by_user',null=True,blank=True)  # Feedback by a user
    rating = models.PositiveIntegerField(null=True,blank=True)  # Rating from 1 to 5
    comments = models.TextField()  # Additional comments by the user
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp for when feedback is created

    def __str__(self):
        return f"Feedback for {self.product.name} by {self.Customer.user.username} (Rating: {self.rating})"
    


    from django.db import models
from datetime import datetime

class Booking(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('SHIPPED', 'Shipped'),
        ('DELIVERED', 'Delivered'),
        ('CANCELLED', 'Cancelled'),
    ]
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE,null=True,blank=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders',null=True,blank=True) 
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=40)
    pincode = models.CharField(max_length=6,null=False)
    landmark=models.CharField(max_length=100,null=False)
    mobile = models.CharField(max_length=20, null=False)
    products = models.ManyToManyField('Quantities', related_name='orders', blank=True) 
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')  
    date = models.DateTimeField(default=datetime.now) 
    tracking_number = models.CharField(max_length=100, blank=True, null=True) 
    total_price=models.PositiveBigIntegerField(null=True,blank=True)
    def __str__(self):
        return f"Order by {self.name} on {self.date}"

    def get_order_status(self):
        return self.status

    def get_order_total(self):
        return sum([product.product.price for product in self.products.all()]) 




class Quantities(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,null=True,blank=True)
    quantities=models.IntegerField(null=True,blank=True)


class ProductsWithQuantity(models.Model):   
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    product_with_quantity=models.JSONField(null=True,blank=True)