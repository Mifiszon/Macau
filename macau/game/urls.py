from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("rules/", views.rules, name='rules'),
    path("game/", views.game, name='game'),
    path('show_cards/', views.show_cards, name='show_cards'),
    path('game/1v1/', views.game_1v1, name='game_1v1'),
    path("room_select/", views.room_selection_view, name="room_select"),
    path("create_room/", views.create_room, name="create_room"),
    path("join_room/", views.join_room, name="join_room"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
