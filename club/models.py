import uuid
from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import AbstractUser, Group, Permission


# Create your models here.
class User(AbstractUser):
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

    class Department(models.TextChoices):
        FINANCE = "finance"
        MARKETING = "marketing"
        VISUAL_CREATION = "visual_creation"
        TECHNICAL_TEAM = "technical_team"
        ER = "er"
        HR = "hr"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
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
    assignee = models.ForeignKey(
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
