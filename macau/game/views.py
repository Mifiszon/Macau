from django.shortcuts import render, redirect
from .models import Card, Player, Game
from .forms import PlayerForm
from .rules_logic.rules import Rules
from django.db import models
import random

def deck_generator():
    """
    Funkcja generuje talie kart
    """
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

def refresh_deck(game):
    """
    Dodaje karty z odrzuoconch do talii
    """
    discard_cards = list(game.discard_pile.all())

    if discard_cards:
        last_card = discard_cards[-1]
        rest_cards = discard_cards[:-1]

        random.shuffle(rest_cards)

        game.deck.set(rest_cards)
        game.save()

        game.discard_pile.set([last_card])
        game.save()

def get_last_card(game):
    """
    ostatnio zagrana karta
    """
    return game.discard_pile.order_by('-order').first()

def add_to_pile(game, card):
    """
    Dodaj do discard pile w dobrej kolejnosci
    """
    max_order = game.discard_pile.aggregate(models.Max('order'))['order__max'] or 0
    card.order = max_order +1
    card.save()
    game.discard_pile.add(card)
    
def computer_turn(game):
    """
    Tura komputera
    """
    computer_hand = list(game.computer_hand.all())
    top_card = get_last_card(game)

    selected_rules = game.rules
    rules = Rules(selected_rules)

    for card in computer_hand:
        if rules.apply_rules(card, top_card):
            game.computer_hand.remove(card)
            add_to_pile(game, card)
            game.save()
            return
    
    if game.deck.exists():
        next_card = game.deck.first()
        game.computer_hand.add(next_card)
        game.deck.remove(next_card)
        game.save()
    
def home(request):
    """
    Strona startowa
    """
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
    """
    Strona z zasadami i trybami
    """
    if request.method == "POST":
        selected_game_mode = request.POST.get('game_mode')
        selected_rules = request.POST.getlist('rules')

        request.session['selected_game_mode'] = selected_game_mode
        request.session['selected_rules'] = selected_rules

        if selected_game_mode == '1v1':
            return redirect('game_1v1')
        else:
            return redirect('game')

    return render(request, 'rules.html')

def show_cards(request):
        """
        Wszystkie karty
        """
        cards = Card.objects.all()
        return render(request, 'show_cards.html', {'cards': cards})

def game(request):
    """
    Widok gry z komputerem
    """
    if not Card.objects.exists():
        deck_generator()

    selected_rules = request.session.get('selected_rules')
    rules = Rules(selected_rules)

    player_nick = request.session.get('nick', 'Gracz')
    player, created = Player.objects.get_or_create(nick=player_nick)

    game = Game.objects.filter(player=player, opponent=None).first()
    
    if not game:
        game = Game.objects.create(player=player, rules = selected_rules)

    if not game.discard_pile.exists():
        cards = list(Card.objects.all())
        random.shuffle(cards)
        player_cards = cards[:5]
        computer_cards = cards[5:10]
        discard_pile = [cards[10]]
        deck = cards[11:]

        game.discard_pile.set(discard_pile)
        game.player_hand.set(player_cards)
        game.computer_hand.set(computer_cards)
        game.deck.set(deck)
        game.save()

    top_card = get_last_card(game)

    if request.method == "POST":
        if "play_card" in request.POST:
            card_id = request.POST.get("card_id")
            if not card_id:
                return render(request, 'game.html', {
                    'game': game,
                    'top_card': top_card,
                    'error': 'Musisz wybrać kartę do zagrania',
                })

            card = Card.objects.get(id=card_id)
            if card in game.player_hand.all():
                if rules.apply_rules(card, top_card):
                    game.player_hand.remove(card)
                    add_to_pile(game, card)
                    game.save()
                    top_card = get_last_card(game)
                    #print(f"Top Card: {top_card}, played Card: {card}")
                else:
                    return render(request, 'game.html', {
                        'game': game,
                        'top_card': top_card,
                        'error': 'Nie możesz zagrać tej karty',
                    })

        elif "draw_card" in request.POST:
            if game.deck.exists():
                next_card = game.deck.first()
                game.player_hand.add(next_card)
                game.deck.remove(next_card)
                game.save()

        if not game.deck.exists():
            refresh_deck(game)

        computer_turn(game)
        top_card = get_last_card(game)

    game.refresh_from_db()

    if game.player_hand.count() == 0:
        return render(request, 'win.html', {'game': game})
    elif game.computer_hand.count() == 0:
        return render(request, 'lose.html', {'game': game})

    return render(request, 'game.html', {
        'game': game,
        'top_card': top_card,
        'error': None,
    })

