# from django.shortcuts import render
from urllib import request
from django.http import JsonResponse
from django.shortcuts import render
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from.models import *
from datetime import date
import pandas as pd
import os
from django.db.models import Q
import traceback
from .models import OrganTransplant
import random
from django.core.mail import send_mail
from .models import EmergencyAlert
from .models import EmailOTP
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from django.db.models.functions import TruncMonth
from .models import KidneyDonor, KidneyPatient
from .models import Service
import json 
from .models import Booking
from django.contrib.auth import login
import openai
from .models import HealthCheckup
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from django.db.models import Sum,Count, Avg
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout 



# from django.contrib.auth import authenticate,login,logout

def index(request):
    return render(request, 'index.html')  # Make sure you're returning
def read_more(request):
    return render(request, 'read-more.html') 
def donate_now(request):
    return render(request, 'donate_now.html')
def about(request):
    return render(request, 'about.html')

def books_view(request):
    return render(request, 'books.html')


def toys(request):
    return render(request, 'toys.html')

def furniture(request):
    return render(request, 'furniture.html')

def clothes(request):
    return render(request, 'clothes.html')

def footwear(request):
    return render(request, 'footwear.html')
def books_view(request):
    return render(request, 'books.html')

def vessels(request):
    return render(request, 'vessels.html')

def all_logins(request):
    return render(request, 'all_logins.html')
def donor_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)  # ✅ Django’s built-in login
            messages.success(request, "Login successful!")
            return redirect("donor_home")  # ✅ redirect to donor home
        else:
            messages.error(request, "Invalid username or password")

    # Always return a response for GET or failed POST
    return render(request, "donor_login.html")
def donor_dashboard(request):

    return render(request,'all_logins.html')

def volunteer_login(request):
    if request.method == "POST":
        username = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            try:
                volunteer = Volunteer.objects.get(user=user)

                # 🔒 Check approval status
                if volunteer.status == "pending":
                    messages.error(request, "Your account is pending approval by admin.")
                    return redirect("volunteer_login")

                # ✅ Approved → login
                login(request, user)
                messages.success(request, "Login successful!")
                return redirect("volunteer_home")

            except Volunteer.DoesNotExist:
                messages.error(request, "You are not registered as a volunteer.")
                return redirect("volunteer_login")

        else:
            messages.error(request, "Invalid email or password.")

    return render(request, "volunteer_login.html")


def admin_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        try:
            if user.is_staff:
                login(request, user)  # ✅ Django’s built-in login
                error="no"
            #     messages.success(request, "Login successful!")
            #     return redirect("donor_home")  # ✅ redirect to donor home
            else:
                error="yes"
            # messages.error(request, "Invalid username or password")
        except:
                error="yes"

    # Always return a response for GET or failed POST
    return render(request,'admin_login.html',locals())

