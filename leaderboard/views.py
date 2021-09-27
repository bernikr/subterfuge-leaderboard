from django.db.models import Max, Q
from django.forms import model_to_dict
from django.http import HttpResponseNotFound, Http404
from django.shortcuts import render

from leaderboard.models import LeaderboardEntry, Player

PAGE_SIZE = 100


def index(request, page=1):
    entries = get_current_leaderboard(1 + (page - 1) * PAGE_SIZE, PAGE_SIZE)

    max_rank = LeaderboardEntry.objects.aggregate(Max('rank'))['rank__max']
    last_page = int((max_rank - 1) / 100) + 1

    pagination = [
                     ("First", "/1", "disabled " if page == 1 else ""),
                     ("Previous", f"/{page - 1}", ("disabled " if page == 1 else "") + "d-none d-sm-table-cell"),
                 ] + [(str(p), f"/{p}",
                       ("active " if p == page else "") + ("d-none d-sm-table-cell" if p < page - 2 or p > page + 2 else ""))
                      for p in range(max(1, page - 3), min(last_page, page + 3) + 1)] + [
                     ("Next", f"/{page + 1}", ("disabled " if page == last_page else "") + "d-none d-sm-table-cell"),
                     ("Last", f"/{last_page}", "disabled" if page == last_page else ""),
                 ]

    update_time = LeaderboardEntry.objects.aggregate(Max('timestamp'))['timestamp__max']
    return render(request, "index.html", {
        "update_time": update_time,
        "leaderboard_entries": entries,
        "pagination": pagination,
    })


def get_current_leaderboard(rank_from, num=100):
    group_dict = LeaderboardEntry.objects.filter(rank__gte=rank_from, rank__lt=rank_from + num) \
        .values('rank').annotate(newest=Max('timestamp'))

    params = Q()
    for obj in group_dict:
        params |= (Q(rank=obj['rank']) & Q(timestamp=obj['newest']))

    return LeaderboardEntry.objects.filter(params)


def player(request, name, id=None):
    if id is None:
        res = Player.objects.filter(name=name)
        if res.count() > 1:
            #TODO User selection
            return HttpResponseNotFound("Multiple Players with this name")
        else:
            player = res.first()
    else:
        player = Player.objects.get(id=id, name=name)

    if player is None:
        raise Http404()

    current_stats = player.leaderboardentry_set.latest("timestamp")

    return render(request, "player.html", {
        "player": player,
        "current_stats": model_to_dict(current_stats),
        "leaderboard_entries": get_current_leaderboard(current_stats.rank-3, 7),
        "stats": list(player.leaderboardentry_set.order_by("timestamp").values()),
    })
