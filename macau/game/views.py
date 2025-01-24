from django.shortcuts import render, redirect
from .models import Card, Player, Game
from .forms import PlayerForm
from .rules_logic.rules import Rules
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
    
def computer_turn(game):
    """
    Ruch kompa
    """
    computer_hand = list(game.computer_hand.all())
    top_card = game.discard_pile.first()

    ##print(f"Top card: {top_card.image}")
    
    for card in computer_hand:
        if can_play(card, top_card):
            game.computer_hand.remove(card)
            ##print(f"Before: {[c.image for c in game.discard_pile.all()]}")
            game.discard_pile.add(card)
            ##print(f"After: {[c.image for c in game.discard_pile.all()]}")
            game.discard_pile.set([card])
            ##print(f"zoo: {[c.image for c in game.discard_pile.all()]}")
            game.save()
            ##print(f"Computer played: {card.image}")
            return

    if game.deck.exists():
        next_card = game.deck.first()
        game.computer_hand.add(next_card)
        game.deck.remove(next_card)
        game.save()
        ##print(f"Computer drew: {next_card.image}")

def can_play(card, top_card):
    """
    Czy karte mozna zagrac
    """
    ##print(f"Top Card: {top_card}, played Card: {card}")
    ##print(f"Comparing: Card color: {card.color}, top color: {top_card.color}")
    ##print(f"Comparing: Card number: {card.number}, top number: {top_card.number}")

    if card.number and top_card.number:
        if card.number == top_card.number:
            return True
    
    if card.marking and top_card.marking:
        if card.marking == top_card.marking:
            return True
    
    if card.color == top_card.color:
        return True
    
    return False
    

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
    Strona z zasadami
    """
    if request.method == "POST":
        selected_rules = request.POST.getlist('rules')
        request.session['selected_rules'] = selected_rules
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
    Widok gry
    """
    if not Card.objects.exists():
        deck_generator()

    player_nick = request.session.get('nick', 'Gracz')
    player, created = Player.objects.get_or_create(nick=player_nick)

    game, created = Game.objects.get_or_create(player=player)

    if created:
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

    if request.method == "POST":
        if "play_card" in request.POST:
            card_id = request.POST.get("card_id")
            card = Card.objects.get(id=card_id)
            if card in game.player_hand.all():
                top_card = game.discard_pile.first()
                if can_play(card, top_card):
                    game.player_hand.remove(card)
                    ##print(f"Before: {[c.image for c in game.discard_pile.all()]}")
                    game.discard_pile.add(card)
                    ##print(f"After: {[c.image for c in game.discard_pile.all()]}")
                    game.discard_pile.set([card])
                    ##print(f"zoo: {[c.image for c in game.discard_pile.all()]}")
                    game.save()
                    ##print(f"Zagrano kartę: {card.image}, Discard Pile: {[c.image for c in game.discard_pile.all()]}")
                else:
                    return render(request, 'game.html', {
                        'game': game,
                        'top_card': game.discard_pile.first(),
                        'error': 'Nie możesz zagrać tej karty',
                    })

        elif "draw_card" in request.POST:
            if game.deck.exists():
                next_card = game.deck.first()
                game.player_hand.add(next_card)
                game.deck.remove(next_card)
                game.save()

        computer_turn(game)

    game.refresh_from_db()

    if game.player_hand.count() == 0:
        return render(request, 'win.html', {'game': game})
    elif game.computer_hand.count() == 0:
        return render(request, 'lose.html', {'game': game})

    return render(request, 'game.html', {
        'game': game,
        'top_card': game.discard_pile.first(),
        'error': None,
    })



