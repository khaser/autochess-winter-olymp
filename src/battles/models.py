from django.db import models

from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from users import models as user_models

# Create your models here.

class Fighter(models.Model):

    class FighterKind(models.TextChoices):
        ARCHER = 'archer', _('archer')
        BERSERKER = 'berserker', _('berserker')
        CAVALRY = 'cavalry', _('cavalry')
        COMMANDER = 'commander', _('commander')
        KNIGHT = 'knight', _('knight')
        INFANTRYMAN = 'infantryman', _('infantryman')

    kind = models.CharField(
        choices=FighterKind.choices,
        max_length = 16,
    )

    ejudge_short_name = models.CharField(db_index=True, max_length=255)


class Placement(models.Model):
    user = models.ForeignKey(user_models.UserInfo, on_delete=models.CASCADE)

class PositionedFigher(models.Model):
    fighter = models.ForeignKey(Fighter, on_delete=models.CASCADE)
    row = models.PositiveIntegerField()
    column = models.PositiveIntegerField()
    placement = models.ForeignKey(Placement, on_delete=models.CASCADE)

    def map_fighter(self):
        return {
            'x': self.column,
            'y': self.row,
            'fighter_kind': self.fighter.kind,
        }


def get_user_fighters(user):
    return user.get_cur_placement().positionedfigher_set.all()

class BattleResult(models.TextChoices):
    RED = 'red', _('red')
    BLUE = 'blue', _('blue')

class Battle(models.Model):

    red_placement = models.OneToOneField(Placement, on_delete=models.CASCADE, related_name = "battles_as_red")
    blue_placement = models.OneToOneField(Placement, on_delete=models.CASCADE, related_name = "battles_as_blue")

    result = models.CharField(
        choices=BattleResult.choices,
        max_length=16,
        blank=True,
    )

    time = models.DateTimeField(default=timezone.now)

    def red_username(self):
        return self.red_placement.user.get_login()

    def blue_username(self):
        return self.blue_placement.user.get_login()

    def winner_username(self):
        return self.blue_username() if self.result == 'blue' else self.red_username()
