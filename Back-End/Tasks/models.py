from django.db import models
from Accounts.models import CustomUser

class Task(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.TextField()
    create_time = models.DateField(auto_now_add=True)
    active = models.BooleanField(default=True)


    def __str__(self):
        return self.title
