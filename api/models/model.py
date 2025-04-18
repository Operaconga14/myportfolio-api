# Admin
# Projects (Featured and Personal)
# Tech Stack
# Services

from enum import Enum
from datetime import datetime
from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator


class ProjectStatus(str, Enum):
    DRAFT = "draft"           # Initial stage, not yet started
    PUBLISHED = "published"   # Project is live or visible to stakeholders
    ARCHIVED = "archived"     # Project is no longer active or relevant
    DONE = "done"             # Project is completed successfully
    ONGOING = "ongoing"       # Project is currently in progress
    ON_HOLD = "on_hold"       # Project is paused or waiting for resources
    CANCELLED = "cancelled"   # Project has been stopped and will not continue
    IN_REVIEW = "in_review"   # Project is under review or approval process
    PLANNING = "planning"     # Project is in the planning phase
    TESTING = "testing"       # Project is in the testing or QA phase
    DELAYED = "delayed"       # Project is behind schedule
    PENDING = "pending"       # Project is awaiting further action or decision


class Admin(models.Model):
    id = fields.IntField(pk=True)
    first_name = fields.CharField(max_length=255, null=True, default=None)
    last_name = fields.CharField(max_length=255, null=True, default=None)
    email = fields.CharField(max_length=255, unique=True)
    username = fields.CharField(max_length=255, null=True, default=None)
    picture = fields.CharField(max_length=500, null=True, default="")
    password = fields.CharField(max_length=255)
    social_url = fields.JSONField(null=True, default=[])
    contact = fields.CharField(max_length=255, null=True, default="")
    location = fields.CharField(max_length=255, null=True, default="")
    created_at = fields.DatetimeField(
        auto_now_add=False, null=True, default=None)
    updated_at = fields.DatetimeField(auto_now=False, null=True, default=None)

    class Meta:
        table = "admin"

    def full_name(self) -> str:
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.username


User_Pydantic = pydantic_model_creator(
    Admin, name="Admin", exclude=["password"]
)
USerIn_Pydantic = pydantic_model_creator(
    Admin, name="AdminIn", exclude_readonly=True
)


class PersonalProjects(models.Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255)
    image = fields.CharField(max_length=500, null=True, default="")
    description = fields.CharField(max_length=255)
    urls = fields.JSONField(null=True, default=[])
    tech_stack = fields.JSONField(null=True, default=[])
    status = fields.CharEnumField(
        enum_type=ProjectStatus, default=ProjectStatus.DRAFT)
    is_completed = fields.BooleanField(default=False)
    created_at = fields.DatetimeField(
        auto_now_add=False, null=True, default=None)
    update_at = fields.DatetimeField(
        auto_now_add=False, null=True, default=None)
    posted_by = fields.ForeignKeyField(
        "models.Admin", related_name="personalproject")

    class Meta:
        table = "personalprojects"


class FeaturedProjects(models.Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255)
    image = fields.CharField(max_length=500, null=True, default="")
    description = fields.CharField(max_length=255)
    urls = fields.JSONField(null=True, default=[])
    tech_stack = fields.JSONField(null=True, default=[])
    status = fields.CharEnumField(
        enum_type=ProjectStatus, default=ProjectStatus.DRAFT)
    is_completed = fields.BooleanField(default=False)
    created_at = fields.DatetimeField(
        auto_now_add=False, null=True, default=None)
    update_at = fields.DatetimeField(
        auto_now_add=False, null=True, default=None)
    posted_by = fields.ForeignKeyField(
        "models.Admin", related_name="featureproject")

    class Meta:
        table = "featuredprojects"


class TechStack(models.Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255)
    image = fields.CharField(max_length=500, null=True, default="")
    posted_by = fields.ForeignKeyField(
        "models.Admin", related_name="techstack")

    class Meta:
        table = "techstacks"


class Services(models.Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255)
    description = fields.CharField(max_length=255, null=True)
    image = fields.CharField(max_length=500, null=True, default="")
    posted_by = fields.ForeignKeyField("models.Admin", related_name="services")

    class Meta:
        table = "services"
