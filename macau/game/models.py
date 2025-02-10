from django.db import models
import random

class Card(models.Model):
    COLORS = [('pik', 'Pik'), ('kier', 'Kier'), ('karo', 'Karo'), ('trefl', 'Trefl')]
    MARKINGS = [('walet', 'Walet'), ('dama', 'Dama'), ('krol', 'Król'), ('as', 'As')]

    color = models.CharField(max_length=10, choices=COLORS)
    number = models.IntegerField(null=True, blank=True)
    marking = models.CharField(max_length=10, choices=MARKINGS, null=True, blank=True)
    function = models.CharField(max_length=100, null=True, blank=True)
    image = models.ImageField(upload_to="cards/", null=True)
    order = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.marking if self.marking else self.number} {self.color}"

class Player(models.Model):
    nick = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.nick

class Room(models.Model):
    code = models.CharField(max_length=10, unique=True)
    players = models.ManyToManyField(Player, related_name="rooms")
    max_players = models.IntegerField(default=4)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Room {self.code}"

class Game(models.Model):
    room = models.OneToOneField(Room, on_delete=models.CASCADE, related_name="game")
    players = models.ManyToManyField(Player, related_name="games")
    deck = models.ManyToManyField(Card, related_name="deck")
    discard_pile = models.ManyToManyField(Card, related_name='discard_pile')
    hands = models.JSONField(default=dict)  # Przechowuje karty w rękach graczy
    turn_order = models.JSONField(default=list)  # Kolejność tur graczy
    current_turn = models.IntegerField(default=0)  # Indeks gracza, który ma turę
    turn_action_done = models.BooleanField(default=False)

    def __str__(self):
        return f"Game in {self.room.code}"
    
    def next_turn(self):
        self.current_turn = (self.current_turn + 1) % len(self.turn_order)
        self.turn_action_done = False
        self.save()
    
    def start_game(self):
        """Rozpoczyna grę, tasuje karty i rozdaje po 5 dla każdego gracza."""
        cards = list(Card.objects.all())
        random.shuffle(cards)
        
        self.deck.set(cards[10:])
        self.discard_pile.set([cards[9]])
        
        player_hands = {}
        for i, player in enumerate(self.players.all()):
            player_hands[player.nick] = [card.id for card in cards[i * 5:(i + 1) * 5]]
        
        self.hands = player_hands
        self.turn_order = [player.nick for player in self.players.all()]
        self.current_turn = 0
        self.save()
