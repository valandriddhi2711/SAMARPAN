from django.contrib import admin
from .models import *
from .models import Service

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    search_fields = ('title', 'description')

@admin.register(Donor)
class DonorAdmin(admin.ModelAdmin):
    list_display = ('user', 'contact', 'address', 'userpic', 'regdate')
    # search_fields = ['user__username', 'Contact']
    # list_filter = ['address']

@admin.register(Volunteer)
class VolunteerAdmin(admin.ModelAdmin):
    list_display = ['user', 'Contact', 'address']

admin.site.register(DonationArea)
admin.site.register(Donation)
admin.site.register(Gallery)
@admin.register(GiftDonation)
class GiftDonationAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'company',
        'campaign',
        'amount',
        'matched_amount',
        'status',
        'created_at',
    )

    list_filter = ('status', 'company', 'campaign')
    search_fields = ('user__username', 'company__name')
    ordering = ('-created_at',)

    actions = ['approve_donations', 'reject_donations']

    def approve_donations(self, request, queryset):
        queryset.update(status='approved')

    def reject_donations(self, request, queryset):
        queryset.update(status='rejected')
