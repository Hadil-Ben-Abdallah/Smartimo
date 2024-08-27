from django.db import models
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.core.exceptions import ValidationError
from core.models import User, Property, Communication, Notification

class MobileApp(models.Model):
    id = models.AutoField(primary_key=True)
    app_name = models.CharField(max_length=255)
    version = models.CharField(max_length=50)
    platform = models.CharField(max_length=50)
    store_url = models.URLField()

    def install(self):
        return f"Guide for installing {self.app_name} on {self.platform} can be found at {self.store_url}"

    def update(self):
        return f"Updating {self.app_name} to version {self.version} on {self.platform}."

    def navigate(self, destination):
        return f"Navigating to {destination} within {self.app_name}."

class AppProperty(Property):
    features = models.JSONField(default=list)
    saved = models.BooleanField(default=False)

    def search_listings(self, search_criteria):
        properties = Property.objects.filter(**search_criteria)
        return properties

    def view_details(self):
        return {
            "type": self.type,
            "address": self.address,
            "description": self.description,
            "photos": self.photos,
            "videos": self.videos,
            "size": self.size,
            "bathroom_number": self.bathroom_number,
            "badroom_number": self.badroom_number,
            "garage": self.garage,
            "garden": self.garden,
            "swiming_pool": self.swiming_pool,
            "price": self.price,
            "year_built": self.year_built,
            "status": self.status,
            "features": self.features,
            "saved": self.saved,
        }

    def save_listing(self):
        self.saved = True
        self.save()
        return f"Property at {self.address} has been saved as a favorite."

class CommunicationManager(Communication):
    notifications = models.JSONField(default=list)
    inbox = models.JSONField(default=list)

    def send_message(self, recipient, message):
        self.message.append({"recipient": recipient, "message": message})
        self.save()
        return f"Message sent to {recipient}"

    def receive_message(self, sender, message):
        self.inbox.append({"sender": sender, "message": message})
        self.save()
        return f"Message received from {sender}"

    def notify_user(self, notification):
        self.notifications.append(notification)
        self.save()
        return "User has been notified."

class NotificationManager(Notification):
    user_preferences = models.JSONField(default=dict)

    def update_preferences(self, preferences):
        self.user_preferences.update(preferences)
        self.save()
        return "User preferences updated."

    def track_event(self, event):
        return f"Tracking event: {event}"

class MobileUserAccount(User):
    ssologin = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        # Ensure the password is hashed before saving
        if self.password and not self.password.startswith('pbkdf2_'):
            self.password = make_password(self.password)
        super(MobileUserAccount, self).save(*args, **kwargs)

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

    def register(self, username, email, password):
        """
        Registers a new user account.
        :param username: The username for the new account
        :param email: The email for the new account
        :param password: The password for the new account
        :return: Success or failure message
        """
        if User.objects.filter(username=username).exists():
            return "Username already taken"

        if User.objects.filter(email=email).exists():
            return "Email already registered"

        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            return "User registered successfully"
        except ValidationError as e:
            return f"Registration failed: {e}"

    def update_profile(self, user, profile_data):
        """
        Updates the user's profile information.
        :param user: The user object
        :param profile_data: A dictionary containing profile fields to update
        :return: Success or failure message
        """
        try:
            if 'username' in profile_data:
                if User.objects.filter(username=profile_data['username']).exclude(id=user.id).exists():
                    return "Username already taken"
                User.username = profile_data['username']

            if 'email' in profile_data:
                if User.objects.filter(email=profile_data['email']).exclude(id=user.id).exists():
                    return "Email already registered"
                User.email = profile_data['email']

            if 'password' in profile_data:
                user.set_password(profile_data['password'])

            user.save()
            return "Profile updated successfully"
        except Exception as e:
            return f"Profile update failed: {e}"
