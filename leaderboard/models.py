from django.db import models


class Player(models.Model):
    name = models.TextField(null=False, blank=False, unique=True)
    joined = models.DateField(null=False)

    def __str__(self):
        return self.name


class LeaderboardEntry(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)

    timestamp = models.DateTimeField()

    rank = models.IntegerField()
    elo = models.IntegerField()
    gold = models.IntegerField()
    silver = models.IntegerField()
    bronze = models.IntegerField()
    ratedgames = models.IntegerField()
    totalgames = models.IntegerField()
    finished = models.IntegerField()
    eliminated = models.IntegerField()
    resigned = models.IntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['player', 'timestamp'], name='single player at time'),
            models.UniqueConstraint(fields=['rank', 'timestamp'], name='single rank at time'),
        ]

    def __str__(self):
        return f"{self.rank}. {self.player.name} on {self.timestamp}"
