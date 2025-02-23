from django.db import models
from django.contrib.auth.models import AbstractUser
import re,os

from MyAdmin.models import IndustryModel as IndustryModel

#For Validation
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator,FileExtensionValidator


#Name Validator  
def validate_name(value):
    if not re.match(r'^[A-Za-z\s]+$', value):
        raise ValidationError("Name Can Only Contain Letters and Spaces.")

#Phone Validator
def validate_phone(value):
    phone_pattern = r'^[789]\d{9}$'
    if not re.match(phone_pattern, value):
        raise ValidationError("Please Enter A Valid Phone Number.")

#Resume Validator
def validate_studentResume(value):
    extension = os.path.splitext(value.name)[1].lower()
    allowed_extensions = ['.pdf']
    if extension not in allowed_extensions:
        raise ValidationError("Only PDF and DOCX Files Are Allowed For Resumes.")

# Student Details Model
class StudentDetails(models.Model):
    first_name = models.CharField(max_length=30,validators=[validate_name],blank=False)
    last_name = models.CharField(max_length=30,validators=[validate_name],blank=False)
    studentPhoto = models.ImageField(upload_to='Users/StudentPhoto/',validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])],blank=True)
    studentResume = models.FileField(upload_to='Users/StudentResume/',validators=[validate_studentResume],blank=True)
 
# Company Details Model   
class CompanyDetails(models.Model):
    company_name = models.CharField(max_length=30,blank=False)
    companyLogo = models.ImageField(upload_to='Users/CompanyLogo/',validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])],blank=True)

# User Model
class UserModel(AbstractUser):
    phone = models.CharField(max_length=10,validators=[validate_phone],unique=True)
    email = models.EmailField(validators=[EmailValidator(message="Please Enter A Valid Email Address.")],unique=True)
    StudentDetails = models.ForeignKey(StudentDetails, on_delete=models.CASCADE,null=True,blank=True)
    CompanyDetails = models.ForeignKey(CompanyDetails, on_delete=models.CASCADE,null=True,blank=True)
    user_type = models.SmallIntegerField(null=True,blank=True)
    verified = models.BooleanField(default=False)

    def __str__(self):
        return self.username    
    
# Feedback Model
class FeedbackModel(models.Model):
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    phone = models.CharField(max_length=10)
    message = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name

#Otp Model
class OtpModel(models.Model):
    student = models.ForeignKey('UserModel', on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    
    def __str__(self):
        return self.otp
    
class InternshipModel(models.Model):
    UserModel = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    IndustryModel = models.ForeignKey(IndustryModel, on_delete=models.CASCADE)
    title = models.CharField(max_length=500)
    location = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    skills = models.CharField(max_length=100,null=True,blank=True)
    description = models.CharField(max_length=200,null=True,blank=True)
    stipend = models.CharField(max_length=20)
    status = models.BooleanField(default=False)
    verified = models.BooleanField(default=False)
    
    def __str__(self):
        return self.title
    
class BookmarkModel(models.Model):
    UserModel = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    InternshipModel = models.ForeignKey(InternshipModel, on_delete=models.CASCADE)
    
class FeedbackStudentModel(models.Model):
    UserModel = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=30,blank=False)
    description = models.CharField(max_length=200,null=True,blank=True)
        
class CandidateModel(models.Model):
    student = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='student')
    internship = models.ForeignKey(InternshipModel, on_delete=models.CASCADE, related_name='internship')
    company = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='company')

    def __str__(self):
        return f"{self.student.id} - {self.internship.title}"