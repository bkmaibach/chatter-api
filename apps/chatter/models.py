from django.db import models
from django.utils import timezone
from django.conf import settings

class Room(models.Model):
    name = models.CharField(max_length=80)
    password = models.CharField(max_length=255, blank=True, default='')

    def __str__(self):
        return self.name

class Entry(models.Model):
    text = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE
    )

    def was_published_recently(self):
        return timezone.now() - datetime.timedelta(days=1) <= self.timstamp <= timezone.now()

    def last_50_entries(room_id):
        return Entry.objects.order_by('-timestamp').all().filter(room_id=room_id)[:50]
    
    def __str__(self):
        """Return the model as a string"""
        return str(self.timestamp) + " - " + self.text