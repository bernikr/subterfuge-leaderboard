from django.contrib import admin

from leaderboard.models import Player, LeaderboardEntry, Leaderboard

admin.site.register(Player)
admin.site.register(Leaderboard)
admin.site.register(LeaderboardEntry)
