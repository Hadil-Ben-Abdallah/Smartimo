from django.db import models
from datetime import datetime
from maintenance_and_service_requests.models import MaintenanceRequest
from core.models import TimeStampedModel


class MaintenanceRequestMedia(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    request = models.ForeignKey(MaintenanceRequest, on_delete=models.CASCADE)
    file_path = models.CharField(max_length=255, blank=True, null=True)
    media_type = models.CharField(max_length=50, blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    annotations = models.TextField(blank=True, null=True)

    def add_media(self, request, file_path, media_type, annotations=None):
        self.request = request
        self.file_path = file_path
        self.media_type = media_type
        self.annotations = annotations
        self.uploaded_at = datetime.now()
        self.save()

    def annotate_media(self, annotations):
        self.annotations = annotations
        self.save()

    def get_media(self):
        return {
            "media_id": self.id,
            "file_path": self.file_path,
            "media_type": self.media_type,
            "uploaded_at": self.uploaded_at,
            "annotations": self.annotations
        }

