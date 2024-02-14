from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save,pre_save
from django.utils import timezone

from destination.models import Destination
from django.db.models.signals import post_delete
from django.dispatch import receiver
# Create your models here.




class User(AbstractUser):
    is_organisor=models.BooleanField(default=False)
    is_agent=models.BooleanField(default=True)
    destination_assign = models.ForeignKey(
        Destination,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        default=None  # Set your default value here, or another valid instance of Destination
    )
    agent_full_name = models.CharField(max_length=60, blank=True, null=True)

    def __str__(self):
        return f"{self.username}"
class UserProfile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    def __str__(self):
        return self.user.username
    
class Lead(models.Model):

    first_name=models.CharField(max_length=20)
    last_name=models.CharField(max_length=20)
    age=models.IntegerField(default=0)
    agent=models.ForeignKey("Agent",null=True, blank=True, on_delete=models.SET_NULL)
    category=models.ForeignKey("Category", related_name="leads", null =True, blank=True,default=2, on_delete=models.SET_NULL)
    destination=models.CharField(max_length=20,null=True)
    date_added=models.DateTimeField(auto_now_add=True)
    phone_number=models.CharField(max_length=10)
    email=models.EmailField()
    profile_picture=models.ImageField(null=True, blank=True,upload_to="profile_pictures/")
    converted_date = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
def handle_upload_follow_ups(instance,filename):
    return f"lead_followups/lead_{instance.lead.pk}/{filename}"



class Agent(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    organisation=models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    full_name=models.CharField(max_length=30,null=True)
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
        # return f"{self.user.first_name} {self.user.last_name}"
    
    def save(self, *args, **kwargs):
        # Set the constant value before saving
        self.full_name = f"{self.user.first_name} {self.user.last_name}"
        super().save(*args, **kwargs)

class Category(models.Model):
    name=models.CharField(max_length=30)
    organisation=models.ForeignKey(UserProfile,on_delete=models.CASCADE)

    def __str__(self):
        return self.name



def post_user_create_signal(sender,instance,created,**kwargs):
    # instance -instance of model that triggered the signal, User
    # created - either new instance created (True) or updated (False only
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(post_user_create_signal,sender=User)

@receiver(post_delete, sender=Agent)
def delete_user(sender, instance, **kwargs):
    if instance.user:
        instance.user.delete()


