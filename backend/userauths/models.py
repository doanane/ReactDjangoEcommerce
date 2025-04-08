from datetime import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser
from shortuuid.django_fields import ShortUUIDField
from django.db.models.signals import post_save
from django.utils import timezone


# Create your models here.
class User(AbstractUser):
    username = models.CharField(unique=True, max_length=100)
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(null=True, blank=True, max_length=100)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email
    
    def save(self, *args, **kwargs):
        # Only process email if it exists and contains @
        if self.email and "@" in self.email:
            email_username = self.email.split("@")[0]  # Just get the part before @
            
            if not self.full_name:
                self.full_name = email_username
            
            if not self.username:
                self.username = email_username
        
        super().save(*args, **kwargs)


class Profile(models. Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.FileField(upload_to= "image", default="default/default-user.jpg", null=True, blank= True)
    full_name = models.CharField(unique=True, max_length=100, null=True, blank=True)
    about = models.TextField(null=True, blank=True)
    gender = models.CharField( max_length=100, null=True, blank=True)
    country = models.CharField( max_length=100, null=True, blank=True)
    state = models.CharField( max_length=100, null=True, blank=True)
    address = models.CharField( max_length=100, null=True, blank=True)
    date = models.DateTimeField(auto_created=True)
    pid = ShortUUIDField(unique=True,length= 10, max_length=20, alphabet="abcdefghijklmnopqrstuvwxyz")

    def __str__(self):
        if self.full_name:
            return str(self.full_name)
        else:
            return str(self.user.full_name)



    def save(self, *args, **kwargs):
        if self.full_name == "" or self.full_name == None:
            self.full_name = self.user.full_name
  
        super(Profile, self).save(*args, **kwargs)


        # making use of signals

def create_user_profile(sender,instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance, date=timezone.now())

def save_user_profile(sender,instance, **kwargs):
     if hasattr(instance, 'profile'):
         instance.profile.save()

post_save.connect(create_user_profile, sender = User)
post_save.connect(save_user_profile, sender = User)

# explanation of code
# i made the sender the user model, so whenever the user model is created a prfile is also automatically saved, and when the user model is saved the profile is saved for them, it takes arguments(sender, instance, created, **kwargs) the post_save.connect the create_user and save_user function to the post signal for that particular model we are saving. the create_user is always called whenever a new user is called





