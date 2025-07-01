import uuid
from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.conf import settings

from django.contrib.auth.models import BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_admin", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    class Department(models.TextChoices):
        FINANCE = "finance"
        MARKETING = "marketing"
        VISUAL_CREATION = "visual_creation"
        TECHNICAL_TEAM = "technical_team"
        ER = "er"
        HR = "hr"

    username = models.CharField(max_length=150, unique=True, null=True, blank=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    phone_number = models.CharField(max_length=10, blank=True)
    is_admin = models.BooleanField(default=False)
    is_board = models.BooleanField(default=False)
    department = models.CharField(
        max_length=20, choices=Department.choices, default=Department.FINANCE
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = CustomUserManager()

    groups = models.ManyToManyField(
        Group,
        related_name="clubuser_set",
        blank=True,
        help_text="The groups this user belongs to.",
        verbose_name="groups",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="clubuser_set",
        blank=True,
        help_text="Specific permissions for this user.",
        verbose_name="user permissions",
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name} -> ({self.department})"


class Task(models.Model):
    class Status(models.TextChoices):
        TODO = "ToDo", "To Do"
        IN_PROGRESS = "InProgress", "In Progress"
        DONE = "Done", "Done"
        EVALUATED = "Evaluated", "Evaluated"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.TODO
    )
    due_date = models.DateTimeField()
    priority = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(3)]
    )
    creator = models.ForeignKey(
        User, related_name="created_tasks", on_delete=models.CASCADE
    )
    assigned_to = models.ForeignKey(
        User,
        related_name="assigned_tasks",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    department = models.CharField(
        default="finance", max_length=20, choices=User.Department.choices
    )

    def __str__(self):
        return f"{self.title} [{self.status}]"


class Event(models.Model):
    class EventType(models.TextChoices):
        MEETING = "meeting", "Meeting"
        WORKSHOP = "workshop", "Workshop"
        PARTY = "party", "Party"
        COMPETITION = "competition", "Competition"
        OTHER = "other", "Other"

    class Status(models.TextChoices):
        UPCOMING = "upcoming", "Upcoming"
        ONGOING = "ongoing", "Ongoing"
        COMPLETED = "completed", "Completed"
        CANCELED = "canceled", "Canceled"

    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    event_type = models.CharField(max_length=20, choices=EventType.choices, default=EventType.MEETING)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    location = models.CharField(max_length=255)
    department = models.CharField(max_length=20, choices=User.Department.choices, null=True, blank=True)
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='events')
    is_mandatory = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.UPCOMING)
    event_photo = models.ImageField(upload_to='event_photos/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.start_time.strftime('%Y-%m-%d %H:%M')})"

class File(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='files/')
    uploaded_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='uploaded_files'
    )
    department = models.CharField(
        max_length=50,
        choices=[(tag.name, tag.value) for tag in User.Department]
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)

    file_type = models.CharField(max_length=50, blank=True)
    description = models.TextField(blank=True)
    is_public = models.BooleanField(default=False)
    last_accessed = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} uploaded by {self.uploaded_by}"
    

class Poll(models.Model):
    question = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    allowed_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='allowed_polls')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question

class Choice(models.Model):
    poll = models.ForeignKey(Poll, related_name='choices', on_delete=models.CASCADE)
    text = models.CharField(max_length=255)

    def __str__(self):
        return self.text

class Vote(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name="votes")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE, related_name="votes")
    voted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('poll', 'user')