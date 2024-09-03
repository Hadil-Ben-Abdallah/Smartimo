from django.db import models
from core.models import Resource, Notification, TimeStampedModel
from lease_rental_management.models import Tenant, PropertyManager

class ResourceInfo(Resource):
    location = models.CharField(max_length=255, blank=True, null=True)
    capacity = models.IntegerField(blank=True, null=True)
    property_manager = models.ForeignKey(PropertyManager, on_delete=models.CASCADE)
    amenities = models.JSONField(default=dict, blank=True, null=True)
    availability_calendar = models.JSONField(default=dict, blank=True, null=True)
    booking_policies = models.JSONField(default=dict, blank=True, null=True)

    def view_resource_details(self):
        return {
            "location": self.location,
            "capacity": self.capacity,
            "property_manager": self.property_manager.username,
            "amenities": self.amenities,
            "availability_calendar": self.availability_calendar,
            "booking_policies": self.booking_policies
        }

    def check_availability(self, date, time):
        day_availability = self.availability_calendar.get(date)
        if not day_availability:
            return False
        for period in day_availability:
            start_time, end_time = period['start_time'], period['end_time']
            if start_time <= time < end_time:
                return False
        return True

    def update_availability_calendar(self, booking_date, start_time, end_time):
        day_availability = self.availability_calendar.get(booking_date, [])
        day_availability.append({
            "start_time": start_time,
            "end_time": end_time
        })
        self.availability_calendar[booking_date] = day_availability
        self.save()

    def apply_booking_policies(self, tenant, booking_request):
        if booking_request['attendee_count'] > self.capacity:
            return False, "Booking exceeds resource capacity."
        if 'tenants_only' in self.booking_policies and not isinstance(tenant, Tenant):
            return False, "Booking is restricted to tenants only."
        return True, "Booking is allowed."


