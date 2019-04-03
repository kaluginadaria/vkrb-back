from celery import shared_task

from vkrb.client.fcm import NotificationFirebaseMethod


@shared_task
def send_notification(request):
    NotificationFirebaseMethod(**request).execute()