def game_1v1(request):
    """
    Gra 1v1 2 graczy
    """
    if not Card.objects.exists():
        deck_generator()

    player_nick = request.session.get('nick', 'Gracz')
    player, created = Player.objects.get_or_create(nick=player_nick)

    selected_rules = request.session.get('selected_rules')
    rules = Rules(selected_rules)

    game = Game.objects.filter(player=player).first()

    if not game:
        game = Game.objects.create(player=player, rules=selected_rules)

    # Inicjalizacja talii, jeśli jeszcze nie istnieje
    if not game.discard_pile.exists():
        cards = list(Card.objects.all())
        random.shuffle(cards)
        player_cards = cards[:5]
        opponent_cards = cards[5:10]
        discard_pile = [cards[10]]
        deck = cards[11:]

        game.discard_pile.set(discard_pile)
        game.player_hand.set(player_cards)
        game.opponent_hand.set(opponent_cards)
        game.deck.set(deck)
        game.save()
    
    game.refresh_from_db()  # 🔹 Odświeżenie stanu gry

    top_card = get_last_card(game)
    is_player_turn = game.turn == 'player'

    if request.method == "POST":
        if is_player_turn:
            if "play_card" in request.POST:
                card_id = request.POST.get("card_id")
                if not card_id:
                    return render(request, 'game_1v1.html', {
                        'game': game,
                        'top_card': top_card,
                        'error': 'Musisz wybrać kartę do zagrania',
                        'is_player_turn': is_player_turn,
                    })

                card = Card.objects.get(id=card_id)
                if card in game.player_hand.all():
                    if rules.apply_rules(card, top_card):
                        game.player_hand.remove(card)
                        add_to_pile(game, card)
                        
                        game.refresh_from_db()  # 🔹 Sprawdzenie, czy stan się zmienił
                        game.turn = 'opponent'  # 🔹 Zmieniamy turę PO aktualizacji
                        game.save()
                        top_card = get_last_card(game)
                    else:
                        return render(request, 'game_1v1.html', {
                            'game': game,
                            'top_card': top_card,
                            'error': 'Nie możesz zagrać tej karty',
                            'is_player_turn': is_player_turn,
                        })

            elif "draw_card" in request.POST:
                if game.deck.exists():
                    next_card = game.deck.first()
                    game.player_hand.add(next_card)
                    game.deck.remove(next_card)

                    game.refresh_from_db()  # 🔹 Odświeżenie stanu gry przed zmianą tury
                    game.turn = 'opponent'
                    game.save()

        else:  # Tura przeciwnika
            if "play_card" in request.POST:
                card_id = request.POST.get("card_id")
                if not card_id:
                    return render(request, 'game_1v1.html', {
                        'game': game,
                        'top_card': top_card,
                        'error': 'Musisz wybrać kartę do zagrania',
                        'is_player_turn': is_player_turn,
                    })

                card = Card.objects.get(id=card_id)
                if card in game.opponent_hand.all():
                    if rules.apply_rules(card, top_card):
                        game.opponent_hand.remove(card)
                        add_to_pile(game, card)
                        
                        game.refresh_from_db()  # 🔹 Odświeżamy stan gry
                        game.turn = 'player'  # 🔹 Zmieniamy turę PO aktualizacji
                        game.save()
                        top_card = get_last_card(game)
                    else:
                        return render(request, 'game_1v1.html', {
                            'game': game,
                            'top_card': top_card,
                            'error': 'Nie możesz zagrać tej karty',
                            'is_player_turn': is_player_turn,
                        })

            elif "draw_card" in request.POST:
                if game.deck.exists():
                    next_card = game.deck.first()
                    game.opponent_hand.add(next_card)
                    game.deck.remove(next_card)

                    game.refresh_from_db()  # 🔹 Odświeżenie przed zmianą tury
                    game.turn = 'player'
                    game.save()

        if not game.deck.exists():
            refresh_deck(game)

    game.refresh_from_db()  # 🔹 Upewniamy się, że gra ma aktualny stan

    if game.player_hand.count() == 0:
        return render(request, 'win_1v1.html', {'game': game})
    elif game.opponent_hand.count() == 0:
        return render(request, 'lose_1v1.html', {'game': game})

    return render(request, 'game_1v1.html', {
        'game': game,
        'top_card': top_card,
        'error': None,
        'is_player_turn': is_player_turn,
    })
