from django.db import models
from profiles.models import Profile
# Create your models here.

class Log(models.Model):
    profile=models.ForeignKey(Profile,on_delete=models.CASCADE,null=True,blank=True)
    photo=models.ImageField(upload_to='logs')
    is_correct=models.BooleanField(default=False)
    created=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Log of{self.profile.id}"