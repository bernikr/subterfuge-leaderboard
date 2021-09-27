from django.contrib import admin
from django.urls import path

from leaderboard import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.index, name='leaderboard'),
    path('<int:page>', views.index, name='leaderboard_page'),

    path('player/<str:name>', views.player, name='player'),
    path('player/<str:name>/<int:id>', views.player, name='player_by_id'),
]
