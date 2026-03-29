import random
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from datetime import date





class Donor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    contact = models.CharField(max_length=15, null=True)
    address = models.CharField(max_length=300, null=True)
    userpic = models.ImageField(upload_to="donor_pics/", null=True, blank=True)
    regdate = models.DateTimeField(auto_now_add=True)
    date_of_birth = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.user.username
    @property
    def age(self):
        if self.date_of_birth:
            today = date.today()
            return today.year - self.date_of_birth.year - (
                (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
            )
        return None

    def __str__(self):
        return self.user.username


class Volunteer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    Contact = models.CharField(max_length=15, null=True)
    address = models.CharField(max_length=300, null=True)
    userpic = models.FileField(null=True)
    idpic = models.FileField(null=True)
    aboutme = models.CharField(max_length=300, null=True)
    status = models.CharField(max_length=20, null=True)
    regdate = models.DateTimeField(auto_now_add=True)
    adminremark = models.CharField(max_length=300, null=True)
    updationdate = models.DateField(null=True)

    def __str__(self):
        return self.user.username  # ✅ fixed typo


class DonationArea(models.Model):
    areaname = models.CharField(max_length=100, null=True)
    description = models.CharField(max_length=300, null=True)
    creationdate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.areaname


class Donation(models.Model):
    donor = models.ForeignKey(Donor, on_delete=models.CASCADE)
    donationname = models.CharField(max_length=100, null=True)
    donationpic = models.FileField(null=True)
    collectionloc = models.CharField(max_length=300, null=True)
    description = models.CharField(max_length=300, null=True)
    status = models.CharField(max_length=50, null=True)
    donationdate = models.DateTimeField(auto_now_add=True)
    adminremark = models.CharField(max_length=300, null=True)
    volunteer = models.ForeignKey(Volunteer, on_delete=models.CASCADE, null=True, blank=True)
    donationArea = models.ForeignKey(DonationArea, on_delete=models.CASCADE, null=True, blank=True)
    volunteerremark = models.CharField(max_length=300, null=True)
    updationdate = models.DateField(null=True)

    def __str__(self):
        return f"{self.donationname} by {self.donor.user.username}"


class Gallery(models.Model):
    donation = models.ForeignKey(Donation, on_delete=models.CASCADE)
    deliverypic = models.FileField(upload_to="delivery_gallery/", null=True, blank=True)
    creationdate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"DeliveryPic {self.id}"


# from django.db import models

# class MyUUIDModel(models.Model):
#     username = models.CharField(max_length=100)
#     regnumber = models.IntegerField(unique=True)

#     def __str__(self):
#         return f"{self.username} - {self.regnumber}"

class Service(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    icon = models.CharField(max_length=100, blank=True)
    image = models.ImageField(upload_to='services/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    booking_date = models.DateField()
    booking_time = models.TimeField()
    status = models.CharField(max_length=20, choices=[('pending','Pending'), ('confirmed','Confirmed')], default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.service.title}"
    
class Company(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Campaign(models.Model):
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title


class GiftDonation(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)

    contributor_name = models.CharField(max_length=150)
    email = models.EmailField()

    amount = models.DecimalField(max_digits=10, decimal_places=2)
    matched_amount = models.DecimalField(max_digits=10, decimal_places=2)

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.company.name}"
    
status = models.CharField(
    max_length=10,
    choices=(
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
    )
)

class EmailOTP(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.otp = str(random.randint(100000, 999999))
        super().save(*args, **kwargs)

    def is_expired(self):
        return timezone.now() > self.created_at + timedelta(minutes=5)

    def __str__(self):
        return f"{self.user.username} - {self.otp}"
# from django.db import models

class OrganTransplant(models.Model):
    year = models.IntegerField()
    state = models.CharField(max_length=100)
    transplants = models.IntegerField()

    def __str__(self):
        return f"{self.state} - {self.year}"
    
class HealthCheckup(models.Model):

    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    age = models.IntegerField()

    CHECKUP_CHOICES = [
        ('Full Body', 'Full Body Checkup'),
        ('Blood Test', 'Blood Test'),
        ('Heart', 'Heart Checkup'),
        ('Kidney', 'Kidney Checkup'),
        ('Liver', 'Liver Checkup'),
        ('Diabetes', 'Diabetes Test'),
        ('Eye', 'Eye Checkup'),
        ('Dental', 'Dental Checkup'),
        ('BP', 'Blood Pressure Check'),
        ('Thyroid', 'Thyroid Test'),
    ]

    checkup_type = models.CharField(max_length=50, choices=CHECKUP_CHOICES)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class KidneyDonor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    age = models.IntegerField()
    blood_group = models.CharField(max_length=5)
    contact = models.CharField(max_length=15)
    address = models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class KidneyPatient(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    age = models.IntegerField()
    blood_group = models.CharField(max_length=5)
    hospital = models.CharField(max_length=200)
    contact = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
    
class EmergencyAlert(models.Model):
    patient_name = models.CharField(max_length=100)
    organ_needed = models.CharField(max_length=50)
    hospital = models.CharField(max_length=200)
    contact_number = models.CharField(max_length=15)
    description = models.TextField()
    location = models.CharField(max_length=200)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.patient_name
    
class BloodDonor(models.Model):
    fullname = models.CharField(max_length=100)
    age = models.IntegerField(null=True, blank=True)
    blood_group = models.CharField(max_length=5)
    city = models.CharField(max_length=100)
    mobile = models.CharField(max_length=15)

    status = models.CharField(max_length=20, default='Pending')

    def __str__(self):
        return self.fullname
    
class DonationHistory(models.Model):
    donor = models.ForeignKey(BloodDonor, on_delete=models.CASCADE)
    hospital = models.CharField(max_length=200)
    donation_date = models.DateField()
    units = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.donor.fullname} - {self.donation_date}"



class Hospital(models.Model):
    hospital_name = models.CharField(max_length=150)
    location = models.CharField(max_length=200)
    contact_details = models.CharField(max_length=20)
    supported_services = models.TextField()

    def __str__(self):
        return self.hospital_name
    
class PermisRequest(models.Model):
    donor = models.ForeignKey(
        Donor,
        on_delete=models.CASCADE,
        related_name="requests"   # ✅ IMPORTANT
    )
    requested_by = models.ForeignKey(User, on_delete=models.CASCADE)

    status = models.CharField(
        max_length=10,
        choices=[
            ('Pending', 'Pending'),
            ('Accepted', 'Accepted'),
            ('Rejected', 'Rejected')
        ],
        default='Pending'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']   # ✅ ADD THIS

    def __str__(self):
        return f"{self.donor} - {self.status}"
    
class BloodDonation(models.Model):
    donor = models.ForeignKey(Donor, on_delete=models.CASCADE)
    donationname = models.CharField(max_length=100)
    donationdate = models.DateField()
    blood_group = models.CharField(max_length=5, null=True)
    city = models.CharField(max_length=100, null=True)

    class Meta:
        ordering = ['-donationdate']   # ✅ Latest first
    
   
