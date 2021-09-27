from django.contrib import admin

from leaderboard.models import Player, LeaderboardEntry

admin.site.register(Player)
admin.site.register(LeaderboardEntry)
