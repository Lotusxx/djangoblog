from django.contrib import admin
from django.urls import path,include
 
urlpatterns = [
    path('admin/', admin.site.urls),
    #省略
    path('djangoblog/',include('djangoblog.urls')),
]