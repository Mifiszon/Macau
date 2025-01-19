from django.shortcuts import render, redirect
from .models import Card, Player, Game
from .forms import PlayerForm
from .rules_logic.rules import Rules
import random

def deck_generator():
    """Funkcja generuje talie kart"""
    Card.objects.all().delete()

    colors = ['pik', 'kier', 'karo', 'trefl']
    markings = ['walet', 'dama', 'krol', 'as']

    for color in colors:
        for marking in markings:
            image_path = f"cards/{marking}_{color}.png"
            Card.objects.create(color=color,number=None, marking=marking, image=image_path)

    for color in colors:
        for number in range(2, 11):
            image_path = f"cards/{number}_{color}.png"
            Card.objects.create(color=color,marking=None, number=number, image=image_path)
    

def home(request):
    """Strona startowa"""
    Player.objects.all().delete()
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
        request.session['selected_rules'] = selected_rules
        return redirect('game')
    return render(request, 'rules.html')

def show_cards(request):
        """Widok do wyświetlania wszystkich kart w grze"""
        cards = Card.objects.all()
        return render(request, 'show_cards.html', {'cards': cards})

def game(request):
    """Strona z grą"""
    #if not Card.objects.exists():
    #    deck_generator()
    
    deck_generator()

    cards = list(Card.objects.all())
    random.shuffle(cards)

    player_nick = request.session.get('nick', 'Gracz')
    player, created = Player.objects.get_or_create(nick=player_nick)

    game, created = Game.objects.get_or_create(player=player)

    player_cards = []  
    computer_cards = []
    discard_pile = []
    deck = []

    if created:
        # Rozdanie kart dla gracza i komputera
        player_cards = cards[:5]
        computer_cards = cards[5:10]

        # Pierwsza karta do stosu odrzuconych
        discard_pile = [cards[10]]
        deck = cards[11:]

        # Ustawienie kart w grze
        game.discard_pile.set(discard_pile)
        game.player_hand.set(player_cards)
        game.computer_hand.set(computer_cards)
        game.deck.set(deck)

        game.save()

    selected_rules = request.session.get('selected_rules', [])
    rules = Rules(rules=selected_rules)
    
    result = rules.apply_rules(cards, player_cards, discard_pile)

    if result == "Win":
        return render(request, 'game/win.html', {'player': player})
    elif result == "Lose":
        return render(request, 'game/lose.html', {'player': player})

    return render(request, 'game.html', {
        'game': game,
        'player_cards': player_cards,
        'computer_cards': computer_cards,
        'deck': deck,
        'discard_pile': discard_pile[0] if discard_pile else None,  # Sprawdzamy, czy lista jest pusta
    })

