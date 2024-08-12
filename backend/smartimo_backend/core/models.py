from django.db import models
from django.utils import timezone
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout

class Property(models.Model):
    PROPERTY_TYPES = [
        ('residential', 'Residential'),
        ('commercial', 'Commercial'),
        ('mixed_use', 'Mixed Use'),
        ('land', 'Land'),
        ('special_purpose', 'Special Purpose'),
        ('investment', 'Investment'),
        ('luxury', 'Luxury'),
        ('recreational', 'Recreational'),
        ('development', 'Development'),
    ]

    property_id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=50, choices=PROPERTY_TYPES, default='residential')
    address = models.CharField(max_length=50)
    description = models.TextField()
    photos = models.ImageField(upload_to='photos/')
    videos = models.FileField(upload_to='videos/')
    size = models.DecimalField(max_digits=10, decimal_places=2)
    bathroom_number = models.IntegerField(default=0)
    badroom_number = models.IntegerField(default=0)
    garage = models.BooleanField(default=False)
    garden = models.BooleanField(default=False)
    swiming_pool = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    year_built = models.DateField(auto_now=True)
    status = models.CharField(max_length=50)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

class Notification(models.Model):
    notification_id = models.AutoField(primary_key=True)
    message = models.TextField()
    status = models.CharField(max_length=50)
    date = models.DateTimeField(default=timezone.now)

    def send_notification(self):
        pass

class Reminder(models.Model):
    REMINDER_FREQUENCY = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('quartly', 'Quartly'),
        ('bi-annually', 'Bi-annually'),
        ('annually', 'Annually'),
    ]
    DELIVARY_CHANNEL = [
        ('email', 'Email'),
        ('sms', 'SMS'),
        ('in_platform_alert', 'In-platform Alert'),
    ]
    REMINDER_STATUS = [
        ('scheduled', 'Scheduled'),
        ('sent', 'Sent')
    ]
    reminder_id = models.AutoField(primary_key=True)
    message_content = models.TextField()
    reminder_date = models.DateTimeField()
    frequency = models.CharField(max_length=50, choices=REMINDER_FREQUENCY, default='daily')
    delivary_channel = models.CharField(max_length=50, choices=DELIVARY_CHANNEL, default='email')
    status = models.CharField(max_length=50, choices=REMINDER_STATUS, default='scheduled')

    def create_reminder(self, reminder_date):
        self.reminder_date = reminder_date
        self.save()
    
    def update_reminder(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.save()
    
    def send_reminder(self):
        self.status = 'sent'
        self.save()

    def delete_reminder(self):
        self.delete()


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

# class PropertyListing(models.Model):
#     property_listing_id = models.AutoField(primary_key=True)
#     type = models.CharField(max_length=50)
#     address = models.CharField(max_length=50)
#     description = models.TextField()
#     photo = models.ImageField(upload_to='photos/')
#     video = models.FileField(upload_to='videos/')
#     size = models.DecimalField(max_digits=10, decimal_places=2)
#     bathroom_number = models.IntegerField(default=0)
#     badroom_number = models.IntegerField(default=0)
#     garage = models.BooleanField(default=False)
#     garden = models.BooleanField(default=False)
#     swiming_pool = models.BooleanField(default=False)
#     price = models.DecimalField(max_digits=10, decimal_places=2)
#     year_built = models.DateField(auto_now=True)
#     status = models.CharField(max_length=50)

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
    description = models.TextField()
    contact_info = models.CharField(max_length=255)

class User(models.Model):
    USER_TYPES = (
        ('client', 'Client'),
        ('lease_rental_tenant', 'Lease Rental Tenant'),
        ('property_owner', 'Property Owner'),
        ('property_manager', 'Property Manager'),
        ('vendor', 'Vendor'),
        ('prospective_buyer_renter', 'Prospective Buyer Renter'),
        ('real_estate_agent', 'Real Estate Agent'),
        ('prospective_tenant', 'Prospective Tenant')
    )
    
    user_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    username = models.CharField(unique=True, max_length=100)
    password = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    cin = models.CharField(max_length=8)
    birth_date = models.DateTimeField(auto_now=True)
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=250)
    credit_card_number = models.CharField(max_length=20)
    job_title = models.CharField(max_length=100)
    user_type = models.CharField(max_length=50, choices=USER_TYPES, default='client')

    def __str__(self):
        return self.username
    
class Document(models.Model):
    DOCUMENT_TYPES = (
        ('contract', 'Contract'),
        ('agreement', 'Agreement'),
        ('deed', 'Deed'),
        ('lease', 'Lease'),
        ('addendum', 'Addentum'),
        ('inspection_report', 'Inspection Report'),
        ('insurance_policy', 'Insurance Policy'),
    )

    document_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    document_type = models.CharField(max_length=50, choices=DOCUMENT_TYPES, default='contract')
    file_path = models.CharField(max_length=255)
    description = models.TextField()
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    version = models.CharField(max_length=10)
    access_permissions = models.JSONField(default=dict)
    expiration_date = models.DateField()

    def upload_document(self, file_path):
        self.file_path = file_path
        self.save()
    
    def update_document(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.save()
    
    def set_permissions(self, permissions):
        self.access_permissions = permissions
        self.save()

class Portal(models.Model):
    portal_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    version = models.CharField(max_length=50)
    url = models.URLField()

    def login(self, request, username, password):
        """
        Authenticates the user and logs them in.
        :param request: The HTTP request object
        :param username: The username of the user
        :param password: The password of the user
        :return: Success or failure message
        """
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return "Login successful"
        else:
            return "Invalid credentials"

    def logout(self, request):
        """
        Logs the user out.
        :param request: The HTTP request object
        :return: Success message
        """
        auth_logout(request)
        return "Logout successful"

    def navigate(self, destination):
        return f"Navigating to {destination} within {self.portal_name}."
# class Vendor(models.Model):
#     vendor_id = models.AutoField(primary_key=True)
#     name = models.CharField(max_length=100)
#     certifications = models.TextField()

#     def create_profile(self):
#         pass