class ResourceBooking(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    resource = models.ForeignKey(ResourceInfo, on_delete=models.CASCADE)
    booking_date = models.DateField(blank=True, null=True)
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    purpose = models.TextField(blank=True, null=True)
    attendee_count = models.IntegerField(blank=True, null=True)
    status = models.CharField(max_length=50, choices=[('confirmed', 'Confirmed'), ('pending', 'Pending'), ('canceled', 'Canceled'), ('rejected', 'Rejected'), ('unavailable', 'Unavailable')],default="pending")

    def create_booking(self):
        if not self.id.check_availability(self.booking_date, self.start_time):
            self.status = "unavailable"
            self.save()
            return False, "Resource is not available at the selected time."
        
        allowed, message = self.id.apply_booking_policies(self.tenant, {
            "attendee_count": self.attendee_count
        })
        if not allowed:
            self.status = "rejected"
            self.save()
            return False, message
        
        self.status = "confirmed"
        self.id.update_availability_calendar(self.booking_date, self.start_time, self.end_time)
        self.save()
        return True, "Booking confirmed."

    def update_booking(self, new_start_time, new_end_time):
        if self.status != "confirmed":
            return False, "Only confirmed bookings can be updated."

        day_availability = ResourceInfo.availability_calendar.get(self.booking_date, [])
        updated_availability = [period for period in day_availability if not (
            period['start_time'] == self.start_time and period['end_time'] == self.end_time
        )]
        ResourceInfo.availability_calendar[self.booking_date] = updated_availability
        self.id.save()

        self.start_time = new_start_time
        self.end_time = new_end_time
        self.id.update_availability_calendar(self.booking_date, self.start_time, self.end_time)
        self.save()

        return True, "Booking updated."

    def cancel_booking(self):
        if self.status not in ["confirmed", "pending"]:
            return False, "Cannot cancel a booking that is already canceled or unavailable."

        day_availability = ResourceInfo.availability_calendar.get(self.booking_date, [])
        updated_availability = [period for period in day_availability if not (
            period['start_time'] == self.start_time and period['end_time'] == self.end_time
        )]
        ResourceInfo.availability_calendar[self.booking_date] = updated_availability
        self.id.save()

        self.status = "canceled"
        self.save()

        return True, "Booking canceled."

    def view_booking_details(self):
        return {
            "tenant": self.tenant.username,
            "resource": self.id.view_resource_details(),
            "booking_date": self.booking_date,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "purpose": self.purpose,
            "attendee_count": self.attendee_count,
            "status": self.status
        }


class BookingNotification(Notification):
    booking = models.ForeignKey(ResourceBooking, on_delete=models.CASCADE)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    notification_type = models.CharField(max_length=50, choices=[('confirmation', 'Confirmation'), ('reminder', 'Reminder'), ('cancellation', 'Cancellation')], default='confirmation')

    def generate_notification_message(self):
        if self.notification_type == "confirmation":
            return f"Booking confirmed for {self.booking.view_booking_details()['resource']['location']} on {self.booking.booking_date}."
        elif self.notification_type == "reminder":
            return f"Reminder: You have a booking at {self.id.view_booking_details()['resource']['location']} on {self.booking.booking_date} at {self.booking.start_time}."
        elif self.notification_type == "cancellation":
            return f"Booking for {self.id.view_booking_details()['resource']['location']} on {self.booking.booking_date} has been canceled."
        else:
            return "Notification type not recognized."

    def schedule_reminder(self, remind_at):
        return f"Reminder scheduled for {remind_at}."


class ResourceBookingAdmin(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    property_manager = models.ForeignKey(PropertyManager, on_delete=models.CASCADE)
    resource = models.ForeignKey(ResourceInfo, on_delete=models.CASCADE)
    booking_policies = models.JSONField(default=dict, blank=True, null=True)
    availability_schedule = models.JSONField(default=dict, blank=True, null=True)

    def set_availability_schedule(self, new_schedule):
        self.availability_schedule = new_schedule
        self.resource.availability_calendar = new_schedule
        self.resource.save()
        self.save()

    def approve_booking_request(self, booking):
        if BookingNotification.status == "pending":
            BookingNotification.status = "confirmed"
            booking.save()
            Resource.resource_id.update_availability_calendar(booking.booking_date, booking.start_time, booking.end_time)
            return True, "Booking approved."
        return False, "Booking is not pending."

    def reject_booking_request(self, booking):
        if BookingNotification.status == "pending":
            BookingNotification.status = "rejected"
            booking.save()
            return True, "Booking rejected."
        return False, "Booking is not pending."

    def view_booking_reports(self):
        bookings = ResourceBooking.objects.filter(resource_id=self.resource.id)
        return bookings.values()

    def configure_booking_policies(self, new_policies):
        self.booking_policies = new_policies
        self.resource.booking_policies = new_policies
        self.resource.save()
        self.save()


class ResourceBookingAnalytics(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    resource = models.ForeignKey(ResourceInfo, on_delete=models.CASCADE)
    booking_data = models.JSONField(default=dict, blank=True, null=True)
    revenue_generated = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, blank=True, null=True)
    peak_booking_times = models.JSONField(default=dict, blank=True, null=True)

    def generate_booking_report(self):
        bookings = ResourceBooking.objects.filter(resource_id=self.resource.id)
        total_bookings = bookings.count()
        total_revenue = sum(booking.resource_id.apply_booking_policies()['price'] for booking in bookings)
        peak_times = {}
        for booking in bookings:
            hour = booking.start_time.hour
            peak_times[hour] = peak_times.get(hour, 0) + 1
        self.booking_data = {
            "total_bookings": total_bookings,
            "total_revenue": total_revenue,
            "peak_times": peak_times
        }
        self.save()

    def analyze_booking_trends(self):
        peak_times = self.booking_data.get("peak_times", {})
        most_popular_time = max(peak_times, key=peak_times.get, default=None)
        return {
            "most_popular_time": most_popular_time,
            "booking_trend": peak_times
        }

    def calculate_revenue(self):
        self.revenue_generated = sum(booking.resource_id.apply_booking_policies()['price'] for booking in ResourceBooking.objects.filter(resource_id=self.resource.id))
        self.save()

    def optimize_resource_allocation(self):
        trends = self.analyze_booking_trends()
        popular_times = trends.get("most_popular_time")
        return f"Allocate more resources during peak time: {popular_times}."


