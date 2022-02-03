from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.shortcuts import redirect
from django.template.loader import render_to_string

from .models import Post, Category


@receiver(post_save, sender=Post)
def send_mail_for_subscribers(sender, instance, created, **kwargs):

    sub_text = instance.post_text
    category = Category.objects.get(pk=Post.objects.get(pk=instance.pk).categories.pk)

    subscribers = category.subscribers.all()

    post = instance

    for subscriber in subscribers:

        html_content = render_to_string(
            'mail.html', {'user': subscriber, 'text': sub_text[:50], 'post': post})

        msg = EmailMultiAlternatives(
            subject=f'Здравствуй, {subscriber.username}. Новая статья в вашем любимом разделе!',
            from_email='serha@yandex.ru',
            to=[subscriber.email]
        )

        msg.attach_alternative(html_content, 'text/html')

        msg.send()

    return redirect('/')
