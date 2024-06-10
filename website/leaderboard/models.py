from itertools import chain

from django.db import models


class Leaderboard(models.Model):
    filename = models.CharField(max_length=255, null=False, blank=False, unique=True)
    timestamp = models.DateTimeField()

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
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='entries')
    leaderboard = models.ForeignKey(Leaderboard, on_delete=models.CASCADE, related_name='entries')

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

    @property
    def timestamp(self):
        return self.leaderboard.timestamp

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['player', 'leaderboard'], name='no duplicate players per leaderboard'),
            models.UniqueConstraint(fields=['rank', 'leaderboard'], name='no duplicate ranks per leaderboard'),
        ]

    def __str__(self):
        return f"{self.rank}. {self.player.name} on {self.timestamp}"


def to_dict(instance):
    opts = instance._meta
    data = {}
    for f in chain(opts.concrete_fields, opts.private_fields):
        data[f.name] = f.value_from_object(instance)
    for f in opts.many_to_many:
        data[f.name] = [i.id for i in f.value_from_object(instance)]
    return data