def admin_home(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    return render(request,'admin_home.html')


def donor_reg(request):
    error = ""
    if request.method == "POST":
        fname = request.POST.get("firstname")
        lname = request.POST.get("lastname")
        email = request.POST.get("email")
        contact = request.POST.get("contact")
        pwd = request.POST.get("pwd")
        cpwd = request.POST.get("cpwd")
        address = request.POST.get("address")
        userpic = request.FILES.get("userpic")

        if pwd != cpwd:
            error = "password_mismatch"
        elif User.objects.filter(username=email).exists():
            error = "exists"
        else:
            try:
                user = User.objects.create_user(
                    first_name=fname,
                    last_name=lname,
                    username=email,
                    email=email,
                    password=pwd
                )
                Donor.objects.create(
                    user=user,
                    contact=contact,
                    address=address,
                    userpic=userpic
                )
                messages.success(request, "Registration successful! Please login.")
                return redirect("donor_login")  # ✅ correct redirect
            except Exception as e:
                print("Error during donor registration:", e)
                error = "yes"
                traceback.print_exc()

    return render(request, "donor_reg.html", {"error": error})

def donor_home(request):
    if not request.user.is_authenticated:
        return redirect('donor_login')

    # ✅ Direct redirect to dashboard
    return redirect('dashboard_donation')

def donate_now(request):
    if not request.user.is_authenticated:
        return redirect('donor_login')

    user = request.user
    # Safely get or create a Donor record for the logged-in user
    donor, created = Donor.objects.get_or_create(user=user)

    error = ""  # initialize error variable

    if request.method == "POST":
        donationname = request.POST.get('donationname')
        donationpic = request.FILES.get('donationpic')
        collectionloc = request.POST.get('collectionloc')
        description = request.POST.get('description')

        try:
            Donation.objects.create(
                donor=donor,
                donationname=donationname,
                donationpic=donationpic,
                collectionloc=collectionloc,
                description=description,
                status="pending"
            )
            error = "No"
        except Exception as e:
            print("Error while saving donation:", e)
            error = "Yes"

    return render(request, 'donate_now.html', {'error': error})

def logout_view(request):
    logout(request)
    return redirect('donor_login')

def donation_history(request):
    if not request.user.is_authenticated:
        return redirect('donor_login')
    user = request.user
    donor = Donor.objects.get(user=user) 
    donation=Donation.objects.filter(donor=donor)
    # (ep"16""10:30,10:60")
    return render(request,'donation_history.html',locals())

def pending_donation(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    # user = request.user
    # donor = Donor.objects.get(user=user) 
    donation=Donation.objects.filter(status="pending")
    # (ep"16""10:30,10:60")
    return render(request,'pending_donation.html',locals())

def view_donationdetail(request, pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')

    donation = Donation.objects.get(id=pid)  
    if request.method == "POST":
        status =request.POST['status']
        adminremark = request.POST['adminremark']
        try:
            donation.adminremark = adminremark
            donation.status = status
            donation.updationdate = date.today()
            donation.save()
            error ="no"
        except:
            error ="yes"

    return render(request, 'view_donationdetail.html', {'donation': donation})

# def uuid_example(request):
#     # Generate next reg number
#     if MyUUIDModel.objects.count() == 0:
#         regno = 1001
#     else:
#         regno = MyUUIDModel.objects.aggregate(Max('regnumber'))['regnumber__max'] + 1

#     error = ""

#     if request.method == "POST":
#         username = request.POST['username']

#         try:
#             MyUUIDModel.objects.create(
#                 username=username,
#                 regnumber=regno
#             )
#             error = "no"
#         except:
#             error = "yes"

#     return render(request, "uuid_example.html", locals())

def accepted_donation(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    # user = request.user
    # donor = Donor.objects.get(user=user) 
    donation=Donation.objects.filter(status="accept")
    # (ep"16""10:30,10:60")
    return render(request,'accepted_donation.html',locals())

def add_area(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')

    error = ""   # ✅ FIX: initialize first

    if request.method == "POST":
        areaname = request.POST.get('areaname')
        description = request.POST.get('description')

        try:
            DonationArea.objects.create(
                areaname=areaname,
                description=description
            )
            error = "No"
        except Exception as e:
            print("Error while saving donation:", e)
            error = "Yes"

    return render(request, 'add_area.html', {'error': error})

def manage_area(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    # user = request.user
    # donor = Donor.objects.get(user=user) 
    area=DonationArea.objects.all()
    # (ep"16""10:30,10:60")
    return render(request,'manage_area.html',locals())

def edit_area(request,pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    area = DonationArea.objects.get(id=pid)
    error = ""   

    if request.method == "POST":
        areaname = request.POST.get('areaname')
        description = request.POST.get('description')
        area.areaname = areaname
        area.description = description

        try:
            
                area.save()
                error = "No"
        except:
            error = "Yes"

    return render(request, 'edit_area.html', locals())

def delete_area(request,pid):
    area=DonationArea.objects.get(id=pid)
    area.delete()
    return redirect('manage_area')



def donor_forgot_password(request):
    def donor_forgot_password(request):
        if request.method == "POST":
            email = request.POST.get("username")
            password = request.POST.get("password")

        try:
            user = User.objects.get(username=email)  # username=email
            user.set_password(password)
            user.save()

            messages.success(request, "Password changed successfully. Please login.")
            return redirect("donor_login")

        except User.DoesNotExist:
            messages.error(request, "Email not registered!")

    return render(request, "donor_forgot_password.html")


def manage_donor(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    # user = request.user
    # donor = Donor.objects.get(user=user) 
    donor=Donor.objects.all()
    # (ep"16""10:30,10:60")
    return render(request,'manage_donor.html',locals())

def view_donordetail(request,pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    donor = Donor.objects.get(id=pid)
    # error = ""   

    # if request.method == "POST":
    #     areaname = request.POST.get('areaname')
    #     description = request.POST.get('description')
    #     area.areaname = areaname
    #     area.description = description

    #     try:
            
    #             area.save()
    #             error = "No"
    #     except:
    #         error = "Yes"

    return render(request, 'view_donordetail.html', locals())

def delete_donor(request, pid):
    donor = get_object_or_404(Donor, id=pid)
    donor.delete()
    return redirect('view_donor')

def volunteer_reg(request):
    error = ""
    if request.method == "POST":
        fname = request.POST.get("firstname")
        lname = request.POST.get("lastname")
        email = request.POST.get("email")
        contact = request.POST.get("contact")
        pwd = request.POST.get("pwd")
        cpwd = request.POST.get("cpwd")
        address = request.POST.get("address")
        aboutme = request.POST.get("aboutme")
        userpic = request.FILES.get("userpic", None)
        idpic = request.FILES.get("idpic", None)

        # 1️⃣ Password check
        if pwd != cpwd:
            error = "password_mismatch"
            messages.error(request, "Passwords do not match!")
        # 2️⃣ Existing user check
        elif User.objects.filter(username=email).exists():
            error = "exists"
            messages.error(request, "User with this email already exists!")
        else:
            try:
                user = User.objects.create_user(
                    first_name=fname,
                    last_name=lname,
                    username=email,
                    email=email,
                    password=pwd
                )

                Volunteer.objects.create(
                    user=user,
                    Contact=contact,
                    address=address,
                    aboutme=aboutme,
                    userpic=userpic,
                    idpic=idpic,
                    status="pending"
                )

                messages.success(request, "Registration successful! Please login.")
                return redirect("volunteer_login")

            except Exception as e:
                print("Error during volunteer registration:", e)
                traceback.print_exc()
                messages.error(request, f"Error: {str(e)}")
                error = "yes"

    return render(request, "volunteer_reg.html", {"error": error})



def new_volunteer(request):
    volunteers = Volunteer.objects.filter(status="pending")
    return render(request, "new_volunteer.html", {
        "volunteers": volunteers
    })
def view_volunteerdetail(request, pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')

    volunteer = get_object_or_404(Volunteer, id=pid)
    error = ""

    if request.method == "POST":
        status = request.POST.get('status')
        adminremark = request.POST.get('adminremark')

        try:
            volunteer.status = status
            volunteer.adminremark = adminremark
            volunteer.updationdate = date.today()
            volunteer.save()
            error = "no"
        except Exception as e:
            print("Update error:", e)
            error = "yes"

    return render(
        request,
        'view_volunteerdetail.html',
        {
            'volunteer': volunteer,  # ✅ singular (matches template)
            'error': error
        }
    )

def accepted_volunteer(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')

    volunteers = Volunteer.objects.filter(status="accepted")
    return render(request, "accepted_volunteer.html", {
        "volunteers": volunteers
    })

def rejected_volunteer(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')

    volunteers = Volunteer.objects.filter(status="rejected")
    return render(request, 'rejected_volunteer.html', {
        'volunteers': volunteers
    })

def all_volunteers(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')

    volunteers = Volunteer.objects.all().order_by('-regdate')  # newest first
    return render(request, 'all_volunteers.html', {
        'volunteers': volunteers
    })
def delete_volunteer(request,pid):
    User.objects.get(id=pid)
    User.delete()
    return redirect('all_volunteer')

def accepted_donationdetail(request, pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')

    donation = get_object_or_404(Donation, id=pid)  
    donationarea = DonationArea.objects.all()
    volunteer = Volunteer.objects.all()

    error = ""  # initialize error variable

    if request.method == "POST":
        donationareaid = request.POST.get('donationareaid')
        volunteerid = request.POST.get('volunteerid')

        try:
            da = DonationArea.objects.get(id=donationareaid)
            v = Volunteer.objects.get(id=volunteerid)  # ✅ fixed

            donation.donationarea = da
            donation.volunteer = v
            donation.status = "Volunteer Allocated"
            donation.updationdate = date.today()
            donation.save()
            error = "no"
        except Exception as e:
            print("Error assigning volunteer:", e)
            error = "yes"

    return render(request, 'accepted_donationdetail.html', {
        'donation': donation,
        'donationarea': donationarea,
        'volunteer': volunteer,
        'error': error
    })
def volunteer_home(request):
    if not request.user.is_authenticated:
        return redirect('volunteerr_login')
    return render(request,'volunteer_home.html')

# def collection_req(request):
#     if not request.user.is_authenticated:
#         return redirect('volunteer_login')

#     volunteer = get_object_or_404(Volunteer, user=request.user)

#     donation = Donation.objects.filter(
#         volunteer=volunteer,
#         status="volunteer Allocated"
#     ).order_by('-id')

#     return render(request, 'collection_req.html', {
#         'donation': donation
#     })
def collection_req(request):
    if not request.user.is_authenticated:
        return redirect('volunteer_login')

    volunteer = get_object_or_404(Volunteer, user=request.user)

    donations = Donation.objects.filter(
        volunteer=volunteer,
        status="Volunteer Allocated"
    )

    return render(request, 'collection_req.html', {
        'donation': donations
    })


def donationcollection_detail(request, pid):
    if not request.user.is_authenticated:
        return redirect('volunteer_login')

    donation = get_object_or_404(Donation, id=pid)
    error = ""

    if request.method == "POST":
        status = request.POST.get('status')
        volunteerremark = request.POST.get('volunteerremark')  # FIXED name

        try:
            donation.status = status
            donation.volunteerremark = volunteerremark
            donation.updationdate = date.today()
            donation.save()
            error = "no"
        except Exception as e:
            print("Error:", e)
            error = "yes"

    return render(request, 'donationcollection_detail.html', {
        'donation': donation,
        'error': error
    })
def donationrec_volunteer(request):
    if not request.user.is_authenticated:
        return redirect('volunteer_login')

    volunteer = get_object_or_404(Volunteer, user=request.user)

    donations = Donation.objects.filter(
        volunteer=volunteer,
        status__iexact="Donation Received"
    )

    return render(request, 'donationrec_volunteer.html', {
        'donation': donations
    })


def donationrec_detail(request, pid):
    if not request.user.is_authenticated:
        return redirect('volunteer_login')

    donation = get_object_or_404(Donation, id=pid)
    error = ""

    if request.method == "POST":
        try:
            status = request.POST.get("status")
            deliverypic = request.FILES.get("deliverypic")

            # Update donation
            donation.status = status
            donation.updationdate = date.today()

            if deliverypic:
                donation.deliverypic = deliverypic

            donation.save()

            # Save to Gallery table
            if deliverypic:
                Gallery.objects.create(
                    donation=donation,
                    deliverypic=deliverypic
                )

            error = "no"

        except Exception as e:
            print("Error:", e)
            error = "yes"

    return render(request, 'donationrec_detail.html', {
        'donation': donation,
        'error': error
    })

def donationnotrec_volunteer(request):
    if not request.user.is_authenticated:
        return redirect('volunteer_login')

    volunteer = get_object_or_404(Volunteer, user=request.user)

    donations = Donation.objects.filter(
        volunteer=volunteer,
        status="Donation not Received"
    )

    return render(request, 'donationnotrec_volunteer.html', {
        'donation': donations
    })
def donationdelivered_volunteer(request):
    if not request.user.is_authenticated:
        return redirect('volunteer_login')

    volunteer = get_object_or_404(Volunteer, user=request.user)

    donations = Donation.objects.filter(
        volunteer=volunteer,
        status="Donation Delivered"
    )

    return render(request, 'donationdelivered_volunteer.html', {
        'donation': donations
    })

def profile_volunteer(request):
    if not request.user.is_authenticated:
        return redirect('volunteer_login')

    # Get volunteer linked to logged-in user
    volunteer = get_object_or_404(Volunteer, user=request.user)

    if request.method == "POST":
        try:
            # User model fields
            user = request.user
            user.first_name = request.POST.get("firstname")
            user.last_name = request.POST.get("lastname")
            user.email = request.POST.get("email")
            user.save()

            # Volunteer model fields
            volunteer.Contact = request.POST.get("contact")
            volunteer.address = request.POST.get("address")
            volunteer.aboutme = request.POST.get("aboutme")

            # Images
            if request.FILES.get("userpic"):
                volunteer.userpic = request.FILES.get("userpic")

            if request.FILES.get("idpic"):
                volunteer.idpic = request.FILES.get("idpic")

            volunteer.save()

            messages.success(request, "Profile updated successfully ✅")
            return redirect('profile_volunteer')

        except Exception as e:
            print("Profile Error:", e)
            messages.error(request, "Something went wrong ❌")

    return render(request, 'profile_volunteer.html', {
        'volunteer': volunteer
    })

# from django.shortcuts import render, redirect
# from django.db.models import Count
# from django.db.models.functions import TruncMonth
# import json   # ✅ IMPORTANT

def dashboard_donation(request):
    if not request.user.is_authenticated:
        return redirect('donor_login')

    try:
        donor = Donor.objects.get(user=request.user)
    except Donor.DoesNotExist:
        return redirect('donor_login')

    donations = Donation.objects.filter(donor=donor)

    # 📊 Monthly Data
    monthly_data = (
        donations
        .annotate(month=TruncMonth('donationdate'))
        .values('month')
        .annotate(total=Count('id'))
        .order_by('month')
    )

    months = [d['month'].strftime('%b %Y') for d in monthly_data if d['month']]
    counts = [d['total'] for d in monthly_data]

    context = {
        "total_donations": donations.count(),
        "pending_donations": donations.filter(status="pending").count(),
        "accepted_donations": donations.filter(status="accept").count(),
        "recent_donations": donations.order_by("-id")[:5],

        # ✅ CONVERT TO JSON (VERY IMPORTANT)
        "months": json.dumps(months),
        "counts": json.dumps(counts),
    }

    return render(request, "dashboard_donation.html", context)

def dashboard_volunteer(request):
    if not request.user.is_authenticated:
        return redirect('volunteer_login')  # your volunteer login URL

    try:
        volunteer = Volunteer.objects.get(user=request.user)
    except Volunteer.DoesNotExist:
        return redirect('volunteer_login')

    donations = Donation.objects.filter(volunteer=volunteer)

    # Monthly donations handled by this volunteer
    monthly_data = (
        donations
        .annotate(month=TruncMonth('donationdate'))
        .values('month')
        .annotate(total=Count('id'))
        .order_by('month')
    )

    months = [d['month'].strftime('%b %Y') for d in monthly_data if d['month']]
    counts = [d['total'] for d in monthly_data]

    context = {
        "total_donations": donations.count(),
        "pending_donations": donations.filter(status="pending").count(),
        "accepted_donations": donations.filter(status="accept").count(),
        "recent_donations": donations.order_by("-id")[:5],
        "months": months,
        "counts": counts,
    }

    return render(request, "dashboard_volunteer.html", context)

def services_page(request):
    services = Service.objects.all()
    return render(request, "services_page.html", {"services": services})

def add_service(request):
    if not request.user.is_staff:
        messages.error(request, "You are not authorized to add services.")
        return redirect('services_page')  # make sure this URL exists!

    if request.method == "POST":
        title = request.POST.get('title')
        description = request.POST.get('description')
        icon = request.POST.get('icon')
        image = request.FILES.get('image')

        if title and description:
            Service.objects.create(title=title, description=description, icon=icon, image=image)
            messages.success(request, "Service added successfully!")
            return redirect('services_page')  # again, make sure this URL exists
        else:
            messages.error(request, "Please provide both title and description.")

    return render(request, "add_service.html")


# Manage Services Page
def manage_services(request):
    if not request.user.is_staff:
        messages.error(request, "You are not authorized to view this page.")
        return redirect('services_page')

    services = Service.objects.all()
    return render(request, "manage_services.html", {"services": services})


# Delete Service
def delete_service(request, service_id):
    if not request.user.is_staff:
        messages.error(request, "You are not authorized to perform this action.")
        return redirect('manage_services')

    service = get_object_or_404(Service, id=service_id)
    service.delete()
    messages.success(request, "Service deleted successfully!")
    return redirect('manage_services')


# Edit Service
# views.py
def edit_service(request, service_id):
    if not request.user.is_staff:
        messages.error(request, "You are not authorized to perform this action.")
        return redirect('manage_services')

    service = get_object_or_404(Service, id=service_id)

    if request.method == "POST":
        service.title = request.POST.get('title')
        service.description = request.POST.get('description')
        service.icon = request.POST.get('icon')
        if request.FILES.get('image'):
            service.image = request.FILES.get('image')
        service.save()
        messages.success(request, "Service updated successfully!")
        return redirect('manage_services')

    return render(request, "edit_service.html", {"service": service})


def new_booking(request):
    if not request.user.is_authenticated:
        messages.error(request, "Please login to book a service.")
        return redirect('donor_login')  # replace with your login URL name

    services = Service.objects.all()

    if request.method == "POST":
        service_id = request.POST.get('service')
        booking_date = request.POST.get('booking_date')
        booking_time = request.POST.get('booking_time')

        if service_id and booking_date and booking_time:
            service = Service.objects.get(id=service_id)
            Booking.objects.create(
                user=request.user,
                service=service,
                booking_date=booking_date,
                booking_time=booking_time
            )
            messages.success(request, "Booking created successfully!")
            return redirect('my_bookings')  # replace with your bookings page
        else:
            messages.error(request, "All fields are required.")

    context = {"services": services}
    return render(request, "new_booking.html", context)
def my_bookings(request):
    if not request.user.is_authenticated:
        messages.error(request, "Please login to view your bookings.")
        return redirect('login')  # replace with your login URL name

    # Get all bookings for the logged-in user
    bookings = Booking.objects.filter(user=request.user).order_by('-booking_date', '-booking_time')

    context = {"bookings": bookings}
    return render(request, "my_bookings.html", context)
def donor_profile(request):
    donor = get_object_or_404(Donor, user=request.user)

    if request.method == "POST":
        donor.user.first_name = request.POST.get("firstname")
        donor.user.last_name = request.POST.get("lastname")
        donor.contact = request.POST.get("contact")
        donor.address = request.POST.get("address")
        # donor.aboutme = request.POST.get("aboutme")

        if request.FILES.get("userpic"):
            donor.userpic = request.FILES.get("userpic")
        # if request.FILES.get("idpic"):
        #     donor.idpic = request.FILES.get("idpic")

        donor.user.save()
        donor.save()
        messages.success(request, "Profile updated successfully!")
        return redirect("donor_profile")

    return render(request, "donor_profile.html", {"donor": donor})

def contact_us(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        subject = request.POST.get("subject")
        message_text = request.POST.get("message")

        # Optional: save message to database or send email
        # Example: save to a model
        # ContactMessage.objects.create(name=name, email=email, subject=subject, message=message_text)

        messages.success(request, "Your message has been sent successfully!")
        return redirect("contact_us")

    return render(request, "contact_us.html")



def gift_donations(request):
    if not request.user.is_authenticated:
        return redirect('donor_login')

    user = request.user

    gift_qs = GiftDonation.objects.filter(
        user=user
    ).select_related('company', 'campaign').order_by('-created_at')

    # === METRICS ===
    total_gifts = gift_qs.count()

    pending_matches = gift_qs.filter(status='pending').count()

    total_matched_amount = gift_qs.filter(
        status='approved'
    ).aggregate(total=Sum('matched_amount'))['total'] or 0

    avg_match_amount = gift_qs.filter(
        status='approved'
    ).aggregate(avg=Avg('matched_amount'))['avg'] or 0

    context = {
        'gift_donations': gift_qs,
        'total_gifts': total_gifts,
        'pending_matches': pending_matches,
        'total_matched_amount': total_matched_amount,
        'avg_match_amount': round(avg_match_amount, 2),
    }

    return render(request, 'gift_donations.html', context)

def admin_dashboard(request):
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('admin_login')

    donations = Donation.objects.all()

    # Monthly donation stats
    monthly_data = (
        donations
        .annotate(month=TruncMonth('donationdate'))
        .values('month')
        .annotate(total=Count('id'))
        .order_by('month')
    )

    months = [d['month'].strftime('%b %Y') for d in monthly_data if d['month']]
    counts = [d['total'] for d in monthly_data]

    # ✅ DEFINE VARIABLES FIRST
    pending_donations = Donation.objects.filter(status='pending').count()
    accepted_donations = Donation.objects.filter(status='accepted').count()

    # ✅ PROPER CONTEXT DICTIONARY
    context = {
        "total_donations": donations.count(),
        "pending_donations": pending_donations,
        "accepted_donations": accepted_donations,
        "recent_donations": donations.order_by("-id")[:10],
        "months": months,
        "counts": counts,
    }

    return render(request, "admin_dashboard.html", context)

def dsettings(request):
    user = request.user

    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        email_notifications = request.POST.get('email_notifications') == 'on'
        dark_mode = request.POST.get('dark_mode') == 'on'

        # Update username and email
        user.username = username
        user.email = email
        user.save()

        # Update password
        if password and password == confirm_password:
            user.set_password(password)
            user.save()
            messages.success(request, "Password updated successfully!")

        # Update profile preferences (assuming you have a Profile model)
        profile = user.profile
        profile.email_notifications = email_notifications
        profile.dark_mode = dark_mode
        profile.save()

        messages.success(request, "Settings updated successfully!")
        return redirect('settings')

    return render(request, 'settings.html', {'user': user})

def update_settings(request):
    user = request.user

    if request.method == "POST":
        # Get form data
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        email_notifications = request.POST.get('email_notifications') == 'on'
        dark_mode = request.POST.get('dark_mode') == 'on'

        # Update username and email
        if username:
            user.username = username
        if email:
            user.email = email
        user.save()

        # Update password if both fields match
        if password and password == confirm_password:
            user.set_password(password)
            user.save()
            messages.success(request, "Password updated successfully!")
        elif password != confirm_password:
            messages.error(request, "Passwords do not match!")

        # Update profile preferences (requires Profile model)
        profile = user.profile
        profile.email_notifications = email_notifications
        profile.dark_mode = dark_mode
        profile.save()

        messages.success(request, "Settings updated successfully!")
        return redirect('settings')  # redirect back to settings page

    # If GET request, just redirect to settings
    return redirect('settings')




openai.api_key = settings.OPENAI_API_KEY


def chatbot_page(request):
    return render(request, 'chatbot.html')


def chatbot_response(request):
    message = request.GET.get('message', '').lower()

    # Greeting
    if any(word in message for word in ["hello", "hi", "hey"]):
        reply = "Hello 👋 Welcome to Samarpan Donation Management System! How can I help you?"

    # About project
    elif "samarpan" in message or "about" in message:
        reply = "Samarpan is a Donation Management System that connects donors, volunteers, and needy people."

    # Donation process
    elif "how to donate" in message or "donation process" in message:
        reply = "To donate, go to the Donation page, fill the form, submit item details, and our volunteer will collect it."

    elif "donation" in message:
        reply = "You can donate clothes, books, food, and other usable items through the donation section."

    # Volunteer
    elif "volunteer" in message:
        reply = "You can register as a volunteer from the Volunteer Registration page and help manage donations."

    # Login/Register
    elif "login" in message:
        reply = "Click on the Login button in the navbar and enter your credentials."

    elif "register" in message:
        reply = "You can register as a Donor or Volunteer from the Registration page."

    # Contact
    elif "contact" in message:
        reply = "You can contact us through the Contact page for any support."

    # Admin
    elif "admin" in message:
        reply = "Admin manages users, donations, approvals, and overall system operations."

    # Thanks
    elif "thank" in message:
        reply = "You're welcome 😊 Happy to help!"

    # Exit
    elif "bye" in message:
        reply = "Goodbye! Have a wonderful day 🌟"

    else:
        reply = "Sorry 😔 I didn't understand that. Please ask about donation, volunteer, login, or contact."

    return JsonResponse({'response': reply})






# def send_otp(request):
#     if request.method == "POST":
#         email = request.POST.get("email")
#         print("Email entered:", email)

#         if not email:
#             return render(request, "send_otp.html", {
#                 "error": "Please enter email"
#             })

#         try:
#             user = User.objects.get(email=email)
#         except User.DoesNotExist:
#             return render(request, "send_otp.html", {
#                 "error": "Email is not registered!"
#             })

#         otp = str(random.randint(100000, 999999))
#         print("Generated OTP:", otp)

#         EmailOTP.objects.update_or_create(
#             user=user,
#             defaults={"otp": otp}
#         )

#         request.session['email'] = email

#         return redirect("verify_otp")

#     return render(request, "send_otp.html")


# def verify_otp(request):
#     if request.method == "POST":
#         entered_otp = request.POST.get("otp")
#         email = request.session.get("email")

#         try:
#             user = User.objects.get(email=email)
#             otp_record = EmailOTP.objects.get(user=user)

#             if otp_record.is_expired():
#                 otp_record.delete()
#                 return render(request, "verify_otp.html", {
#                     "error": "OTP has expired!"
#                 })

#             if entered_otp == otp_record.otp:
#                 otp_record.delete()  # Delete after success
#                 return redirect("index")
#             else:
#                 return render(request, "verify_otp.html", {
#                     "error": "Invalid OTP"
#                 })

#         except:
#             return render(request, "verify_otp.html", {
#                 "error": "Something went wrong"
#             })

#     return render(request, "verify_otp.html")

# from django.shortcuts import render, redirect
# from django.contrib.auth.models import User
# from .models import EmailOTP
# from django.core.mail import send_mail
# from django.conf import settings
# from django.db.models import Q

def send_otp(request):
    if request.method == "POST":
        email = request.POST.get("email", "").strip().lower()

        try:
            # Allow email OR username
            user = User.objects.get(Q(email__iexact=email) | Q(username__iexact=email))
        except User.DoesNotExist:
            return render(request, "send_otp.html", {"error": "Email is not registered!"})

        # Create OTP automatically
        otp_obj, created = EmailOTP.objects.get_or_create(user=user)
        otp_obj.save()  # auto-generates OTP

        # Send OTP by email
        send_mail(
            "Your OTP Code",
            f"Your OTP is {otp_obj.otp}",
            settings.EMAIL_HOST_USER,
            [user.email],
            fail_silently=False,
        )

        # Save user id in session for verification
        request.session['otp_user_id'] = user.id

        return redirect("verify_otp")

    return render(request, "send_otp.html")


def verify_otp(request):
    if request.method == "POST":
        entered_otp = request.POST.get("otp", "").strip()
        user_id = request.session.get("otp_user_id")

        if not user_id:
            return redirect("send_otp")

        try:
            user = User.objects.get(id=user_id)
            otp_record = EmailOTP.objects.get(user=user)

            if otp_record.is_expired():
                otp_record.delete()
                return render(request, "otp.html", {"error": "OTP expired!"})

            if entered_otp == otp_record.otp:
                otp_record.delete()  # OTP used
                return redirect("index")  # verified successfully

            else:
                return render(request, "otp.html", {"error": "Invalid OTP"})

        except EmailOTP.DoesNotExist:
            return render(request, "otp.html", {"error": "No OTP found"})

    return render(request, "otp.html")


def transplant_dashboard(request):
    data = OrganTransplant.objects.all()
    return render(request, "transplant_dashboard.html", {"data": data})
#
# from django.conf import settings
# from django.shortcuts import render

def organ_csv_view(request):
    file_path = os.path.join(settings.BASE_DIR, "organ_data.csv")
    df = pd.read_csv(file_path)
    data = df.to_dict(orient="records")
    return render(request, "organ_csv.html", {"data": data})

def home(request):
    return render(request, 'home.html')
def about(request):
    return render(request, 'Oabout.html')

def products(request):
    return render(request, 'Oproducts.html')

def service(request):
    return render(request, 'Oservice.html')

def contact(request):
    return render(request, 'Ocontact.html')

def login_page(request):
    return render(request, 'Ologin.html')
def blood(request):
    return render(request, 'blood.html')
def read_moreo(request):
    return render(request, 'read_moreO.html')
def more(request):
    return render(request, 'more.html')

# Register View
def register_view(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('register')

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        messages.success(request, "Registration Successful")
        return redirect('login')

    return render(request, 'register.html')


# Login View
def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid Username or Password")
    return render(request, 'login.html')


# Dashboard
def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'dashboard.html')


# def logout_view(request):
#     logout(request)
#     return redirect('login')   # after logout go to login page



def free_health_checkup(request):

    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        age = request.POST.get('age')
        checkup_type = request.POST.get('checkup_type')

        HealthCheckup.objects.create(
            name=name,
            email=email,
            phone=phone,
            age=age,
            checkup_type=checkup_type
        )

        return redirect('success')

    return render(request, 'free_health_checkup.html')


def success(request):
    return render(request, 'success.html')




def kidney_donor_register(request):

    if request.method == "POST":

        user = request.user
        age = request.POST.get('age')
        blood_group = request.POST.get('blood_group')
        contact = request.POST.get('contact')
        address = request.POST.get('address')

        KidneyDonor.objects.create(
            user=user,
            age=age,
            blood_group=blood_group,
            contact=contact,
            address=address
        )

        return redirect('kidney_patient')

    return render(request, 'kidney_donor.html')


def kidney_patient_register(request):

    if request.method == "POST":

        user_id = request.POST.get('user')
        user = User.objects.get(id=user_id)

        name = request.POST.get('name')
        age = request.POST.get('age')
        blood_group = request.POST.get('blood_group')
        hospital = request.POST.get('hospital')
        doctor = request.POST.get('doctor')
        contact = request.POST.get('contact')
        address = request.POST.get('address')

        KidneyPatient.objects.create(
            user=user,
            name=name,
            age=age,
            blood_group=blood_group,
            hospital=hospital,
            doctor=doctor,
            contact=contact,
            address=address
        )

        return redirect('/')

    users = User.objects.all()
    return render(request,'kidney_patient.html',{'users':users})
# -------- LIVER --------

def liver_donor_register(request):
    if request.method == "POST":
        return redirect('liver-patient')
    users = User.objects.all()
    return render(request, "liver_donor.html", {"users": users})


def liver_patient_register(request):
    if request.method == "POST":
        return redirect('/')
    users = User.objects.all()
    return render(request, "liver_patient.html", {"users": users})


# -------- HEART --------

def heart_donor_register(request):
    if request.method == "POST":
        return redirect('heart-patient')
    users = User.objects.all()
    return render(request, "heart_donor.html")


def heart_patient_register(request):
    return render(request, "heart_patient.html")


# -------- EYE --------

def eye_donor_register(request):
     if request.method == "POST":
        return redirect('eye-patient')
     users = User.objects.all()
     return render(request, "eye_donor.html")


def eye_patient_register(request):
    return render(request, "eye_patient.html")


# -------- LUNG --------

def lung_donor_register(request):
     if request.method == "POST":
        return redirect('lung-patient')
     users = User.objects.all()
     return render(request, "lung_donor.html")


def lung_patient_register(request):
    return render(request, "lung_patient.html")


# -------- PANCREAS --------

def pancreas_donor_register(request):
     if request.method == "POST":
        return redirect('pancreas-patient')
     users = User.objects.all()
     return render(request, "pancreas_donor.html")


def pancreas_patient_register(request):
    return render(request, "pancreas_patient.html")

def emergency_support(request):

    if request.method == "POST":
        patient_name = request.POST['patient_name']
        organ = request.POST['organ']
        blood_group = request.POST['blood_group']
        hospital = request.POST['hospital']
        contact = request.POST['contact']
        details = request.POST['details']

        EmergencyRequest.objects.create(
            patient_name=patient_name,
            organ=organ,
            blood_group=blood_group,
            hospital=hospital,
            contact=contact,
            details=details
        )

        return redirect('/')

    return render(request, 'emergency_support.html')

from django.shortcuts import render, redirect
from .models import Volunteer
from django.contrib.auth.models import User

def volunteer_register(request):
    if request.method == "POST":
        contact = request.POST.get('contact')
        address = request.POST.get('address')
        aboutme = request.POST.get('aboutme')
        userpic = request.FILES.get('userpic')
        idpic = request.FILES.get('idpic')

        Volunteer.objects.create(
            user=request.user,
            contact=contact,
            address=address,
            aboutme=aboutme,
            userpic=userpic,
            idpic=idpic,
            status="Pending"
        )

        return redirect('volunteer_success')

    return render(request, 'volunteer_register.html')
def emergency_alerts(request):
    alerts = EmergencyAlert.objects.all().order_by('-created_date')
    return render(request, 'emergency_alerts.html', {'alerts': alerts})


def add_emergency_alert(request):
    if request.method == "POST":
        patient_name = request.POST.get('patient_name')
        organ_needed = request.POST.get('organ_needed')
        hospital = request.POST.get('hospital')
        contact_number = request.POST.get('contact_number')
        description = request.POST.get('description')
        location = request.POST.get('location')

        EmergencyAlert.objects.create(
            patient_name=patient_name,
            organ_needed=organ_needed,
            hospital=hospital,
            contact_number=contact_number,
            description=description,
            location=location
        )

        return redirect('emergency_alerts')

    return render(request, 'add_emergency_alert.html')


def blood_register(request):

    if request.method == "POST":
        fullname = request.POST.get('fullname')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        blood_group = request.POST.get('blood_group')
        city = request.POST.get('city')
        age = request.POST.get('age')
        address = request.POST.get('address')

        BloodDonor.objects.create(
            fullname=fullname,
            email=email,
            mobile=mobile,
            blood_group=blood_group,
            city=city,
            age=age,
            address=address
        )

        messages.success(request, "Blood Donation Registration Successful!")

        return redirect('blood_donation')
    # return redirect('blood_history')

    return render(request, 'blood_register.html')


def blood_donation(request):

    donors = BloodDonor.objects.all()

    return render(request, 'blood_donation.html', {'donors': donors})



def blood_history(request):
    donors = BloodDonor.objects.all()
    return render(request, 'history.html', {'donors': donors})

def donor_detail(request, pk):
    donor = get_object_or_404(Donor, pk=pk)
    return render(request, 'donor_detail.html', {'donor': donor})

def request_blood(request, donor_id):
    donor = get_object_or_404(Donor, pk=donor_id)

    if request.method == "POST":
        # ✅ Correct name access
        print(f"Blood request sent to {donor.user.username}")

        # ✅ Optional success message
        messages.success(request, "Blood request sent successfully!")

        return redirect('donor_list')   # change if needed

    return redirect('donor_list')

def hospital_partnership(request):
    hospitals = Hospital.objects.all()
    return render(request,'hospital_partnerships.html',{'hospitals':hospitals})

def all_services_data(request):

    donors = BloodDonor.objects.all()
    volunteers = Volunteer.objects.all()
    alerts = EmergencyAlert.objects.all()
    hospitals = Hospital.objects.all()
    history = DonationHistory.objects.all()

    context = {
        'donors': donors,
        'volunteers': volunteers,
        'alerts': alerts,
        'hospitals': hospitals,
        'history': history
    }

    return render(request, 'all_services_data.html', context)

# def request_list(request):
#     donors = Donor.objects.all()
#     return render(request, 'request_list.html', {
#         'donors': donors
#     })

# def accept_request(request, request_id):
#     req = get_object_or_404(PermisRequest, pk=request_id)
#     req.status = 'Accepted'
#     req.save()
#     return redirect('request_list')


# def reject_request(request, request_id):
#     req = get_object_or_404(PermisRequest, pk=request_id)
#     req.status = 'Rejected'
#     req.save()
#     return redirect('request_list')
# def request_blood(request, donor_id):
#     donor = get_object_or_404(Donor, pk=donor_id)

#     if request.method == "POST":
#         existing = PermisRequest.objects.filter(
#             donor=donor,
#             requested_by=request.user
#         ).last()

#         if not existing:
#             PermisRequest.objects.create(
#                 donor=donor,
#                 requested_by=request.user
#             )

#         return redirect('request_list')   # ✅ FIXED

#     return redirect('request_list')

# Show all donors
def request_list(request):
    donors = BloodDonor.objects.all()
    return render(request, 'request_list.html', {'donors': donors})


# ✅ Accept Request
def accept_request(request, pk):
    donor = get_object_or_404(BloodDonor, pk=pk)

    if request.method == "POST":
        donor.status = "Accepted"
        donor.save()

        messages.success(request, f"{donor.fullname} accepted successfully!")

    return redirect('request_list')


# ❌ Reject Request
def reject_request(request, pk):
    donor = get_object_or_404(BloodDonor, pk=pk)

    if request.method == "POST":
        donor.status = "Rejected"
        donor.save()

        messages.error(request, f"{donor.fullname} rejected.")

    return redirect('request_list')
    
def request_blood(request, donor_id):
    donor = get_object_or_404(Donor, pk=donor_id)

    if request.method == "POST":
        # ✅ Correct name access
        print(f"Blood request sent to {donor.user.username}")

        # ✅ Optional success message
        messages.success(request, "Blood request sent successfully!")

        return redirect('request_list')   # change if needed

    return redirect('request_list')

def user_logout(request):
    logout(request)
    return redirect('login') 