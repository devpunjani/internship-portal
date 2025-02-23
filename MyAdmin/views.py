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

import csv
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet

# Models
from Users.models import UserModel as UserModel
from Users.models import FeedbackModel as FeedbackModel
from Users.models import InternshipModel as InternshipModel
from .models import IndustryModel as IndustryModel

# Forms
from .forms import IndustryForm as IndustryForm

def is_admin(user):
    #return user.is_superuser == 1
    return user.user_type == 0

# Dashboard
@login_required
@user_passes_test(is_admin)
def AdminDashboard(request):
    industry_count = IndustryModel.objects.count()
    student_count = UserModel.objects.filter(user_type=1).count()
    feedback_count = FeedbackModel.objects.count()
    company_count = UserModel.objects.filter(user_type=2).count()
    internship_count = InternshipModel.objects.count()
    context = {'industry_count': industry_count,'student_count': student_count,'feedback_count': feedback_count,'company_count':company_count,'internship_count':internship_count}

    return render(request,"AdminDashboard.html",context)

# Admin Login
def AdminLogin(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None and user.is_superuser==1:
                login(request, user)
                return redirect('Dashboard')
            else:
                form.add_error(None, 'Invalid Username or Password')
    else:
        form = AuthenticationForm()
    
    return render(request, 'AdminLogin.html', {'form': form})

# View Industry
@login_required
@user_passes_test(is_admin)
def ViewIndustry(request):
    context = {}
    context["industries"] = IndustryModel.objects.all()
    
    return render(request,"industry/IndustryView.html",context)

# Add Industry
@login_required
@user_passes_test(is_admin)
def AddIndustry(request):
    context = {}
    form = IndustryForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.add_message(request,messages.INFO, 'Successfully Created')
        return redirect("ViewIndustry")
    context['forms'] = form
    
    return render(request, "industry/IndustryAdd.html",context)

# Delete Industry
@login_required
@user_passes_test(is_admin)
def DeleteIndustry(request,id):
    context={}
    obj = get_object_or_404(IndustryModel,id = id)
    if request.method == "GET":
        obj.delete()
        return redirect("ViewIndustry")
    
    return render(request,"industry/IndustryView.html",context)

# Edit Industry
@login_required
@user_passes_test(is_admin)
def EditIndustry(request,id):
    context={}
    obj = get_object_or_404(IndustryModel, id = id)
    form = IndustryForm(request.POST or None, instance = obj)
    if form.is_valid():
        form.save()
        return redirect("ViewIndustry")
    context["form"] = form
    
    return render(request, "industry/IndustryEdit.html", context)

# Bulk Upload Industry
@login_required
@user_passes_test(is_admin)
def BulkUpload(request):
    if request.method == 'POST':
        csv_file=request.FILES["csv_file"]
        
        if not csv_file.name.endswith('.csv'):
            return HttpResponse("File Not Valid !")
        if csv_file.multiple_chunks():
            return HttpResponse("Uploaded File Is Big")
        
        file_data = csv_file.read().decode("utf-8")
        lines = file_data.split("\n")
        c=len(lines)
        
        for i in range(0,c-1):
            fields = lines[i].split(",")
            data_dict = {}
            data_dict["name"] = fields[0]
            form=IndustryForm(data_dict)
            if form.is_valid():
                form.save()

        return redirect("ViewIndustry")
    else:
        return render(request,"industry/IndustryBulkUpload.html")     
        
# Download Csv Industry
@login_required
@user_passes_test(is_admin)
def DownloadCsv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="IndustryData.csv"'

    writer = csv.writer(response)
    writer.writerow(['Name'])
        
    for data in IndustryModel.objects.all():
        writer.writerow([data.name])
            
    return response

# Download Pdf Industry
@login_required
@user_passes_test(is_admin)
def DownloadPdf(request):
    # Fetch data from the database, replace YourModel with your actual model name
    data = IndustryModel.objects.all()
    # Create a file-like buffer to receive PDF data.
    buffer = BytesIO()
    # Create the PDF object, using the BytesIO buffer as its "file."
    p = canvas.Canvas(buffer)
    # Set the initial y-coordinate for writing text
    y_coordinate = 750
    # Write your data to the PDF with proper formatting
    for item in data:
        name = item.name
        # Write data to PDF with formatted text
        p.setFont("Helvetica-Bold", 14)  # Set font and size
        p.drawString(100, y_coordinate, f'Name : {name}')
        """ p.drawString(100, y_coordinate - 20, f'Destination: {destination}') """
        y_coordinate -= 60  # Adjust the vertical spacing between items
    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()
    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file.
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="IndustryData.pdf"'

    return response

# View Student
@login_required
@user_passes_test(is_admin)
def ViewStudent(request):
    context = {}
    context["students"] = UserModel.objects.filter(user_type=1)
    
    return render(request,"student/StudentView.html",context)

# View Verified Student
@login_required
@user_passes_test(is_admin)
def VerifiedStudent(request):
    context = {}
    context["students"] = UserModel.objects.filter(verified=1, user_type=1)
    
    return render(request,"student/StudentVerified.html",context)

# View Unverified Student
@login_required
@user_passes_test(is_admin)
def UnverifiedStudent(request):
    context = {}
    context["students"] = UserModel.objects.filter(verified=0, user_type=1)
    
    return render(request,"student/StudentUnverified.html",context)

# Verify Student
@login_required
@user_passes_test(is_admin)
def VerifyStudent(request,id):
    student = UserModel.objects.get(id=id)
    student.verified = 1  # Set the 'verified' field to 1
    student.save()
    
    return redirect('ViewStudent')

# Unverify Student
@login_required
@user_passes_test(is_admin)
def UnverifyStudent(request,id):
    student = UserModel.objects.get(id=id)
    student.verified = 0  # Set the 'verified' field to 1
    student.save()
    
    return redirect('ViewStudent')

# View Feedback
@login_required
@user_passes_test(is_admin)
def ViewFeedbacks(request):
    context = {}
    context["feedbacks"] = FeedbackModel.objects.all().order_by('-id')
    
    return render(request,"FeedbackView.html",context)

# View Company
@login_required
@user_passes_test(is_admin)
def ViewCompany(request):
    context = {}
    context["companies"] = UserModel.objects.filter(user_type=2)
    
    return render(request,"company/CompanyView.html",context)

# View Verified Company
@login_required
@user_passes_test(is_admin)
def VerifiedCompany(request):
    context = {}
    context["companies"] = UserModel.objects.filter(verified=1, user_type=2)
    
    return render(request,"company/CompanyVerified.html",context)

# View Unverified Company
@login_required
@user_passes_test(is_admin)
def UnverifiedCompany(request):
    context = {}
    context["companies"] = UserModel.objects.filter(verified=0, user_type=2)
    
    return render(request,"company/CompanyUnverified.html",context)

# Verify Company
@login_required
@user_passes_test(is_admin)
def VerifyCompany(request,id):
    company = UserModel.objects.get(id=id)
    company.verified = 1  # Set the 'verified' field to 1
    company.save()
    
    return redirect('ViewCompany')

# Unverify Company
@login_required
@user_passes_test(is_admin)
def UnverifyCompany(request,id):
    company = UserModel.objects.get(id=id)
    company.verified = 0  # Set the 'verified' field to 1
    company.save()
    
    return redirect('ViewCompany')

# View Internship
@login_required
@user_passes_test(is_admin)
def ViewInternshipAdmin(request):
    context = {}
    context["internships"] = InternshipModel.objects.all()
    
    return render(request,"internship/AdminInternshipView.html",context)

# View Verified Internship
@login_required
@user_passes_test(is_admin)
def VerifiedInternship(request):
    context = {}
    context["internships"] = InternshipModel.objects.filter(verified=1)
    
    return render(request,"internship/InternshipVerified.html",context)

# View Unverified Internship
@login_required
@user_passes_test(is_admin)
def UnverifiedInternship(request):
    context = {}
    context["internships"] = InternshipModel.objects.filter(verified=0)
    
    return render(request,"internship/InternshipUnverified.html",context)

# Verify Internship
@login_required
@user_passes_test(is_admin)
def VerifyInternship(request,id):
    internship = InternshipModel.objects.get(id=id)
    internship.verified = 1  # Set the 'verified' field to 1
    internship.status = 1
    internship.save()
    
    return redirect('ViewInternshipAdmin')

# Unverify Internship
@login_required
@user_passes_test(is_admin)
def UnverifyInternship(request,id):
    internship = InternshipModel.objects.get(id=id)
    internship.verified = 0  # Set the 'verified' field to 1
    internship.save()
    
    return redirect('ViewInternshipAdmin')