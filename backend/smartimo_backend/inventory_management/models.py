from django.db import models
from datetime import datetime
from core.models import Property, Notification, TimeStampedModel
from lease_rental_management.models import PropertyManager

class InventoryProperty(Property):
    listing_type = models.CharField(max_length=50, choices=[('rental', 'Rental'), ('sale', 'Sale')], default='rental')
    furnished = models.BooleanField(default=False, blank=True, null=True)
    
    def add_inventory_item(self, item):
        item.property = self
        item.save()

    def remove_inventory_item(self, item_id):
        item = InventoryItem.objects.get(id=item_id)
        if item.property == self:
            item.delete()

    def update_property_details(self, details):
        for key, value in details.items():
            setattr(self, key, value)
        self.save()

    def get_inventory_items(self):
        return InventoryItem.objects.filter(property=self)

    def get_inventory(self):
        return self.get_inventory_items()

class InventoryItem(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    property = models.ForeignKey(InventoryProperty, on_delete=models.CASCADE, related_name='inventory_items')
    category = models.CharField(max_length=50, choices=[('furniture', 'furniture'), ('appliances', 'Appliances'), ('electronics', 'Electronics')], default='furniture')
    name = models.CharField(max_length=100, blank=True, null=True)
    quantity = models.IntegerField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    condition = models.CharField(max_length=50, choices=[('new', 'New'), ('good', 'Good'), ('fair', 'Fair'), ('poor', 'Poor')], default='new')
    photos = models.JSONField(default=list, blank=True, null=True)

    def update_item_details(self, details):
        for key, value in details.items():
            setattr(self, key, value)
        self.save()

    def get_item_photos(self):
        return self.photos

    def add_photo(self, photo_url):
        self.photos.append(photo_url)
        self.save()

    def remove_photo(self, photo_url):
        if photo_url in self.photos:
            self.photos.remove(photo_url)
            self.save()

class MaintenanceLog(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    item = models.ForeignKey(InventoryItem, related_name='maintenance_logs', on_delete=models.CASCADE)
    activity = models.TextField(blank=True, null=True)
    service_provider = models.CharField(max_length=100, blank=True, null=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    next_maintenance_date = models.DateField(null=True, blank=True)

    def record_maintenance(self, activity, service_provider, cost, date, next_maintenance_date=None):
        self.activity = activity
        self.service_provider = service_provider
        self.cost = cost
        self.date = date
        self.next_maintenance_date = next_maintenance_date
        self.save()

    def get_maintenance_history(self, item_id):
        return MaintenanceLog.objects.filter(item_id=item_id)

    def schedule_next_maintenance(self, date):
        self.next_maintenance_date = date
        self.save()

class DepreciationRecord(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    item = models.ForeignKey(InventoryItem, related_name='depreciation_records', on_delete=models.CASCADE)
    initial_value = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    current_value = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    depreciation_rate = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    depreciation_value = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, blank=True, null=True)
    last_depreciation_date = models.DateField(auto_now_add=True, blank=True, null=True)

    def calculate_depreciation(self):
        time_elapsed = (datetime.date.today() - self.last_depreciation_date) / 365
        self.depreciation_value = self.initial_value * (self.depreciation_rate / 100) * time_elapsed
        self.current_value -= self.depreciation_value
        self.last_depreciation_date = datetime.date.today()
        self.save()

    def update_depreciation_record(self):
        self.calculate_depreciation()

    def get_depreciation_schedule(self):
        return {
            'initial_value': self.initial_value,
            'current_value': self.current_value,
            'depreciation_value': self.depreciation_value,
            'last_depreciation_date': self.last_depreciation_date,
        }

class InventoryNotification(Notification):
    property_manager = models.ForeignKey(PropertyManager, on_delete=models.CASCADE)
    type = models.CharField(max_length=100, choices=[('maintenance', 'Maintenance'), ('reminder', 'Reminder'), ('inventory_update', 'Inventory Update')])

    def update_status(self, status):
        self.status = status
        self.save()

    def view_notification_history(self, property_manager_id):
        return InventoryNotification.objects.filter(property_manager=property_manager_id)

