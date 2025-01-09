from django.shortcuts import render, redirect
from .models import Card, Player, Game
from .forms import PlayerForm
import random

def deck_generator():
    """Funkcja generuje talie kart"""
    Card.objects.all().delete()

    colors = ['pik', 'kier', 'karo', 'walet']
    markings = ['walet', 'dama', 'krol', 'as']

    for color in colors:
        for number in range(2,11):
            Card.objects.create(color = color, number = number)
        for marking in markings:
            Card.objects.create(color = color, marking = marking)

def get_dec(request):
    cards = Card.objects.all()

def home(request):
    """Strona startowa"""
    form = PlayerForm()
    if request.method == "POST":
        form = PlayerForm(request.POST)
        if form.is_valid():
            nick = form.cleaned_data['nick']
            request.session['nick'] = nick
            return redirect('rules')
    return render(request, 'home.html', {'form': form})

def rules(request):
    """Strona z zasadami"""
    if request.method == "POST":
        selected_rules = request.POST.getlist('rules')
        custom_settings = request.POST.get('custom_settings', None)
        request.session['selected_rules'] = selected_rules
        request.session['custom_settings'] = custom_settings
        return redirect('game')
    return render(request, 'rules.html')

def game(request):
    """Strona z grą"""
    if not Card.objects.exists():
        deck_generator()

    cards = list(Card.objects.all())
    random.shuffle(cards)

    player_nick = request.session.get('nick', 'Gracz')
    player, created = Player.objects.get_or_create(nick=player_nick)

    game, created = Game.objects.get_or_create(player=player)

    if created:
        player_cards = cards[:5]
        computer_cards = cards[5:10]

        game.deck.set(cards[10:])
        game.player_hand.set(player_cards)
        game.computer_hand.set(computer_cards)

        game.last_played_card = None
        game.save()

    
