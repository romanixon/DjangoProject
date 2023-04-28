from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from celery import shared_task
import datetime

from .models import *
from newsportal import settings


@shared_task
def send_week_notification():
    today = datetime.datetime.now()
    last_week = today - datetime.timedelta(days=7)
    posts = Post.objects.filter(post_in__gte=last_week)
    categories = set(posts.values_list('category__name_category', flat=True))
    subscribers = set(
        Category.objects.filter(name_category__in=categories).values_list('subscribers__email', flat=True))
    html_content = render_to_string(
        'news/daily_post.html',
        {
            'link': settings.SITE_URL,
            'posts': posts,
        }
    )
    msg = EmailMultiAlternatives(
        subject='Статьи за неделю',
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        bcc=subscribers
    )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()


@shared_task
def send_notifications(preview, pk, post_header, subscribers):
    html_content = render_to_string(
        'news/post_created_email.html',
        {
            'text': preview,
            'link': f'{settings.SITE_URL}/news/{pk}'
        }
    )

    msg = EmailMultiAlternatives(
        subject=post_header,
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers,
    )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()
