from django.urls import path
from  . import views
from django.contrib.auth.views import LoginView

urlpatterns = [
    #Home Page
    path('',views.Index, name='Home'),
    
    #Student Pages
    path('StudentRegister/', views.StudentRegister, name='StudentRegister'),
    path('StudentLogin/', views.StudentLogin, name='StudentLogin'),
    path('StudentProfile/', views.Profile, name="Profile"),
    path('StudentDeleteProfile/<id>', views.StudentDeleteProfile, name="StudentDeleteProfile"),
    path('StudentUpdateProfile/<id>', views.EditProfile, name="UpdateProfile"),
    path('StudentFeedback/', views.StudentFeedback, name="StudentFeedback"),
    path('StudentSendOtp/', views.SendOtp, name="SendOtp"),
    path('StudentOtpVerify/<id>', views.OtpVerify, name="OtpVerify"),
    path('StudentResetPassword/<id>', views.ResetPassword, name="ResetPassword"),
    path('StudentViewResume/<path:filepath>/', views.StudentViewResume, name='StudentViewResume'),
    path('ApplyInternship/<id>',views.ApplyInternship,name="ApplyInternship"),
    path('Bookmarks',views.Bookmarks,name="Bookmarks"),
    path('Bookmark/<id>',views.Bookmark,name="Bookmark"),
    path('DeleteBookmark/<id>',views.DeleteBookmark,name="DeleteBookmark"),
    path('AllInternships/',views.AllInternships,name="AllInternships"),
    path('AllIndustries',views.AllIndustries,name="AllIndustries"),
    path('AllCompanies/',views.AllCompanies,name="AllCompanies"),
    path('CompanySearchInternships/<id>',views.CompanySearchInternships,name="CompanySearchInternships"),
    path('IndustrySearchInternships/<id>',views.IndustrySearchInternships,name="IndustrySearchInternships"),
    path('SearchInternships',views.SearchInternships,name="SearchInternships"),
    
    #Company Pages
    path('CompanyRegister/', views.CompanyRegister,name='CompanyRegister'),
    path('CompanyLogin/', views.CompanyLogin,name="CompanyLogin"),
    path('CompanyDashboard/',views.CompanyDashboard,name="CompanyDashboard"),
    path('ViewInternship/',views.ViewInternship,name="ViewInternship"),
    path('AddInternship/',views.AddInternship,name="AddInternship"),
    path('DeleteInternship/<id>',views.DeleteInternship,name="DeleteInternship"),
    path('EditInternship/<id>',views.EditInternship,name="EditInternship"),
    path('InactiveInternship/<id>',views.InactiveInternship,name="InactiveInternship"),
    path('ActiveInternship/<id>',views.ActiveInternship,name="ActiveInternship"),
    path('CandidateView/<id>',views.CandidateView,name="CandidateView"),
    path('FeedbackStudent/<id>',views.FeedbackStudent,name="FeedbackStudent"),
    path('SelectCandidate/<id>',views.SelectCandidate,name="SelectCandidate"),
    
]

 
   
   