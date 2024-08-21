from django.db import models
from core.models import User, Property, Notification

class Agency(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    bank_partnership = models.CharField(max_length=255)
    founding_date = models.DateField()
    bank_code = models.CharField(max_length=100)
    description = models.TextField()
    email = models.EmailField()
    website_link = models.URLField()
    phone_number = models.CharField(max_length=20)
    location = models.CharField(max_length=255)

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

    def view_listings(self):
        return self.listings.all()

    def edit_listing(self, listing_id, **kwargs):
        try:
            listing = self.listings.get(id=listing_id)
            for attr, value in kwargs.items():
                setattr(listing, attr, value)
            listing.save()
            return listing
        except ThePropertyListing.DoesNotExist:
            return None

    def receive_notifications(self):
        return PropertyNotification.objects.filter(user_id=self.id).order_by('-id')

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
    properties = models.ManyToManyField(ThePropertyListing, related_name='owner_properties')

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

class ProspectiveBuyerRenter(User):
    preferences = models.JSONField()
    saved_listings = models.ManyToManyField('ThePropertyListing', related_name='saved_by')

    def search_properties(self):
        filters = self.preferences
        properties = ThePropertyListing.objects.filter(**filters)
        return properties

    def save_listing(self, listing):
        self.saved_listings.add(listing)

    def subscribe_notifications(self):
        pass

class SavedListing(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(ProspectiveBuyerRenter, on_delete=models.CASCADE)
    property = models.ForeignKey(ThePropertyListing, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def save_listing(self):
        self.save()

    def get_saved_listings(self):
        return self.user.saved_listings.all()

class PropertyNotification(Notification):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def get_notifications(self):
        return PropertyNotification.objects.filter(user_id=self.user_id).order_by('-created_at')
