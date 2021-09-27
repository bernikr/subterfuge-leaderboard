from django.contrib import admin

from leaderboard.models import Player, LeaderboardEntry, SourceFile

admin.site.register(SourceFile)
admin.site.register(Player)
admin.site.register(LeaderboardEntry)
