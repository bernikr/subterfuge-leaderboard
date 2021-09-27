from django.db import models


class Player(models.Model):
    name = models.TextField(null=False, blank=False, unique=True)
    joined = models.DateField(null=False)


class LeaderboardEntry(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)

    timestamp = models.DateTimeField()

    elo = models.IntegerField()
    gold = models.IntegerField()
    silver = models.IntegerField()
    bronze = models.IntegerField()
    ratedgames = models.IntegerField()
    totalgames = models.IntegerField()
    finished = models.IntegerField()
    eliminated = models.IntegerField()
    resigned = models.IntegerField()
