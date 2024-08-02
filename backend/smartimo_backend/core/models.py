from django.db import models
from django.utils import timezone

class Property(models.Model):
    property_id = models.AutoField(primary_key=True)
    address = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

class Notification(models.Model):
    notification_id = models.AutoField(primary_key=True)
    status = models.CharField(max_length=50)

    def send_notification(self):
        pass

class ClientInteraction(models.Model):
    client_interaction_id = models.AutoField(primary_key=True)
    interaction_type = models.CharField(max_length=50)
    notes = models.TextField()

    def log_interactions(self):
        pass

# class LeaseAgreement(models.Model):
#     lease_id = models.AutoField(primary_key=True)
#     start_date = models.DateField()
#     end_date = models.DateField()
#     rent_amount = models.DecimalField(max_digits=10, decimal_places=2)
#     security_deposit = models.DecimalField(max_digits=10, decimal_places=2)

class Communication(models.Model):
    communication_id = models.AutoField(primary_key=True)
    message = models.TextField()
    date = models.DateTimeField()

    def send_message(self):
        pass

class PropertyListing(models.Model):
    property_listing_id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    description = models.TextField()
    photo = models.ImageField(upload_to='photos/')
    video = models.FileField(upload_to='videos/')
    size = models.DecimalField(max_digits=10, decimal_places=2)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50)

class FinancialReport(models.Model):
    financial_report_id = models.AutoField(primary_key=True)
    financial_data = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class SalesOpportunity(models.Model):
    sales_opportunity_id = models.AutoField(primary_key=True)
    value = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50)

    def create_opportunity(self):
        pass

    def update_opportunity(self):
        pass

class Resource(models.Model):
    resource_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    content = models.TextField()
    contact_info = models.CharField(max_length=255)

from django.db import models

class User(models.Model):
    USER_TYPES = (
        ('client', 'Client'),
        ('lease_rental_tenant', 'Lease Rental Tenant'),
        ('property_owner', 'Property Owner'),
        ('property_manager', 'Property Manager'),
        ('prospective_buyer_renter', 'Prospective Buyer Renter'),
        ('real_estate_agent', 'Real Estate Agent'),
    )
    
    user_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    cin = models.CharField(max_length=8)
    birth_date = models.DateTimeField(auto_now=True)
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=250)
    user_type = models.CharField(max_length=50, choices=USER_TYPES, default='client')

    def __str__(self):
        return self.name


class Vendor(models.Model):
    vendor_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    certifications = models.TextField()

    def create_profile(self):
        pass

