# from django.contrib import admin
# from .models import RealEstateAgent, ThePropertyListing, PropertyOwner, ProspectiveBuyerRenter, SavedListing, PropertyNotification

# class RealEstateAgentAdmin(admin.ModelAdmin):
#     list_display = ('id', 'name', 'email', 'phone')
#     search_fields = ('name', 'email', 'phone')
#     filter_horizontal = ('listings',)

# class ThePropertyListingAdmin(admin.ModelAdmin):
#     list_display = ('property_listing_id', 'type', 'price', 'status', 'agent_id')
#     search_fields = ('address', 'type', 'price')
#     list_filter = ('type', 'status', 'agent_id')  # Ensure these fields exist in the model

# class PropertyOwnerAdmin(admin.ModelAdmin):
#     list_display = ('id', 'name', 'email', 'phone')
#     search_fields = ('name', 'email', 'phone')
#     filter_horizontal = ('properties',)

# class ProspectiveBuyerRenterAdmin(admin.ModelAdmin):
#     list_display = ('id', 'name', 'email')
#     search_fields = ('name', 'email')
#     filter_horizontal = ('saved_listings',)

# class SavedListingAdmin(admin.ModelAdmin):
#     list_display = ('id', 'user_id', 'property_id', 'created_at')
#     list_filter = ('created_at',)

# class PropertyNotificationAdmin(admin.ModelAdmin):
#     list_display = ('user_id', 'message', 'created_at')
#     search_fields = ('message',)
#     list_filter = ('created_at',)

# admin.site.register(RealEstateAgent, RealEstateAgentAdmin)
# admin.site.register(ThePropertyListing, ThePropertyListingAdmin)
# admin.site.register(PropertyOwner, PropertyOwnerAdmin)
# admin.site.register(ProspectiveBuyerRenter, ProspectiveBuyerRenterAdmin)
# admin.site.register(SavedListing, SavedListingAdmin)
# admin.site.register(PropertyNotification, PropertyNotificationAdmin)



