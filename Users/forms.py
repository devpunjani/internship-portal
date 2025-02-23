from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import FeedbackModel
from .models import UserModel
from .models import StudentDetails
from .models import CompanyDetails

# User Register Form        
class UserRegisterForm(UserCreationForm):
    class Meta:
        model = UserModel
        fields = ('username','phone','email')  

# Feedback Form
class FeedbackForm(forms.ModelForm):
    class Meta:
        model = FeedbackModel
        fields = ('name','email','phone','message')
 