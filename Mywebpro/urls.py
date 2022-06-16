"""Mywebpro URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views

from MedNoti import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.my_home, name='home'),
    path('login/', views.my_login, name='login'),
    path('logout/', views.my_logout, name='logout'),
    path('register/', views.regis, name='regis'),
    path('after/', views.my_regis, name='sign'),
    path('profile/', views.my_profile, name='profile'),
    path('createprofile/', views.create_profile, name='createprofile'),
    path('change_password/', views.change_password, name='change_password'),
    path('home/', views.my_home, name='home'),
    path('adddrug/', views.add_drug, name='adddrug'),
    path('menu/', views.my_menu, name='menu'),
    path('editprofile/', views.edit_profile, name='edit_profile'),
    path('editdrug/<int:num>', views.edit_drug, name='editdrug'),
    path('addother/', views.addOther, name='addother'),
    path('deletemed/<int:num>', views.delete_med, name='deletemed'),
    path('calendar/', views.my_calendar, name='calendar'),
    path('home2/<int:num>', views.my_home2, name='home2'),
    path('event/', views.my_event, name='event'), 
    path('history/', views.my_history, name='history'),
    path('minus-med/<int:num>', views.minus_med, name='minus-med'),
    path('delete-event/<int:num>', views.delete_event, name='delete-event'),
    path('other/', views.other_page, name='other'),
    path('other/<int:num>', views.my_other, name='myother'),
    path('editother/<int:num>', views.edit_other, name='edit_other'),
    path('report/', views.my_report, name='report'),
    path('setting/', views.my_setting, name='setting'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html'), 
        name='password_change_done'),

    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='registration/password_change.html'), 
        name='password_change'),

    path('password_reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_done.html'),
     name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),

    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'),
     name='password_reset_complete'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

