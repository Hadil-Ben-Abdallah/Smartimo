from django.db import models
from core.models import Property, TimeStampedModel
from property_listing.models import PropertyOwner 

class MapInterface(TimeStampedModel):
    map_service = models.CharField(max_length=255, blank=True, null=True)
    property_markers = models.JSONField(default=list, blank=True, null=True)
    search_filters = models.JSONField(default=dict, blank=True, null=True)
    custom_boundaries = models.JSONField(default=dict, blank=True, null=True)
    map_layers = models.JSONField(default=list, blank=True, null=True)

    def display_map(self):
        return {
            "map_service": self.map_service,
            "property_markers": self.property_markers,
            "search_filters": self.search_filters,
            "custom_boundaries": self.custom_boundaries,
            "map_layers": self.map_layers
        }

    def update_markers(self, new_filters):
        self.search_filters.update(new_filters)
        self.property_markers = self.filter_properties(self.search_filters)
        self.save()

    def set_custom_boundaries(self, boundaries):
        self.custom_boundaries = boundaries
        self.save()

    def add_layer(self, layer):
        self.map_layers.append(layer)
        self.save()


class MappingProperty(TimeStampedModel):
    location = models.CharField(max_length=255, blank=True, null=True)
    property_type = models.CharField(max_length=255, blank=True, null=True)
    owner = models.ForeignKey(PropertyOwner, on_delete=models.CASCADE)

    def get_property_details(self):
        return {
            "location": self.location,
            "property_type": self.property_type,
            "owner": self.owner.get_owner_details(),
        }

    def filter_properties(self, filters):
        filtered_properties = MappingProperty.objects.all()
        if 'property_type' in filters:
            filtered_properties = filtered_properties.filter(property_type=filters['property_type'])
        if 'location' in filters:
            filtered_properties = filtered_properties.filter(location__icontains=filters['location'])
        return [{"id": prop, "location": prop.location} for prop in filtered_properties]


class GISData(TimeStampedModel):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    boundary_info = models.TextField(blank=True, null=True)
    lot_size = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    parcel_data = models.TextField(blank=True, null=True)
    land_use = models.CharField(max_length=255, blank=True, null=True)

    def get_boundary_info(self):
        return self.boundary_info

    def get_lot_size(self):
        return self.lot_size

    def get_parcel_data(self):
        return self.parcel_data

    def get_land_use(self):
        return self.land_use


class MarketAnalytics(TimeStampedModel):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    market_trends = models.JSONField(default=dict, blank=True, null=True)
    property_values = models.JSONField(default=dict, blank=True, null=True)
    investment_opportunities = models.JSONField(default=dict, blank=True, null=True)

    def analyze_market_trends(self):
        trends = self.market_trends
        # Analyze trends
        return trends

    def get_property_values(self):
        return self.property_values

    def identify_investment_opportunities(self):
        opportunities = self.investment_opportunities
        # Identify opportunities
        return opportunities


class TenantResources(TimeStampedModel):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    nearby_amenities = models.JSONField(default=list, blank=True, null=True)
    neighborhood_guides = models.JSONField(default=dict, blank=True, null=True)
    community_resources = models.JSONField(default=dict, blank=True, null=True)

    def get_nearby_amenities(self):
        return self.nearby_amenities

    def get_neighborhood_guides(self):
        return self.neighborhood_guides

    def get_community_resources(self):
        return self.community_resources


class GeolocationMarketing(TimeStampedModel):
    id = models.CharField(max_length=255)
    target_area = models.JSONField(default=dict, blank=True, null=True)
    user_preferences = models.JSONField(default=dict, blank=True, null=True)
    advertisements = models.JSONField(default=list, blank=True, null=True)

    def create_campaign(self, campaign_data):
        self.target_area = campaign_data.get('target_area', self.target_area)
        self.user_preferences = campaign_data.get('user_preferences', self.user_preferences)
        self.advertisements = campaign_data.get('advertisements', self.advertisements)
        self.save()
        return self

    def target_users(self, location, preferences):
        self.target_area.update(location)
        self.user_preferences.update(preferences)
        self.save()

    def track_campaign_performance(self):
        performance_data = {
            "campaign_id": self.id,
            "click_through_rate": 0.05,
            "conversion_rate": 0.02,
            "roi": 15000,
        }
        return performance_data

