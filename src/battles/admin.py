from django.contrib import admin

from . import models

class FighterAdmin(admin.ModelAdmin):
    list_display = ('ejudge_short_name', 'kind')

class PositionedFigherAdmin(admin.ModelAdmin):
    list_display = ('fighter', 'row', 'column', 'placement')

class PlacementAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user')

class BattleAdmin(admin.ModelAdmin):
    list_display = ('red_placement', 'blue_placement')

admin.site.register(models.Fighter, FighterAdmin)
admin.site.register(models.PositionedFigher, PositionedFigherAdmin)
admin.site.register(models.Battle, BattleAdmin)
admin.site.register(models.Placement, PlacementAdmin)
