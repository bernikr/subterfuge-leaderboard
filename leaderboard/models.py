from django.db import models


class SourceFile(models.Model):
    filename = models.CharField(max_length=255, null=False, blank=False, unique=True)

    def __str__(self):
        return self.filename


class Player(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    joined = models.DateField(null=False)

    def __str__(self):
        return self.name

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name', 'joined'], name='no duplicates'),
        ]


class LeaderboardEntry(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    source_file = models.ForeignKey(SourceFile, null=True, on_delete=models.SET_NULL)

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
