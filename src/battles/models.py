from django.db import models

from django.utils.translation import gettext_lazy as _

from users import models as user_models

# Create your models here.

import battles.core

class Fighter(models.Model):

    class FighterKind(models.TextChoices):
        ARCHER = 'ARC', _('Archer')
        BERSERKER = 'BER', _('Berserker')
        CAVALRY = 'CAV', _('Cavalry')
        COMMANDER = 'COM', _('Commander')
        KNIGHT = 'KN', _('Knight')
        INFANTRYMAN = 'INF', _('Infantryman')

    kind = models.CharField(
        choices=FighterKind.choices,
        max_length = 3,
    )

    ejudge_short_name = models.CharField(db_index=True, max_length=255)


class PositionedFigher(models.Model):
    fighter = models.OneToOneField(Fighter, on_delete=models.CASCADE)
    row = models.PositiveIntegerField()
    column = models.PositiveIntegerField()
    user = models.ForeignKey(user_models.UserInfo, on_delete=models.CASCADE)

class Battle(models.Model):
    red_team = models.OneToOneField(user_models.UserInfo, on_delete=models.CASCADE, related_name = "battles_as_red")
    blue_team = models.OneToOneField(user_models.UserInfo, on_delete=models.CASCADE, related_name = "battles_as_blue")

    class BattleResult(models.TextChoices):
        RED = 'R', _('Blue')
        BLUE = 'B', _('Red')

    result = models.CharField(
        choices=BattleResult.choices,
        max_length = 1,
    )
