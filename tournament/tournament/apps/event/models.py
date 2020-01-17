from django.db import models

# Create your models here.
class Event(models.Model):
    code = models.CharField(max_length=10)

    def __str__(self):
        return f"Event {self.code}"
