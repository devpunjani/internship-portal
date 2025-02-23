from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('',include('django.contrib.auth.urls')),
    path('admin/',admin.site.urls),
    path('',include('MyAdmin.urls')),
    path('',include('Users.urls')),
]

urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)