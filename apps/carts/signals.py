from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Cart
from django.core.cache import cache


@receiver([post_save, post_delete], sender=Cart)
def cart_cache(sender, instance, **kwargs):
    cache.delete_pattern(f"*carts:{instance.id}*")
