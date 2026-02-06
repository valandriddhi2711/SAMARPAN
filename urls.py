"""
URL configuration for donation project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path, include
from donation.views import *
from donation.views import index, books_view 
from django.conf import settings
from django.conf.urls.static import static

# from donation.views import index,all_logins,donor_login,volunteer_login,admin_login


urlpatterns = [
     path('admin/', admin.site.urls),  # ✅ This line is required
    # path('', include('donation.urls')), 
    path('', index, name='index'),
    path('books/', books_view, name='books'),
    path('read-more/', read_more, name='read-more'),
    path('donate-now/', donate_now, name='donate_now'),
    path('about/', about, name='about'),
    path('toys/', toys, name='toys'),
    path('furniture/', furniture, name='furniture'),
    path('clothes/', clothes, name='clothes'),
    path('footwear/', footwear, name='footwear'),
    path('vessels/', vessels, name='vessels'),
    path('login/', all_logins, name='all_logins'),
    path('donor_login/', donor_login, name='donor_login'),
    path('donor_dashboard/', donor_dashboard, name='donor_dashboard'), 
    path('volunteer_login/', volunteer_login, name='volunteer_login'),
    path('admin_login/', admin_login, name='admin_login'),
    path("donor_reg/",donor_reg, name="donor_reg"),
    path('donor_forgot_password/',donor_forgot_password, name='donor_forgot_password'),
    path("donor_login/",donor_login, name="donor_login"),
    path('donor_home/', donor_home, name='donor_home'),
    path('admin_home/', admin_home, name='admin_home'),
    path('logout/', logout, name='logout'),
    path('donate_now/', donate_now, name='donate_now'),
    path('donation_history/', donation_history, name='donation_history'),
    path('pending_donation/', pending_donation, name='pending_donation'),
    path('view_donationdetail/<int:pid>/', view_donationdetail, name='view_donationdetail'),
    path('add_area/', add_area, name='add_area'),
    path('manage_area/', manage_area, name='manage_area'),
    path('edit_area/<int:pid>/', edit_area, name='edit_area'),
    path('delete_area/<int:pid>/', delete_area, name='delete_area'),
    path('accepted_donation/', accepted_donation, name='accepted_donation'),
    path('manage_donor/', manage_donor, name='manage_donor'),
    path('view_donordetail/<int:pid>/', view_donordetail, name='view_donordetail'),
    path('delete_donor/<int:pid>/', delete_donor, name='delete_donor'),
    path("volunteer_reg/",volunteer_reg, name="volunteer_reg"),
    path('volunteer_home/', volunteer_home, name='volunteer_home'),
    path('new_volunteer/', new_volunteer, name='new_volunteer'),
    path('view_volunteerdetail/<int:pid>/', view_volunteerdetail, name='view_volunteerdetail'),
    path('accepted_volunteer/', accepted_volunteer, name='accepted_volunteer'),
    path('rejected_volunteer/', rejected_volunteer, name='rejected_volunteer'),
    path('all_volunteers/', all_volunteers, name='all_volunteers'),
    path('delete_volunteer/<int:pid>/', delete_volunteer, name='delete_volunteer'),
    path('accepted_donationdetail/<int:pid>/', accepted_donationdetail, name='accepted_donationdetail'),
    path('collection_req/', collection_req, name='collection_req'),
    path('donationcollection_detail/<int:pid>/', donationcollection_detail, name='donationcollection_detail'),
    path('donationrec_volunteer/', donationrec_volunteer, name='donationrec_volunteer'),
    path('donationrec_detail/<int:pid>/', donationrec_detail, name='donationrec_detail'),
    path('donationnotrec_volunteer/', donationnotrec_volunteer, name='donationnotrec_volunteer'),
    path('donationdelivered_volunteer/', donationdelivered_volunteer, name='donationdelivered_volunteer'),
    path('profile_volunteer/', profile_volunteer, name='profile_volunteer'),
    path('dashboard_donation/', dashboard_donation, name='dashboard_donation'),
    path('dashboard_volunteer/', dashboard_volunteer, name='dashboard_volunteer'),
    path('services/', services_page, name='services_page'),  # ✅ this name must match
    path('services/add/', add_service, name='add_service'),
    path('services/manage/', manage_services, name='manage_services'),
    path('services/delete/<int:service_id>/', delete_service, name='delete_service'),
    path('services/edit/<int:service_id>/', edit_service, name='edit_service'),
    path('booking/new/', new_booking, name='new_booking'),
    path('booking/my/', my_bookings, name='my_bookings'),
    path('donor/profile/', donor_profile, name='donor_profile'),
    path('contact-us/', contact_us, name='contact_us'),
    path('gift-donations/',gift_donations,name='gift_donations'),
    path('admin-dashboard/', admin_dashboard, name='admin_dashboard'),
    path('dsettings/', dsettings, name='dsettings'),
    path('update-settings/', update_settings, name='update_settings'),




]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)