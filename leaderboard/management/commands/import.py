import os
import re
from datetime import datetime

import lxml.html as lh
from django.core.management import BaseCommand
from django.db import transaction
from tqdm import tqdm

from leaderboard.models import Player, LeaderboardEntry, SourceFile

filename_pattern = re.compile(r"^leaderboard_\d{8}_\d{6}[^.]*.html$")
updated_pattern = re.compile(r"^Leaderboard updated on \w*, ([^.]*).$")


class Command(BaseCommand):
    help = 'Import Leaderborad fles'

    def add_arguments(self, parser):
        parser.add_argument('path', type=str)

    def handle(self, *args, **options):
        import_files(options['path'])


def import_files(path):
    already_imported_files = {a[0] for a in SourceFile.objects.values_list('filename')}
    files = [f for f in os.listdir(path) if filename_pattern.match(f) and f not in already_imported_files]
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
    filename = os.path.basename(file)
    sourcefile, new = SourceFile.objects.get_or_create(filename=filename)
    if not new:
        print(f"File '{filename}' was already imported, skipping")
        return
    sourcefile.save()

    page = lh.parse(file)

    time = next(p.groups()[0] for p in
                (updated_pattern.match(p) for p in
                 (p.text_content() for p in page.xpath("//p"))
                 ) if p is not None)
    time = datetime.strptime(time, '%d %b %y %H:%M:%S %z')

    rows = page.xpath("//table/tr")
    for row in tqdm(rows[1:]):
        r = [c.text_content() for c in row.xpath("./td")]

        playername = r[1]
        joined_date = datetime.strptime(r[11], "%d %b %Y").date()

        player, new = Player.objects.get_or_create(name=playername, joined=joined_date)
        if new:
            player.save()

        new_entry = LeaderboardEntry(
            player=player,
            source_file=sourcefile,
            timestamp=time,
            rank=str_to_int(r[0]),
            elo=str_to_int(r[2]),
            gold=str_to_int(r[3]),
            silver=str_to_int(r[4]),
            bronze=str_to_int(r[5]),
            ratedgames=str_to_int(r[6]),
            totalgames=str_to_int(r[7]),
            finished=str_to_int(r[8]),
            eliminated=str_to_int(r[9]),
            resigned=str_to_int(r[10])
        )

        try:
            prev_entry = player.leaderboardentry_set.filter(timestamp__lt=new_entry.timestamp).latest('timestamp')
            if prev_entry.totalgames != new_entry.totalgames or prev_entry.rank != new_entry.rank:
                new_entry.save()
        except LeaderboardEntry.DoesNotExist:
            new_entry.save()
