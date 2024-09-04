import csv
import os
import re
from datetime import datetime
from pathlib import Path

import lxml.html as lh
import pytz
import requests
from tqdm import tqdm

filename_pattern = re.compile(r"^leaderboard_\d{8}_\d{6}[^.]*.(html|1\.csv)$")
updated_pattern = re.compile(r"^Leaderboard updated on \w*, ([^.]*).$")


def main():
    path = Path(__file__).parent / "../archive"
    # already_imported_files = {a[0] for a in Leaderboard.objects.values_list('filename')}
    # files = [f for f in os.listdir(path) if filename_pattern.match(f) and f not in already_imported_files]
    files = [f for f in path.glob("*") if filename_pattern.match(f.name)]
    files.sort()
    num = len(files)
    for i, f in enumerate(files):
        print(f"parse file {i + 1}/{num}: {f.name}")
        import_file(f)


def str_to_int(s):
    if s == "-":
        return 0
    elif s.endswith('%'):
        return int(s[:-1])
    else:
        return int(s)


def import_file(file):
    ext = filename_pattern.match(file.name).group(1)

    res = {
        'html': import_html,
        '1.csv': import_csv_1,
    }.get(ext)(file)

    requests.post("http://localhost:5173/api/import", json=res)


def import_html(file):
    filename = os.path.basename(file)

    page = lh.parse(file)

    time = next(p.groups()[0] for p in
                (updated_pattern.match(p) for p in
                 (p.text_content() for p in page.xpath("//p"))
                 ) if p is not None)
    res = {
        "timestamp": datetime.strptime(time, '%d %b %y %H:%M:%S %z').isoformat(),
        "entries": [],
    }

    rows = page.xpath("//table/tr")
    for row in tqdm(rows[1:]):
        r = [c.text_content() for c in row.xpath("./td")]
        res["entries"].append(save_leaderboard_row(r))

    return res


def import_csv_1(file):
    filename = os.path.basename(file)

    with open(file) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        leaderboard = None
        for i, r in tqdm(enumerate(csv_reader)):
            if i == 0:
                continue
            elif i == 1:
                time = datetime.strptime(f"{r[12]} {r[13]}", '%d %b %Y %H:%M').replace(tzinfo=pytz.UTC)
                leaderboard = Leaderboard(filename=filename, timestamp=time)
                leaderboard.save()
            save_leaderboard_row(r, leaderboard)


def save_leaderboard_row(r):
    return {
        "player": {
            "name": r[1],
            "joined": datetime.strptime(r[11], "%d %b %Y").date().isoformat(),
        },
        "rank": str_to_int(r[0]),
        "elo": str_to_int(r[2]),
        "gold": str_to_int(r[3]),
        "silver": str_to_int(r[4]),
        "bronze": str_to_int(r[5]),
        "rated_games": str_to_int(r[6]),
        "total_games": str_to_int(r[7]),
        "finished": str_to_int(r[8]),
        "eliminated": str_to_int(r[9]),
        "resigned": str_to_int(r[10]),
    }


if __name__ == '__main__':
    main()
