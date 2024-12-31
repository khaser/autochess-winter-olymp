from django.apps import AppConfig

from ejudge.database import EjudgeDatabase

from django.conf import settings

class UsersConfig(AppConfig):
    name = 'users'

    def ready(self):
        from .models import UserInfo
        from django.contrib.auth.models import User
        from battles import models as battles_models

        def create_user(login):
            db = EjudgeDatabase()
            user_data = db.get_user_by_login(login)
            if not user_data:
                raise Exception("Requested team not found in ejudge")
            ejudge_user_id = int(user_data['user_id'])

            user = User.objects.create_user(login, first_name=login)
            userInfo = UserInfo.objects.create(user=user, ejudge_user_id=ejudge_user_id)
            placement = battles_models.Placement.objects.create(user=userInfo)

            return userInfo

        # User.objects.filter(is_superuser=False).all().delete()
        # for team_login in settings.REGISTRED_TEAMS:
        #     create_user(team_login)

