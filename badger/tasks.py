from datetime import datetime

from celery import shared_task
from django.contrib.auth.models import User
from badger.models import Badge
from datetime import datetime, timedelta


@shared_task
def check_users_seniority_task(self):
    users = User.objects.all()
    pionneer_badge = Badge.objects.get_or_create(name='Pionneer',
                                                 description='Pour vos 1 an sur le site, vous recevez un badge Pionneer',
                                                 image='pionneer.png')
    for user in users:
        if is_one_year_old(user):
            user.badges.add(pionneer_badge)
            user.save()


def is_one_year_old(user):
    return datetime.now() - user.date_joined > timedelta(days=365)
