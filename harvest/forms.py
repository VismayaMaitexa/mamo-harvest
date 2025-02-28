from django import forms
from django.contrib.auth.models import User
from . import models
class CustomerUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']
        widgets={
            'password':forms.PasswordInput()
        }
            
DISTRICTS = [
    ('district1', 'Alappuzha,'),
    ('district2', 'Ernakulam'),
    ('district3', 'Idukki'),
    ('district4', 'Kannur'),
    ('district5', 'Kasaragod'),
    ('district6', 'Kollam'),
    ('district7', 'Kottayam'),
    ('district8', 'Kozhikode'),
    ('district9', 'Malappuram '),
    ('district10', 'Palakkad'),
    ('district11', 'Pathanamthitta '),
    ('district12', 'Thiruvananthapuram'),    
    ('district13', 'Thrissur'),
    ('district14', 'Wayanad'),

]  

class CustomerForm(forms.ModelForm):
        district = forms.ChoiceField(choices=DISTRICTS)

        class Meta:
            model=models.Customer
            fields=['address','mobile','profile_pic','district']    


#form of farmer

class FarmerUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']
        widgets={
            'password':forms.PasswordInput()
        }
                    
DISTRICTS = [
    ('district1', 'Alappuzha,'),
    ('district2', 'Ernakulam'),
    ('district3', 'Idukki'),
    ('district4', 'Kannur'),
    ('district5', 'Kasaragod'),
    ('district6', 'Kollam'),
    ('district7', 'Kottayam'),
    ('district8', 'Kozhikode'),
    ('district9', 'Malappuram '),
    ('district10', 'Palakkad'),
    ('district11', 'Pathanamthitta '),
    ('district12', 'Thiruvananthapuram'),    
    ('district13', 'Thrissur'),
    ('district14', 'Wayanad'),

]  
class FarmerForm(forms.ModelForm):
        district = forms.ChoiceField(choices=DISTRICTS)

        class Meta:
            model=models.Farmer
            fields=['address','mobile','profile_pic','district','certificate']    


 #form for product    
      
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model =models.Product
        fields = ['name', 'description', 'price', 'quantity', 'category', 'image']
   
  #form for feedback 

     



from django import forms
from .models import Booking, Product  # Assuming you have a Product model

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = [
            'name', 'address', 'pincode', 'landmark',
            'mobile', 'status', 'tracking_number'
        ]
        widgets = {
            'products': forms.CheckboxSelectMultiple(), 
        }

    # Custom validation for mobile number (assuming it should be a 10-digit number)
    def clean_mobile(self):
        mobile = self.cleaned_data.get('mobile')
        if len(mobile) < 10:
            raise forms.ValidationError("Mobile number must be at least 10 digits.")
        return mobile

#profile update user
from django import forms
from .models import Customer

class CustomerUpdateForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=True, label="First Name")
    last_name = forms.CharField(max_length=30, required=True, label="Last Name")
    username = forms.CharField(max_length=150, required=True, label="Username")

    class Meta:
        model = Customer
        fields = ['profile_pic', 'address', 'mobile']  # Include the fields specific to the Customer model

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            # Assuming Customer has a One-to-One relation with User and you want to pre-fill user data
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name
            self.fields['username'].initial = user.username

    def save(self, commit=True):
        instance = super().save(commit=False)
        user = instance.user  # Assuming 'Customer' model has a 'user' field related to the User model
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.username = self.cleaned_data['username']
        if commit:
            user.save()  # Save user data
            instance.save()  # Save customer data
        return instance

#profile update of farmer
from .models import Farmer


class FarmerUpdateForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=True, label="First Name")
    last_name = forms.CharField(max_length=30, required=True, label="Last Name")
    username = forms.CharField(max_length=150, required=True, label="Username")

    class Meta:
        model = Farmer
        fields = ['profile_pic', 'address', 'mobile']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name
            self.fields['username'].initial = user.username

    def save(self, commit=True):
        instance = super().save(commit=False)
        user = instance.user
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.username = self.cleaned_data['username']
        if commit:
            user.save()
            instance.save()
        return instance
    

#form for payment
    
class PaymentForm(forms.ModelForm):
    class Meta:
        model =models.Payment
        fields = ['card_number', 'expiration_date', 'cv_code', 'card_owner']


# forms.py
from django import forms
from .models import Feedback, Product
from django.contrib.auth.models import User

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['product', 'comments']
        
        
    # Optionally, you can add a custom clean method to handle additional logic (e.g., for farmer)
    def __init__(self, *args, **kwargs):
        super(FeedbackForm, self).__init__(*args, **kwargs)
        # Adding dynamic choices for product based on user's context
        self.fields['product'].queryset = Product.objects.all()  # Assuming user has access to all products
    

from .models import Quantities

class QuantitiesForm(forms.ModelForm):
    class Meta:
        model = Quantities
        fields = ['product', 'quantities']
        widgets = {
            'product': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'Select Product'
            }),
            'quantities': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Quantities',
                'min': '1'
            }),
        }
        labels = {
            'product': 'Product',
            'quantities': 'Quantities',
        }