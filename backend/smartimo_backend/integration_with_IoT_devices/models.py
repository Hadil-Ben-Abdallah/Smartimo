from django.db import models

class IoTDevice(models.Model):
    DEVICE_TYPES = [
        ('thermostat', 'Smart Thermostat'),
        ('camera', 'Security Camera'),
        ('sensor', 'Environmental Sensor'),
        ('lock', 'Smart Lock'),
        ('leak_sensor', 'Water Leak Sensor'),
    ]

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    type = models.CharField(max_length=20, choices=DEVICE_TYPES)
    location = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=20, choices=[('online', 'Online'), ('offline', 'Offline')], default='offline')

    def add_device(self, name, device_type, location, status='offline'):
        new_device = IoTDevice.objects.create(
            name=name, 
            type=device_type, 
            location=location, 
            status=status
        )
        return new_device

    def update_device(self, name=None, location=None, status=None):
        if name:
            self.name = name
        if location:
            self.location = location
        if status:
            self.status = status
        self.save()
        return self

    def remove_device(self):
        self.delete()

    def get_device_details(self):
        return {
            'id': self.id,
            'name': self.name,
            'type': self.type,
            'location': self.location,
            'status': self.status
        }

class SmartThermostat(IoTDevice):
    temperature = models.FloatField(blank=True, null=True)
    setpoint = models.FloatField(blank=True, null=True)
    mode = models.CharField(max_length=20, choices=[('heating', 'Heating'), ('cooling', 'Cooling'), ('off', 'Off')], default='off')
    schedule = models.JSONField(default=dict, blank=True, null=True)

    def adjust_temperature(self, new_setpoint):
        self.setpoint = new_setpoint
        self.save()

    def set_schedule(self, new_schedule):
        self.schedule = new_schedule
        self.save()

    def get_temperature_data(self):
        return {
            'temperature': self.temperature,
            'setpoint': self.setpoint,
            'mode': self.mode,
            'schedule': self.schedule
        }

    def send_alert(self, message):
        print(f"Alert: {message}")

class SecurityCamera(IoTDevice):
    video_feed_url = models.URLField(blank=True, null=True)
    recording_schedule = models.JSONField(default=dict, blank=True, null=True)
    motion_detection_zones = models.JSONField(default=dict, blank=True, null=True)
    storage_options = models.JSONField(default=dict, blank=True, null=True)

    def view_live_feed(self):
        return self.video_feed_url

    def review_recorded_footage(self):
        return "Recorded footage data"

    def configure_camera(self, settings):
        if 'recording_schedule' in settings:
            self.recording_schedule = settings['recording_schedule']
        if 'motion_detection_zones' in settings:
            self.motion_detection_zones = settings['motion_detection_zones']
        if 'storage_options' in settings:
            self.storage_options = settings['storage_options']
        self.save()

    def send_motion_alert(self, message):
        print(f"Motion Alert: {message}")

class EnvironmentalSensor(IoTDevice):
    air_quality = models.FloatField(blank=True, null=True)
    humidity = models.FloatField(blank=True, null=True)
    temperature = models.FloatField(blank=True, null=True)
    carbon_monoxide_level = models.FloatField(blank=True, null=True)

    def monitor_environment(self):
        return {
            'air_quality': self.air_quality,
            'humidity': self.humidity,
            'temperature': self.temperature,
            'carbon_monoxide_level': self.carbon_monoxide_level
        }

    def set_alert_thresholds(self, thresholds):
        for key, value in thresholds.items():
            setattr(self, key, value)
        self.save()

    def get_environmental_data(self):
        return {
            'air_quality': self.air_quality,
            'humidity': self.humidity,
            'temperature': self.temperature,
            'carbon_monoxide_level': self.carbon_monoxide_level
        }

    def send_environmental_alert(self, message):
        print(f"Environmental Alert: {message}")

class SmartLock(IoTDevice):
    lock_status = models.CharField(max_length=20, choices=[('locked', 'Locked'), ('unlocked', 'Unlocked')],default='locked')
    access_profiles = models.JSONField(default=dict, blank=True, null=True)
    access_history = models.JSONField(default=dict, blank=True, null=True)

    def control_lock(self, action):
        if action in ['lock', 'unlock']:
            self.lock_status = action
            self.save()

    def create_access_profile(self, profile):
        profile_id = f"profile_{len(self.access_profiles) + 1}"
        self.access_profiles[profile_id] = profile
        self.save()

    def grant_access(self, tenant_id, access_code):
        self.access_profiles[tenant_id] = access_code
        self.save()

    def revoke_access(self, tenant_id):
        if tenant_id in self.access_profiles:
            del self.access_profiles[tenant_id]
            self.save()

    def get_access_history(self):
        return self.access_history

class WaterLeakSensor(IoTDevice):
    water_usage = models.FloatField(blank=True, null=True)
    leak_detected = models.BooleanField(default=False, blank=True, null=True)
    moisture_level = models.FloatField(blank=True, null=True)

    def monitor_water_usage(self):
        return {
            'water_usage': self.water_usage,
            'leak_detected': self.leak_detected,
            'moisture_level': self.moisture_level
        }

    def set_leak_thresholds(self, thresholds):
        for key, value in thresholds.items():
            setattr(self, key, value)
        self.save()

    def get_water_data(self):
        return {
            'water_usage': self.water_usage,
            'leak_detected': self.leak_detected,
            'moisture_level': self.moisture_level
        }

    def send_leak_alert(self, message):
        print(f"Water Leak Alert: {message}")

