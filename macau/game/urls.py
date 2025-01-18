from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("rules/", views.rules, name='rules'),
    path("game/", views.game, name='game'),
    path('show_cards/', views.show_cards, name='show_cards'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
