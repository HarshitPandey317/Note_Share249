from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password

class Group(models.Model):
    name = models.CharField(max_length=200)
    password = models.CharField(max_length=200)  # Hashed password
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owned_groups")
    members = models.ManyToManyField(User, related_name="note_groups", blank=True)

    def __str__(self):
        return self.name

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

class Subgroup(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='subgroups')
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Note(models.Model):
    subgroup = models.ForeignKey(Subgroup, on_delete=models.CASCADE, related_name='notes')
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='uploads/')
    uploader = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title  # Fixed from .name to .title