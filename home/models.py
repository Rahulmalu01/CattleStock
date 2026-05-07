from django.db import models

class TeamMember(models.Model):
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=150)
    image = models.ImageField(upload_to='team/')

    def __str__(self):
        return self.name
    
class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name