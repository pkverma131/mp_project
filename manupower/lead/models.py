from django.db import models
from django.contrib.auth.models import AbstractUser


class Industry(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    GRANUAL_TYPES = [
        ('LDPE', 'Low-Density Polyethylene'),
        ('HDPE', 'High-Density Polyethylene'),
    ]

    industry = models.ForeignKey(Industry, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=100)
    granual_type = models.CharField(max_length=4, choices=GRANUAL_TYPES, default='LDPE')
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Lead(models.Model):
    company_name = models.CharField(max_length=100)
    industry = models.ForeignKey(Industry, on_delete=models.CASCADE, related_name='leads')
    website = models.URLField(max_length=200, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(max_length=254, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.company_name

class LeadMeta(models.Model):
    lead = models.OneToOneField(Lead, on_delete=models.CASCADE, related_name='meta')
    additional_info = models.TextField(blank=True, null=True)
    # Add other fields as needed

class LeadCatalogue(models.Model):
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name='catalogue')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='catalogues')

    def __str__(self):
        return f"{self.lead.company_name} - {self.product.name}"

class ContactPerson(models.Model):
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name='contacts')
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100, unique=True)
    phone = models.CharField(max_length=20)
    position = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class User(AbstractUser):
    role = models.CharField(max_length=50, blank=True, null=True)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='lead_users',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        verbose_name='groups'
    )
    
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='lead_users_permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions'
    )

class Activity(models.Model):
    CALL = 'call'
    EMAIL = 'email'
    MEETING = 'meeting'
    FOLLOW_UP = 'follow_up'
    DEMO = 'demo'
    SITE_VISIT = 'site_visit'
    WEBINAR = 'webinar'
    DOCUMENT_SENT = 'document_sent'
    PROPOSAL = 'proposal'
    CONTRACT = 'contract'
    SOCIAL_MEDIA = 'social_media'
    LEAD_NURTURING = 'lead_nurturing'
    REMINDER = 'reminder'
    SURVEY = 'survey'
    TRAINING_SESSION = 'training_session'

    ACTIVITY_TYPES = [
        (CALL, 'Call'),
        (EMAIL, 'Email'),
        (MEETING, 'Meeting'),
        (FOLLOW_UP, 'Follow-Up'),
        (DEMO, 'Demo'),
        (SITE_VISIT, 'Site Visit'),
        (WEBINAR, 'Webinar'),
        (DOCUMENT_SENT, 'Document Sent'),
        (PROPOSAL, 'Proposal'),
        (CONTRACT, 'Contract'),
        (SOCIAL_MEDIA, 'Social Media Interaction'),
        (LEAD_NURTURING, 'Lead Nurturing'),
        (REMINDER, 'Reminder'),
        (SURVEY, 'Survey'),
        (TRAINING_SESSION, 'Training Session'),
    ]

    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name='activities')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities')
    activity_type = models.CharField(max_length=50, choices=ACTIVITY_TYPES)
    description = models.TextField(blank=True, null=True)
    scheduled_at = models.DateTimeField(blank=True, null=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.activity_type} - {self.lead.company_name}"

class Email(models.Model):
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name='emails')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='emails')
    subject = models.CharField(max_length=255)
    body = models.TextField()
    status = models.CharField(max_length=50)  # e.g., sent, failed
    sent_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject

class Call(models.Model):
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name='calls')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='calls')
    phone_number = models.CharField(max_length=20)
    call_time = models.DateTimeField()
    duration = models.IntegerField()  # duration in seconds
    outcome = models.CharField(max_length=100)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Call to {self.phone_number} at {self.call_time}"

class Task(models.Model):
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name='tasks')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    due_date = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=50)  # e.g., pending, completed
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Note(models.Model):
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name='notes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notes')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Note by {self.user.username} on {self.created_at}"
