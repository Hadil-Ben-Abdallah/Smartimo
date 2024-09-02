from django.db import models
from core.models import  User, Property, TimeStampedModel

class MarketplacePropertyListing(Property):
    marketplace_id = models.CharField(max_length=255, unique=True, null=True, blank=True)
    
    def upload_to_marketplace(self):
        if not self.marketplace_id:
            self.marketplace_id = "marketplace123"
            self.save()
            return {"success": True, "marketplace_id": self.marketplace_id}
        return {"success": False, "message": "Already uploaded"}

    def update_listing(self):
        if self.marketplace_id:
            return {"success": True, "message": "Listing updated successfully"}
        return {"success": False, "message": "Listing not uploaded to marketplace"}

    def synchronize_with_marketplace(self):
        if self.marketplace_id:
            return {"success": True, "message": "Synchronized with marketplace"}
        return {"success": False, "message": "Listing not uploaded to marketplace"}

    def receive_notification(self, notification):
        if notification.get('type') == 'update':
            self.synchronize_with_marketplace()
        elif notification.get('type') == 'status_change':
            pass

class Booking(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=50, choices=[('pending', 'Pending'), ('confirmed', 'Confirmed'), ('cancelled', 'Cancelled')], default='pending')
    marketplace_booking_id = models.CharField(max_length=255, unique=True, null=True, blank=True)

    def view_bookings(self):
        return Booking.objects.filter(user=self.user)

    def synchronize_bookings(self):
        if self.marketplace_booking_id:
            return {"success": True, "message": "Booking synchronized successfully"}
        return {"success": False, "message": "Booking not found in marketplace"}

    def receive_notification(self, notification):
        if notification.get('type') == 'booking_request':
            self.status = 'pending'
        elif notification.get('type') == 'booking_confirmation':
            self.status = 'confirmed'
        elif notification.get('type') == 'booking_cancellation':
            self.status = 'cancelled'
        self.save()
        return {"success": True, "status": self.status}

    def update_booking_status(self, status):
        self.status = status
        self.save()
        return {"success": True, "updated_status": self.status}

class Transaction(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='property_transactions')
    marketplace_property = models.ForeignKey(MarketplacePropertyListing, on_delete=models.CASCADE, related_name='marketplace_transactions')
    amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    commission = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=50, blank=True, null=True)
    marketplace_transaction_id = models.CharField(max_length=255, unique=True, null=True, blank=True)

    def record_transaction(self):
        if not self.marketplace_transaction_id:
            self.marketplace_transaction_id = "transaction123"
            self.save()
            return {"success": True, "transaction_id": self.marketplace_transaction_id}
        return {"success": False, "message": "Transaction already recorded"}

    def track_transaction(self):
        if self.marketplace_transaction_id:
            return {
                "status": self.status,
                "amount": self.amount,
                "commission": self.commission,
                "date": self.date,
                "marketplace_transaction_id": self.marketplace_transaction_id
            }
        return {"success": False, "message": "Transaction not recorded"}

    def reconcile_transactions(self):
        if self.marketplace_transaction_id:
            return {"success": True, "message": "Transaction reconciled successfully"}
        return {"success": False, "message": "Transaction not recorded"}

    def generate_transaction_report(self):
        return {
            "transaction_id": self.id,
            "property": self.property.property_id,
            "amount": self.amount,
            "commission": self.commission,
            "date": self.date,
            "status": self.status,
        }

class Availability(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    availability_dates = models.JSONField(default=list, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def update_availability(self):
        self.save()
        return {"success": True, "availability_dates": self.availability_dates, "price": self.price}

    def synchronize_availability(self):
        return {"success": True, "message": "Availability synchronized successfully"}

    def bulk_update_availability(self, availability_data):
        self.availability_dates = availability_data.get('availability_dates', self.availability_dates)
        self.price = availability_data.get('price', self.price)
        self.save()
        return {"success": True, "availability_dates": self.availability_dates, "price": self.price}

    def receive_notification(self, notification):
        if notification.get('type') == 'availability_update':
            self.synchronize_availability()

class UserAccount(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    password = models.CharField(max_length=128, blank=True, null=True)
    marketplace_user_id = models.CharField(max_length=255, unique=True, null=True, blank=True)

    def single_sign_on(self):
        if not self.marketplace_user_id:
            self.marketplace_user_id = "user123"
            self.save()
            return {"success": True, "marketplace_user_id": self.marketplace_user_id}
        return {"success": False, "message": "User already connected"}

    def unify_accounts(self):
        return {"success": True, "message": "Accounts unified successfully"}

    def navigate_to_marketplace(self):
        return {"success": True, "message": "Navigation to marketplace successful"}

    def maintain_session(self):
        return {"success": True, "message": "Session maintained successfully"}

