from django.db import models
from django.utils import timezone
from core.models import Document, Notification

class SigningDocument(Document):
    signer_list = models.JSONField()
    status = models.CharField(max_length=50, choices=[('pending', 'Pending'), ('signed', 'Signed'), ('completed', 'Completed')], default='pending')
    
    def prepare_for_signature(self, signer_list):
      self.signer_list.set(signer_list)
      self.status = 'pending'
      self.save()
      return self

    def track_status(self):
        all_signed = all(signer.signature for signer in self.signer_list.all())
        self.status = 'completed' if all_signed else 'pending'
        self.save()
        return self.status

    def download_document(self):
        # Download the document
        return f"Downloading document: {self.title}"

class Signer(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    signature = models.TextField(null=True, blank=True)  # Electronic signature provided by the signer.
    document = models.ForeignKey(SigningDocument, on_delete=models.CASCADE)
    signed_at = models.DateTimeField(null=True, blank=True)
    
    def review_document(self, document):
        document = SigningDocument.objects.get(id=document)
        return f"Reviewing document: {document.title}"

    def sign_document(self, document_id):
        self.signature = "Signed with e-signature"
        self.signed_at = timezone.now()
        self.save()
        return f"Document {document_id} signed by {self.name}"

    def get_signature_status(self, document):
        document = SigningDocument.objects.get(id=document)
        status = "Signed" if self.signature else "Pending"
        return f"Signature status for {self.name}: {status}"

class SigningNotification(Notification):
    signer = models.ForeignKey(Signer, on_delete=models.CASCADE)
    document = models.ForeignKey(SigningDocument, on_delete=models.CASCADE)
    type = models.CharField(max_length=50, choices=[('signature', 'Signature'), ('request', 'Request'), ('reminder', 'Reminder')], default='signature')
    delivery_method = models.CharField(max_length=50, choices=[('email', 'Email'), ('sms', 'SMS')], default='email')

    def update_status(self):
        # Update the status of the notification
        return f"Notification {self.notification_id} status updated to delivered."

    def view_notification_history(self, signer_id):
        notifications = SigningNotification.objects.filter(signer=signer_id)
        return [notification.notification_id for notification in notifications]

class Compliance(models.Model):
    id = models.AutoField(primary_key=True)
    document = models.ForeignKey(SigningDocument, on_delete=models.CASCADE)
    regulation = models.CharField(max_length=100)
    compliance_status = models.CharField(max_length=50, choices=[('compliant', 'Compliant'), ('non_compliant', 'Non-compliant')], default='Non-compliant')
    last_checked = models.DateTimeField()

    def check_compliance(self, document_id):
        self.compliance_status = 'compliant'
        self.save()
        return f"Document {document_id} compliance status: {self.compliance_status}"

    def update_compliance_status(self, document_id):
        self.compliance_status = 'compliant'
        self.save()
        return f"Compliance status for document {document_id} updated to compliant."

    def get_compliance_records(self, document_id):
        records = Compliance.objects.filter(document=document_id)
        return [record.id for record in records]

class SignatureTracker(models.Model):
    id = models.AutoField(primary_key=True)
    document = models.ForeignKey(SigningDocument, on_delete=models.CASCADE)
    signer = models.ForeignKey(Signer, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, choices=[('pending', 'Pending'), ('signed', 'Signed'), ('overdue', 'Overdue')])
    reminder_sent = models.BooleanField(default=False)

    def track_signature_status(self, document_id, signer_id):
        signer = Signer.objects.get(id=signer_id, document=document_id)
        self.status = 'signed' if signer.signature else 'pending'
        self.save()
        return self.status

    def send_reminder(self, document_id, signer_id):
        self.reminder_sent = True
        self.save()
        return f"Reminder sent to signer {signer_id} for document {document_id}"

    def get_tracking_report(self, document_id):
        trackers = SignatureTracker.objects.filter(document=document_id)
        return [(tracker.signer.name, tracker.status) for tracker in trackers]