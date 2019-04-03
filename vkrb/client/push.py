from celery import Task
from django.conf import settings

from vkrb.client.fcm import NotificationFirebaseMethod
from vkrb.client.tasks import send_notification
from vkrb.core.models import DeviceType, PushToken
from vkrb.user.models import StatusType


class NotificationPayload:
    def __init__(self, *,
                 title=None,
                 body=None,
                 icon=None,
                 sound='default',
                 badge=None,
                 tag=None,
                 color=None,
                 click_action=None,
                 body_loc_key=None,
                 body_loc_args=None,
                 title_loc_key=None,
                 title_loc_args=None,
                 **kwargs):
        self.title = title
        self.body = body
        self.icon = icon
        self.sound = sound
        self.badge = badge
        self.tag = tag
        self.color = color
        self.click_action = click_action
        self.body_loc_key = body_loc_key
        self.body_loc_args = body_loc_args
        self.title_loc_key = title_loc_key
        self.title_loc_args = title_loc_args
        self.kwargs = kwargs

    def to_dict(self):
        d = {}
        for k, v in self.__dict__.items():
            if k != 'kwargs':
                if v is not None:
                    d[k] = v
        d.update(self.kwargs)
        return d

    @staticmethod
    def from_dict(d):
        if d is None:
            return None
        return NotificationPayload(**d)


class BasePush():
    API_KEY = settings.CLOUDMESSAGING_KEY
    ACTION = None

    @staticmethod
    def parse_os_type_tokens(tokens):
        ios_devices = []
        android_devices = []

        for token in tokens:
            if token.device_type == DeviceType.IOS:
                ios_devices.append(token.token)
            else:
                android_devices.append(token.token)

        return ios_devices, android_devices

    def get_tokens(self):
        raise NotImplemented

    def get_notification(self) -> NotificationPayload:
        pass

    def get_data(self):
        return {}

    def _wrap_data(self, data, notification):
        return {
            'action': self.ACTION,
            'data': data,
            'notification': notification
        }

    def send(self, async=True):
        notification = self.get_notification()
        notification_dict = notification.to_dict()
        data = self._wrap_data(self.get_data(), notification_dict)

        ios_recipients, android_recipients = self.parse_os_type_tokens(
            self.get_tokens()
        )

        self.execute(android_recipients, data=data, async=async)
        self.execute(ios_recipients, data=data,
                     notification=notification_dict, async=async)

    def execute(self, recipients, data=None, notification=None, async=True):
        if not recipients:
            return

        request = {'key': self.API_KEY}
        if data:
            request['data'] = data

        if notification:
            request['notification'] = notification

        if len(recipients) == 1:
            request['to'] = recipients[0]
        else:
            request['registration_ids'] = recipients

        if async:
            send_notification.apply_async(args=[request, ])
        else:
            NotificationFirebaseMethod(**request).execute()


class NewNewsItemPush(BasePush):
    ACTION = 'new_newsitem'

    def __init__(self, newsitem):
        self.newsitem = newsitem
        if newsitem.category:
            self.title = f'Новая новость в категории "{newsitem.category}"'
        else:
            self.title = f'Новая новость'
        self.body = f'{newsitem.title}'

    def get_tokens(self):
        return PushToken.objects.filter(user__is_active=True)

    def get_notification(self):

        return NotificationPayload(
            title=self.title,
            body=self.body
        )

    def get_data(self):

        return {
            'id': self.newsitem.id
        }


class NewUserChangedItemPush(BasePush):
    ACTION = 'profile_updated'

    def __init__(self, user_changed):
        self.user_changed = user_changed
        if user_changed.status == StatusType.APPROVED:
            self.body = f'Изменения профиля приняты'
        elif user_changed.status == StatusType.REJECTED:
            self.body = f'Изменения профиля отклонены'


    def get_tokens(self):
        return PushToken.objects.filter(user=self.user_changed.user)

    def get_notification(self):
        return NotificationPayload(
            body=self.body
        )



class NewRecourseAnswerPush(BasePush):
    ACTION = 'new_recourseanswer'

    def __init__(self, recourse):
        self.recourse = recourse
        self.title = f'На ваше обращение ответил эксперт "{recourse.subject}"'
        self.body = f'{recourse.answer}'

    def get_tokens(self):
        return PushToken.objects.filter(user=self.recourse.user)

    def get_notification(self):
        return NotificationPayload(
            title=self.title,
            body=self.body
        )

    def get_data(self):
        return {
            'id': self.recourse.id,
            'parent_id': self.recourse.parent_id
        }
