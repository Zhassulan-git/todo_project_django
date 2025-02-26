from django.db import models
from users.models import CustomUser

class Project(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)


class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=12, default='assigned')
    #assigned, in progress done
    priority = models.CharField(max_length=12)
    #high, medium, low
    expiration_date = models.DateTimeField(blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')


# class Role(models.Model):
#     user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
#     project