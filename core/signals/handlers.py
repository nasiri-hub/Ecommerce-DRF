from django.dispatch import receiver
from store.signals import order_created, order_updated


@receiver(order_created)
def new_order_created(sender, **kwargs):
    print(kwargs['order'])


@receiver(order_updated)
def update_an_order(sender, **kwargs):
    print(kwargs['updated'])
