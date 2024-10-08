from django.db.models import Max
from django.forms import model_to_dict
from django.http import HttpResponseNotFound, JsonResponse
from django.shortcuts import render

from leaderboard.models import Player, Leaderboard

PAGE_SIZE = 100


def index(request, page=1):
    current_leaderboard = Leaderboard.objects.latest('timestamp')
    max_rank = current_leaderboard.entries.aggregate(Max('rank'))['rank__max']
    last_page = int((max_rank - 1) / 100) + 1

    pagination = [
                     ("First", "/1", "disabled " if page == 1 else ""),
                     ("Previous", f"/{page - 1}", ("disabled " if page == 1 else "") + "d-none d-sm-table-cell"),
                 ] + [(str(p), f"/{p}",
                       ("active " if p == page else "") + (
                           "d-none d-sm-table-cell" if p < page - 2 or p > page + 2 else ""))
                      for p in range(max(1, page - 3), min(last_page, page + 3) + 1)] + [
                     ("Next", f"/{page + 1}", ("disabled " if page == last_page else "") + "d-none d-sm-table-cell"),
                     ("Last", f"/{last_page}", "disabled" if page == last_page else ""),
                 ]

    rank_from = 1 + (page - 1) * PAGE_SIZE
    entries = current_leaderboard.entries.filter(rank__gte=rank_from, rank__lt=rank_from + PAGE_SIZE).order_by("rank")
    update_time = current_leaderboard.timestamp
    return render(request, "index.html", {
        "update_time": update_time,
        "leaderboard_entries": entries,
        "pagination": pagination,
    })


def player(request, name, id=None):
    if id is None:
        res = Player.objects.filter(name=name)
        if res.count() > 1:
            # TODO User selection
            return HttpResponseNotFound("Multiple Players with this name")
        else:
            player = res.first()
    else:
        player = Player.objects.get(id=id, name=name)

    if player is None:
        return render(request, "search_results.html", {
            "results": Player.objects.filter(name__icontains=name).order_by('name'),
            "name": name,
        })

    current_leaderboard = Leaderboard.objects.latest('timestamp')
    current_stats = current_leaderboard.entries.get(player=player)

    leaderboard_around = current_leaderboard.entries \
        .filter(rank__gte=current_stats.rank - 3, rank__lt=current_stats.rank + 4).order_by("rank")
    return render(request, "player.html", {
        "player": player,
        "current_stats": model_to_dict(current_stats),
        "leaderboard_entries": leaderboard_around,
        "stats": [{"timestamp": e.timestamp, "elo": e.elo, "rank": e.rank}
                  for e in player.entries.all()]
    })


def about(request):
    return render(request, "about.html")


def api_search_player(request, search):
    res = Player.objects.filter(name__icontains=search).values_list('name')[:100]
    res = [i[0] for i in res]
    return JsonResponse({"res": res})
