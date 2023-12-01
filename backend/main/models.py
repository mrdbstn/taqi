from django.db import models
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

# Create your models here.

class Family(models.Model):
    id = models.AutoField(primary_key=True)
    family_name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"{self.family_name}"

class Team(models.Model):
    id = models.AutoField(primary_key=True)
    team_name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"{self.team_name}"
    

class User(models.Model):
    id = models.AutoField(primary_key=True)
    profile_id = models.CharField(max_length=100, null=True, blank=False, unique=True)
    first_name = models.CharField(max_length=100, blank=False)
    last_name = models.CharField(max_length=100, blank=False)
    email_address = models.CharField(max_length=320, blank=False)
    parent_email_address = models.CharField(max_length=320, blank=False, unique=True)

    family = models.ForeignKey(Family, related_name="family_members", on_delete=models.CASCADE, null=True, blank=True)
    team = models.ForeignKey(Team, related_name="team_members", on_delete=models.CASCADE, null=True, blank=True)

    def clean(self):
        if self.first_name == "":
            raise ValidationError("First name cannot be empty.")
        
        if self.last_name == "":
            raise ValidationError("Last name cannot be empty.")
        
        if self.profile_id == "":
            raise ValidationError("Profile ID cannot be empty.")
        
        if self.email_address == "":
            raise ValidationError("Email address cannot be empty.")

        self.email_address = self.email_address.lower()
        self.parent_email_address = self.parent_email_address.lower()
        validate_email(self.email_address)
        validate_email(self.parent_email_address)

        if self.email_address == self.parent_email_address:
            raise ValidationError("Parent email address cannot be the same as the user email address.")
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
                    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    

