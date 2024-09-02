from django.db import models
from django.utils import timezone
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ["-created_at"]
        get_latest_by = "-created_at"


class Property(TimeStampedModel):
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
    address = models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    photos = models.ImageField(upload_to='photos/', blank=True, null=True)
    videos = models.FileField(upload_to='videos/', blank=True, null=True)
    size = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    bathroom_number = models.IntegerField(default=0, blank=True, null=True)
    badroom_number = models.IntegerField(default=0, blank=True, null=True)
    garage = models.BooleanField(default=False, blank=True, null=True)
    garden = models.BooleanField(default=False, blank=True, null=True)
    swiming_pool = models.BooleanField(default=False, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    year_built = models.DateField(auto_now=True, blank=True, null=True)
    status = models.CharField(max_length=50, blank=True, null=True)


class Notification(TimeStampedModel):
    notification_id = models.AutoField(primary_key=True)
    message = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=50, blank=True, null=True)
    date = models.DateTimeField(default=timezone.now, blank=True, null=True)

    def send_notification(self):
        pass

class Reminder(TimeStampedModel):
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
    message_content = models.TextField(blank=True, null=True)
    reminder_date = models.DateTimeField(blank=True, null=True)
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

class ClientInteraction(TimeStampedModel):
    client_interaction_id = models.AutoField(primary_key=True)
    interaction_type = models.CharField(max_length=50, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    def log_interactions(self):
        pass

class Communication(TimeStampedModel):
    communication_id = models.AutoField(primary_key=True)
    message = models.TextField(blank=True, null=True)
    date = models.DateTimeField(blank=True, null=True)

    def send_message(self):
        pass

class Report(TimeStampedModel):
    report_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50, blank=True, null=True)
    data = models.JSONField(blank=True, null=True)

class SalesOpportunity(TimeStampedModel):
    sales_opportunity_id = models.AutoField(primary_key=True)
    value = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    status = models.CharField(max_length=50, blank=True, null=True)

    def create_opportunity(self, value, status):
        self.value = value
        self.status = status
        self.save()


    def update_opportunity(self, value, status):
        if value:
            self.value = value
        if status:
            self.status = status
        self.save()

class Resource(TimeStampedModel):
    resource_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    contact_info = models.CharField(max_length=255, blank=True, null=True)

class User(TimeStampedModel):
    USER_TYPES = (
        ('client', 'Client'),
        ('lease_rental_tenant', 'Lease Rental Tenant'),
        ('property_owner', 'Property Owner'),
        ('property_manager', 'Property Manager'),
        ('staff_member', 'Staff Member'),
        ('inspector', 'Inspector'),
        ('vendor', 'Vendor'),
        ('prospective_buyer_renter', 'Prospective Buyer Renter'),
        ('real_estate_agent', 'Real Estate Agent'),
        ('real_estate_developer', 'Real Estate Developer'),
        ('prospective_tenant', 'Prospective Tenant')
    )
    
    user_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    username = models.CharField(unique=True, max_length=100, blank=True, null=True)
    password = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    cin = models.CharField(max_length=8, blank=True, null=True)
    birth_date = models.DateTimeField(auto_now=True, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.CharField(max_length=250, blank=True, null=True)
    credit_card_number = models.CharField(max_length=20, blank=True, null=True)
    job_title = models.CharField(max_length=100, blank=True, null=True)
    user_type = models.CharField(max_length=50, choices=USER_TYPES, default='client')

    def __str__(self):
        return self.username
    
class Document(TimeStampedModel):
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
    title = models.CharField(max_length=100, blank=True, null=True)
    document_type = models.CharField(max_length=50, choices=DOCUMENT_TYPES, default='contract')
    file_path = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    version = models.CharField(max_length=10, blank=True, null=True)
    access_permissions = models.JSONField(default=dict, blank=True, null=True)
    expiration_date = models.DateField(blank=True, null=True)

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

class Portal(TimeStampedModel):
    portal_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    version = models.CharField(max_length=50, blank=True, null=True)
    url = models.URLField(blank=True, null=True)

    def login(self, request, username, password):
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return "Login successful"
        else:
            return "Invalid credentials"

    def logout(self, request):
        auth_logout(request)
        return "Logout successful"

    def navigate(self, destination):
        return f"Navigating to {destination} within {self.name}."

class Feedback(TimeStampedModel):
    feedback_id = models.AutoField(primary_key=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True)
    comments = models.TextField(blank=True, null=True)

    # def edit_feedback(self, rating, comments):
    #     self.rating = rating
    #     self.comments = comments
    #     self.save()

    def delete_feedback(self):
        self.delete()

    def analyze_feedback(self):
        return Feedback.objects.values('rating').annotate(count=models.Count('rating'))
    
class Category(TimeStampedModel):
    category_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(null=True, blank=True)

    def create_category(self, name, description):
        self.name = name
        self.description = description
        self.save()
    
    def update_category(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.save()
    
    def delete_category(self):
        self.delete()

    def get_category_details(self):
        return {
            "id": self.category_id,
            "name": self.name,
            "description": self.description,
        }