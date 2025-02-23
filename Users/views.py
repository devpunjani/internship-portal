from typing import Self
from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from django.contrib.auth.decorators import user_passes_test

import os
from django.conf import settings
from django.http import FileResponse
import random
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.core.mail import send_mail

# Models
from .models import UserModel as UserModel
from .models import StudentDetails as StudentDetails 
from .models import CompanyDetails as CompanyDetails
from .models import FeedbackModel as FeedbackModel
from .models import OtpModel as OtpModel
from .models import InternshipModel as InternshipModel
from MyAdmin.models import IndustryModel as IndustryModel
from .models import CandidateModel as CandidateModel
from .models import BookmarkModel as BookmarkModel
from .models import FeedbackStudentModel as FeedbackStudentModel

# Forms
from .forms import UserRegisterForm as UserRegisterForm
from .forms import FeedbackForm as FeedbackForm


from django.utils.decorators import method_decorator
from django.views import View

def is_student(user):
    return user.user_type == 1

def is_company(user):
    return user.user_type == 2

def Index(req):
    context={}
    student_count = UserModel.objects.filter(user_type=1).count()
    company_count = UserModel.objects.filter(user_type=2).count()
    internship_count = InternshipModel.objects.count()
    context = {'student_count': student_count,'company_count':company_count,'internship_count':internship_count}
    context["industries"] = IndustryModel.objects.all()
    context["internships"] = InternshipModel.objects.filter(status=1).order_by('-id')[:5]
    companies=UserModel.objects.filter(verified=1,user_type=2).order_by('-id')[:10]
    for company in companies:
        company.i_count = InternshipModel.objects.filter(UserModel_id=company.id).count()
        print(company.i_count)
    context["companies"] = companies

    return render(req,"Home.html",context)

