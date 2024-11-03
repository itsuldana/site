from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import Post

@receiver(post_delete, sender=Post)
def delete_news_tags(sender, instance, **kwargs):
    # Очищаем связи новости и тегов
    instance.tags.clear()