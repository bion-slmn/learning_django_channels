from django.db.models.signals import post_save
from .models import Message
from django.dispatch import receiver
import queue


message_queue = queue.Queue()

@receiver(post_save, sender=Message)
def message_created(sender, instance, created, **kwargs):
    print(1111111111222222222)
    if created:
        message_queue.put(instance)