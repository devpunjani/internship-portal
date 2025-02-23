from django.urls import path
from . import views

urlpatterns = [
    #Dashboard
    path('Dashboard/',views.AdminDashboard, name='Dashboard'),
    
    #Admin Login
    path('AdminLogin/',views.AdminLogin,name='AdminLogin'),
    
    #Industry
    path('ViewIndustry/',views.ViewIndustry,name="ViewIndustry"),
    path('AddIndustry/',views.AddIndustry,name="AddIndustry"),
    path('DeleteIndustry/<id>',views.DeleteIndustry,name="DeleteIndustry"),
    path('EditIndustry/<id>',views.EditIndustry,name="EditIndustry"),
    path('BulkUpload/',views.BulkUpload,name="BulkUpload"),
    path('DownloadCsv/', views.DownloadCsv,name='DownloadCsv'),
    path('DownloadPdf/',views.DownloadPdf,name="DownloadPdf"),
    
    #Student
    path('ViewStudent/',views.ViewStudent,name="ViewStudent"),
    path('VerifiedStudent/',views.VerifiedStudent,name="VerifiedStudent"),
    path('UnverifiedStudent/',views.UnverifiedStudent,name="UnverifiedStudent"),
    path('VerifyStudent/<id>',views.VerifyStudent,name="VerifyStudent"),
    path('UnverifyStudent/<id>',views.UnverifyStudent,name="UnverifyStudent"),
    
    #Company
    path('ViewCompany/',views.ViewCompany,name="ViewCompany"),
    path('VerifiedCompany/',views.VerifiedCompany,name="VerifiedCompany"),
    path('UnverifiedCompany/',views.UnverifiedCompany,name="UnverifiedCompany"),
    path('VerifyCompany/<id>',views.VerifyCompany,name="VerifyCompany"),
    path('UnverifyCompany/<id>',views.UnverifyCompany,name="UnverifyCompany"),
    
    #Internship
    path('ViewInternshipAdmin/',views.ViewInternshipAdmin,name="ViewInternshipAdmin"),
    path('VerifiedInternship/',views.VerifiedInternship,name="VerifiedInternship"),
    path('UnverifiedInternship/',views.UnverifiedInternship,name="UnverifiedInternship"),
    path('VerifyInternship/<id>',views.VerifyInternship,name="VerifyInternship"),
    path('UnverifyInternship/<id>',views.UnverifyInternship,name="UnverifyInternship"),
    
    #Feedback
    path('ViewFeedbacks/',views.ViewFeedbacks,name="ViewFeedbacks"),
]
