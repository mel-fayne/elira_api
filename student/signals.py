
from django.utils.crypto import get_random_string
from django.db.models.signals import pre_save
from django.dispatch import receiver

from student.models import Student

@receiver(pre_save, sender=Student)
def set_resetKey(sender, instance, **kwargs):
   unique_id = get_random_string(length=6, allowed_chars='0123456789')
   instance.reset_key = unique_id
   print(unique_id)