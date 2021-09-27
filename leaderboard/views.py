from django.db.models import Max, Q
from django.shortcuts import render

from leaderboard.models import LeaderboardEntry

PAGE_SIZE = 100


def index(request, page=1):
    entries = get_current_leaderboard(1 + (page - 1) * PAGE_SIZE, PAGE_SIZE)

    last_page = int((get_number_of_entries() - 1) / 100) + 1

    pagination = [
                     ("First", 1, "disabled" if page == 1 else ""),
                     ("Previous", page - 1, "disabled" if page == 1 else ""),
                 ] + [(str(p), p, "active" if p == page else "") for p in
                      range(max(1, page - 3), min(last_page, page + 3) + 1)] + [
                     ("Next", page + 1, "disabled" if page == last_page else ""),
                     ("Last", last_page, "disabled" if page == last_page else ""),
                 ]
    print(pagination)
    return render(request, "index.html", {
        "entries": entries,
        "pagination": pagination,
    })


def get_current_leaderboard(rank_from, num=100):
    group_dict = LeaderboardEntry.objects.filter(rank__gte=rank_from, rank__lt=rank_from + num) \
        .values('rank').annotate(newest=Max('timestamp'))

    params = Q()
    for obj in group_dict:
        params |= (Q(rank=obj['rank']) & Q(timestamp=obj['newest']))

    return LeaderboardEntry.objects.filter(params)


def get_number_of_entries():
    return LeaderboardEntry.objects.aggregate(Max('rank'))['rank__max']
