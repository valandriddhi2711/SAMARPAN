from django.db import models
from django.contrib.auth.models import User

class Donor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    contact = models.CharField(max_length=15, null=True)
    address = models.CharField(max_length=300, null=True)
    userpic = models.ImageField(upload_to="donor_pics/", null=True, blank=True)
    regdate = models.DateTimeField(auto_now_add=True)

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
