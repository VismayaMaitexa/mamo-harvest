from django.contrib import admin 
from .models import Product
from . models import Farmer,Feedback
from . models import Customer,Booking,Payment,Quantities,ProductsWithQuantity
# Register your models here.
admin.site.register(Farmer)
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Booking)
admin.site.register(Feedback)
admin.site.register(Payment)
admin.site.register(Quantities)
admin.site.register(ProductsWithQuantity)