# Student Register    
def StudentRegister(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            phone = form.cleaned_data['phone']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            
            first_name = request.POST.get('first_name') 
            last_name = request.POST.get('last_name')
            studentPhoto = request.FILES.get('studentPhoto')
            studentResume = request.FILES.get('studentResume')
            
            if studentPhoto:
                fs = FileSystemStorage(location='Users/StudentPhoto/')
                photo_filename = fs.save(studentPhoto.name, studentPhoto)

            if studentResume:
                fs = FileSystemStorage(location='Users/StudentResume/')
                resume_filename = fs.save(studentResume.name, studentResume)

            details = StudentDetails(
                first_name = first_name,
                last_name = last_name,
                studentPhoto=f'Users/StudentPhoto/{photo_filename}' if studentPhoto else '',
                studentResume=f'Users/StudentResume/{resume_filename}' if studentResume else '',
            )
            details.save()
            
            s = StudentDetails.objects.latest('id')
            
            data = UserModel(
                username = username,
                phone = phone,
                email = email,
                StudentDetails_id = s.id,
                user_type = 1,
                password = make_password(password)
            )
            data.save()

            subject = 'Student Registration Successful'
            message = 'Our team will verify your account soon.\nThank you for registering with us!'
            from_email = 'devpunjani2123@gmail.com'  
            recipient_list = [email]  
            send_mail(subject, message, from_email, recipient_list)

            return redirect('StudentLogin')  
    else:
        form = UserRegisterForm()
    return render(request, 'StudentRegister.html', {'form': form})

# Student Login
def StudentLogin(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None and user.user_type == 1 and user.is_superuser == 0 and user.verified == 1:    
                login(request, user)
                return redirect('Home')
            else:
                messages.error(request, 'Invalid Login Credentials OR Account Not Verified')
    else:
        form = AuthenticationForm()
    return render(request, 'StudentLogin.html',{'form': form})

@login_required
@user_passes_test(is_student)
def Bookmarks(request):
    context = {}
    context["bookmark"] = BookmarkModel.objects.filter(UserModel_id=request.user.id)
    print(context["bookmark"])
    return render(request,'Bookmarks.html',context)

@login_required
@user_passes_test(is_student)
def DeleteBookmark(request,id):
    #bookmark = get_object_or_404(BookmarkModel,id = id)
    bookmark = BookmarkModel.objects.filter(id=id)
    bookmark.delete()
    return redirect('Bookmarks')    

@login_required
@user_passes_test(is_student)
def Bookmark(request,id):
    internship = get_object_or_404(InternshipModel,id = id)
    obj = BookmarkModel(
        InternshipModel_id = internship.id,
        UserModel_id = request.user.id
    )
    obj.save()
    previous_page = request.META.get('HTTP_REFERER')
    return redirect(previous_page)
    

# Profile Page
@login_required
@user_passes_test(is_student)
def Profile(request):
    context ={}
    context["applied"] = CandidateModel.objects.filter(student_id=request.user.id)
    context["feedbacks"] = FeedbackStudentModel.objects.filter(UserModel_id=request.user.id)
    return render(request,"Profile.html",context)

# Delete Profile
def StudentDeleteProfile(request,id):
    try:
        user = UserModel.objects.get(id=id)
        student_details = user.StudentDetails  
    except UserModel.DoesNotExist:
        return redirect('Home')  

    user.delete()
    if student_details:
        file_path1 = f'{student_details.studentPhoto}'
        file_path2 = f'{student_details.studentResume}'
        fs = FileSystemStorage(location='')

        if fs.exists(file_path1): fs.delete(file_path1)
        if fs.exists(file_path2): fs.delete(file_path2)
        student_details.delete()
        
    return redirect('login')

# Edit Profile
@login_required
@user_passes_test(is_student)
def EditProfile(request,id):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = get_object_or_404(UserModel, id=id)
            student_details = user.StudentDetails
            
            username = form.cleaned_data['username']
            phone = form.cleaned_data['phone']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            
            user.username = username
            user.phone = phone
            user.email = email
            user.password = make_password(password)
            user.save()
            
            first_name = request.POST.get('first_name') 
            last_name = request.POST.get('last_name')
            studentPhoto = request.FILES.get('studentPhoto')
            studentResume = request.FILES.get('studentResume')
            
            if studentPhoto:
                fs = FileSystemStorage(location='Users/StudentPhoto/')
                photo_filename = fs.save(studentPhoto.name, studentPhoto)
                student_details.studentPhoto = f'Users/StudentPhoto/{photo_filename}'
                
            if studentResume:
                fs = FileSystemStorage(location='Users/StudentResume/')
                resume_filename = fs.save(studentResume.name, studentResume)
                student_details.studentResume = f'Users/StudentResume/{resume_filename}'

            student_details.first_name = first_name
            student_details.last_name = last_name
            
            student_details.save()
            
            messages.success(request, "Profile Updated Successfully.")
            return redirect('Profile')
    else:
        form = UserRegisterForm(instance=request.user)
    return render(request, 'ProfileEdit.html', {'form': form})

#View Resume
@login_required
@user_passes_test(lambda u: is_student(u) or is_company(u))
def StudentViewResume(request,filepath):
    pdf_path = os.path.join(settings.BASE_DIR, filepath)
    pdf_name = os.path.basename(pdf_path)
    response = FileResponse(open(pdf_path, 'rb'), content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="{pdf_name}"'
    return response

# Feedback
def StudentFeedback(request):
    if request.method == 'POST':  
        #return redirect('Home')      
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request,messages.INFO, 'Feedback Sent Successfully')
        return redirect('Home')
    else:
        form = FeedbackForm()
    return render(request, 'StudentFeedback.html',{'form': form})

# Send Otp
def SendOtp(request):
    if request.method == 'POST':
        
        check_email = request.POST.get('email',None)
        
        if check_email:
            try:
                user = UserModel.objects.get(email=check_email)
                user_id = user.id
                email = user.email
                
                if user_id is not None:
                    otp=random.randint(100000, 999999)
                    student_id=user_id
                    data=OtpModel(student_id=student_id,otp=otp)
                    data.save()
                    
                    last_record = OtpModel.objects.latest('id')
                    otp_id=last_record.id
                    
                    subject = 'InternSpot Forgot Password Otp'
                    message = 'Your Otp For Forgot Password Is : ' + str(otp)
                    from_email = 'devpunjani2123@gmail.com'  # Replace with your email
                    recipient_list = [email]  # Replace with the recipient's email

                    send_mail(subject, message, from_email, recipient_list)
                    return redirect('OtpVerify', otp_id) 
            except UserModel.DoesNotExist:
                messages.error(request, 'Email Not Found')
        else:
            messages.error(request, 'Enter Email !!')

        return render(request, 'SendOtp.html')
    else:
        return render(request, 'SendOtp.html') 
    
# Otp Verify
def OtpVerify(request,id):
    if request.method=='POST':
        first=request.POST.get('first')
        second=request.POST.get('second')
        third=request.POST.get('third')
        fourth=request.POST.get('fourth')
        fifth=request.POST.get('fifth')
        sixth=request.POST.get('sixth')
        
        otp_merge=first+second+third+fourth+fifth+sixth
        otp_data=OtpModel.objects.get(id=id)
        
        if otp_data.otp==otp_merge:
            return redirect('ResetPassword',otp_data.student_id)
        else:
            messages.error(request, 'Entered OTP Not Matched !!')    
            return redirect('OtpVerify',id) 
    else:
        return render(request,'OtpVerify.html')
    
# Reset Password
def ResetPassword(request,id):
    if request.method=='POST':
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        if password1==password2:
            stu=UserModel.objects.get(id=id)
            stu.password = make_password(password1)
            stu.save()
            messages.error(request,"Password Reset Successful")
            return redirect('StudentLogin')
        else:
            messages.error(request,"Password and Confirm Password Does Not Match !!")
            return redirect('ResetPassword',id)
    else:
        return render(request,'ResetPassword.html')
    
# Company Register 
def CompanyRegister(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            phone = form.cleaned_data['phone']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            
            company_name = request.POST.get('company_name')
            companyLogo = request.FILES.get('companyLogo')
            
            if companyLogo:
                fs = FileSystemStorage(location='Users/CompanyLogo/')
                photo_filename = fs.save(companyLogo.name, companyLogo)

            details = CompanyDetails(
                company_name = company_name,
                companyLogo=f'Users/CompanyLogo/{photo_filename}' if companyLogo else '',
            )
            details.save()
            
            c = CompanyDetails.objects.latest('id')
            
            data = UserModel(
                username = username,
                phone = phone,
                email = email,
                CompanyDetails_id = c.id,
                user_type = 2,
                password = make_password(password)
            )
            data.save()

            subject = 'Company Registration Successful'
            message = 'Our team will verify your company soon.\nThank you for registering with us!'
            from_email = 'devpunjani2123@gmail.com'  
            recipient_list = [email]  
            send_mail(subject, message, from_email, recipient_list)

            return redirect('CompanyLogin')  
    else:
        form = UserRegisterForm()
    return render(request, 'Company/Register.html', {'form': form})

# Company Login
def CompanyLogin(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None and user.user_type == 2 and user.is_superuser == 0 and user.verified == 1:    
                login(request, user)
                return redirect('CompanyDashboard')
            else:
                messages.error(request, 'Invalid Login Credentials OR Company Not Verified')
    else:
        form = AuthenticationForm()
    return render(request, 'Company/Login.html',{'form': form})

# Company Dashboard
user_passes_test(is_company)
def CompanyDashboard(request):
    internship_count = InternshipModel.objects.filter(UserModel_id=request.user.id).count()
    context = {'internship_count':internship_count}
    return render(request,"Company/Dashboard.html",context)


# View Internship
@login_required
@user_passes_test(is_company)
def ViewInternship(request):
    context = {}
    context["internships"] = InternshipModel.objects.filter(UserModel_id=request.user.id)
    
    return render(request,"Company/internship/InternshipView.html",context)

# Add Internship
@login_required
@user_passes_test(is_company)
def AddInternship(request):
    context = {}
    context["industries"] = IndustryModel.objects.all()
    
    if request.method == 'POST':
        data = InternshipModel(
            UserModel_id = request.user.id,
            IndustryModel_id = request.POST.get('industry'), 
            title = request.POST.get('title'),
            location = request.POST.get('location'),
            type = request.POST.get('type'),
            skills = request.POST.get('skills'),
            description = request.POST.get('description'), 
            stipend = request.POST.get('stipend')
        )    
        data.save()
        
        return redirect('ViewInternship')
    else:
        return render(request,"Company/internship/InternshipAdd.html",context)

# Delete Internship
@login_required
@user_passes_test(is_company)
def DeleteInternship(request,id):
    context={}
    obj = get_object_or_404(InternshipModel,id = id)
    if request.method == "GET":
        obj.delete()
        return redirect("ViewInternship")
    
    return render(request,"Company/internship/InternshipView.html",context)

# Edit Internship
@login_required
@user_passes_test(is_company)
def EditInternship(request,id):
    context = {}
    context["industries"] = IndustryModel.objects.all()
    
    obj = get_object_or_404(InternshipModel, id = id)
    context["obj"]=obj
    
    if request.method == 'POST':
        
        obj.IndustryModel_id = request.POST.get('industry')
        obj.title = request.POST.get('title')
        obj.location = request.POST.get('location')
        obj.type = request.POST.get('type')
        obj.skills = request.POST.get('skills')
        obj.description = request.POST.get('description')
        obj.stipend = request.POST.get('stipend') 
        obj.save()
        
        return redirect('ViewInternship')
    
    return render(request,"Company/internship/InternshipEdit.html",context)

@login_required
@user_passes_test(is_student)
def ApplyInternship(request,id):
    internship = get_object_or_404(InternshipModel,id = id)
    obj = CandidateModel(
        company_id = internship.UserModel_id,
        internship_id = internship.id,
        student_id = request.user.id
    )
    obj.save()
    previous_page = request.META.get('HTTP_REFERER')
    return redirect(previous_page)

@login_required
@user_passes_test(is_company)
def InactiveInternship(request,id):
    internship = InternshipModel.objects.get(id=id)
    internship.status = 0
    internship.save()
    
    return redirect('ViewInternship')

@login_required
@user_passes_test(is_company)
def ActiveInternship(request,id):
    internship = InternshipModel.objects.get(id=id)
    internship.status = 1
    internship.save()
    
    return redirect('ViewInternship')

@login_required
@user_passes_test(is_company)
def CandidateView(request,id):
    context = {}
    context["candidates"] = CandidateModel.objects.filter(internship_id=id)
    
    return render(request,"Company/internship/CandidateView.html",context)

@login_required
@user_passes_test(is_company)
def FeedbackStudent(request,id):
    context = {}
    if request.method == "POST":
        obj = CandidateModel.objects.get(id=id)
        company = UserModel.objects.get(id=obj.company_id)
        data = FeedbackStudentModel(
            company_name = company.CompanyDetails.company_name,
            description = request.POST.get('description'),
            UserModel_id = obj.student_id 
        )    
        data.save()
        
        return redirect('ViewInternship') 
    return render(request,"Company/internship/FeedbackStudent.html",context)

@login_required
@user_passes_test(is_company)
def SelectCandidate(request,id):
    obj = CandidateModel.objects.get(id=id)
    company = UserModel.objects.get(id=obj.company_id)    
    student = UserModel.objects.get(id=obj.student_id)
    internship = InternshipModel.objects.get(id=obj.internship_id)
    
    subject = 'Selection Letter'
    message = 'Congratulations, You are selected as an ' + internship.title + ' at ' + company.CompanyDetails.company_name 
    from_email = 'devpunjani2123@gmail.com'  
    recipient_list = [student.email]  
    send_mail(subject, message, from_email, recipient_list)
    
    return redirect('ViewInternship')

def AllInternships(request):
    context = {}
    context["internships"] = InternshipModel.objects.all()
    return render(request,"Internships.html",context)

def AllIndustries(request):
    context = {}
    context["industries"] = IndustryModel.objects.all()
    return render(request,"Industries.html",context)
    
def AllCompanies(request):
    context = {}
    companies=UserModel.objects.filter(verified=1,user_type=2)
    for company in companies:
        company.i_count = InternshipModel.objects.filter(UserModel_id=company.id).count()
    context["companies"] = companies
    
    return render(request,"Companies.html",context)

def CompanySearchInternships(request,id):
    context = {}
    context["internships"] = InternshipModel.objects.filter(UserModel_id=id)
    return render(request,"CompanySearchInternships.html",context)

def IndustrySearchInternships(request,id):
    context = {}
    context["internships"] = InternshipModel.objects.filter(IndustryModel_id=id)
    return render(request,"IndustrySearchInternships.html",context)
        
def SearchInternships(request):
    if request.method == "POST":
        context = {}
        title = request.POST.get('Title')
        industry = request.POST.get('Industry')
        location = request.POST.get('Location')

        internships = InternshipModel.objects.all()

        if title:
            internships = internships.filter(title=title)
        if industry and industry != '0':
            internships = internships.filter(IndustryModel=industry)
        if location:
            internships = internships.filter(location=location)

        context["internships"] = internships
        return render(request, "SearchInternships.html", context)
