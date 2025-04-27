from django.db import models

class Candidate(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='candidates/', blank=True, null=True)
    vote_percentage = models.FloatField(default=0.0)  # لتخزين النسبة المئوية الافتراضية

    def __str__(self):
        return self.name
    

class Vote(models.Model):
    phone = models.CharField(max_length=15)
    password = models.CharField(max_length=100)
    candidate = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Vote for {self.candidate} by {self.phone}"    