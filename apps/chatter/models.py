from django.db import models
from django.utils import timezone
from django.conf import settings

class Room(models.Model):
    name = models.CharField(max_length=80)

    def __str__(self):
        return self.name

class Message(models.Model):
    text = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True, blank=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING
    )

    room = models.ForeignKey(
        Room,
        on_delete=models.DO_NOTHING
    )

    def was_published_recently(self):
        return timezone.now() - datetime.timedelta(days=1) <= self.timstamp <= timezone.now()

    def last_50_messages(self, room_id):
        return Message.objects.order_by('-timestamp').all().filter(room_id=room_id)[:50]
    
    def __str__(self):
        """Return the model as a string"""
        return str(self.timestamp) + " - " + self.text