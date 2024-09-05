from django.db import models
from core.models import User, Property, Notification, TimeStampedModel

class Agency(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    bank_partnership = models.CharField(max_length=255, blank=True, null=True)
    founding_date = models.DateField(blank=True, null=True)
    bank_code = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    website_link = models.URLField(blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)

    def create_agency(self, **kwargs):
        return Agency.objects.create(**kwargs)

    def update_agency(self, **kwargs):
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        self.save()
        return self

    def delete_agency(self):
        self.delete()

    def get_agency(self):
        return {
            'name': self.name,
            'bank_partnership': self.bank_partnership,
            'founding_date': self.founding_date,
            'bank_code': self.bank_code,
            'description': self.description,
            'email': self.email,
            'website_link': self.website_link,
            'phone_number': self.phone_number,
            'location': self.location,
        }

class RealEstateAgent(User):
    agency = models.ForeignKey(Agency, on_delete=models.CASCADE, related_name='agent_agency')
    clients_list = models.JSONField(default=list, blank=True, null=True)

    def view_listings(self):
        return ThePropertyListing.get_listing()

    def edit_listing(self, **kwargs):
        try:
            listing = ThePropertyListing.get_listing()
            for attr, value in kwargs.items():
                setattr(listing, attr, value)
            listing.save()
            return listing
        except ThePropertyListing.DoesNotExist:
            return None
    
    # def view_clients(self):
    #     return self.clients.all()
    
    # def assign_tag(self, client, tag):
    #     client.tags.append(tag)
    #     client.save()
    
    # def filter_clients(self, tag):
    #     return self.clients.filter(tags__contains=[tag])
    
    def receive_notifications(self):
        notifications = []
        notifications = Notification.objects.filter(agent_id=self.user_id)
        return notifications

class ThePropertyListing(Property):
    agent = models.ForeignKey(RealEstateAgent, on_delete=models.CASCADE)
    
    def create_listing(self, **kwargs):
        return ThePropertyListing.objects.create(**kwargs)

    def update_listing(self, **kwargs):
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        self.save()
        return self

    def delete_listing(self):
        self.delete()

    def get_listing(self):
        return {
            'address': self.address,
            'type': self.type,
            'size': self.size,
            'price': self.price,
            'photos': self.photos,
            'videos': self.videos,
        }

class PropertyOwner(User):
    properties = models.ForeignKey(ThePropertyListing, on_delete=models.CASCADE, related_name='owner_properties')

    def get_owner_details(self):
        return {
            'name': self.username,
            'email': self.email,
            'phone': self.phone,
            'address': self.address,
            'properties': list(self.properties.values('id', 'address', 'type', 'size', 'price'))
        }

    def add_property(self, property):
        self.properties.add(property)

    def update_property(self, property_id, **kwargs):
        try:
            property = self.properties.get(id=property_id)
            for attr, value in kwargs.items():
                setattr(property, attr, value)
            property.save()
            return property
        except ThePropertyListing.DoesNotExist:
            return None

class SavedListing(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    property = models.ForeignKey(ThePropertyListing, on_delete=models.CASCADE)

    def save_listing(self):
        self.save()

    def get_saved_listings(self):
        return self

class ProspectiveBuyerRenter(User):
    preferences = models.JSONField(blank=True, null=True)
    saved_listings = models.ForeignKey(SavedListing, on_delete=models.CASCADE, related_name='saved_by')

    def search_properties(self):
        filters = self.preferences
        properties = ThePropertyListing.objects.filter(**filters)
        return properties

    def save_listing(self, listing):
        self.saved_listings.add(listing)

    def subscribe_notifications(self):
        pass

class PropertyNotification(Notification):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def get_notifications(self):
        return PropertyNotification.objects.filter(user_id=self.user_id).order_by('-created_at')
