import os
import re
from datetime import datetime

import lxml.html as lh
from django.core.management import BaseCommand
from django.db import transaction

from leaderboard.models import Player, LeaderboardEntry

filename_pattern = re.compile(r"^leaderboard_\d{8}_\d{6}[^.]*.html$")
updated_pattern = re.compile(r"^Leaderboard updated on \w*, ([^.]*).$")


class Command(BaseCommand):
    help = 'Import Leaderborad fles'

    def handle(self, *args, **options):
        import_files(r"\\homecloud.lan\docker\subterfuge-leaderboards")


def import_files(path):
    files = [f for f in os.listdir(path) if filename_pattern.match(f)]
    files.sort()
    num = len(files)
    for i, f in enumerate(files):
        print(f"parse file {i + 1}/{num}: {f}")
        import_file(os.path.join(path, f))


def str_to_int(s):
    if s == "-":
        return 0
    elif s.endswith('%'):
        return int(s[:-1])
    else:
        return int(s)


@transaction.atomic
def import_file(file):
    page = lh.parse(file)

    time = next(p.groups()[0] for p in
                (updated_pattern.match(p) for p in
                 (p.text_content() for p in page.xpath("//p"))
                 ) if p is not None)
    time = datetime.strptime(time, '%d %b %y %H:%M:%S %z')

    rows = page.xpath("//table/tr")
    for row in rows[1:]:
        r = [c.text_content() for c in row.xpath("./td")]

        playername = r[1]
        joined_date = datetime.strptime(r[11], "%d %b %Y").date()

        player, new = Player.objects.get_or_create(name=playername, joined=joined_date)
        if new:
            player.save()

        LeaderboardEntry(
            player=player,
            timestamp=time,
            elo=str_to_int(r[2]),
            gold=str_to_int(r[3]),
            silver=str_to_int(r[4]),
            bronze=str_to_int(r[5]),
            ratedgames=str_to_int(r[6]),
            totalgames=str_to_int(r[7]),
            finished=str_to_int(r[8]),
            eliminated=str_to_int(r[9]),
            resigned=str_to_int(r[10])
        ).save()