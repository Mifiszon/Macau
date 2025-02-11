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
        if self.marking:
            return f"{self.marking} {self.color}"
        else:
            return f"{self.number} {self.color}"
        
class Player(models.Model):
    nick = models.CharField(max_length=20, unique=True)
    
    def __str__(self):
        return self.nick
    
class Game(models.Model):
    player = models.OneToOneField(Player, on_delete=models.CASCADE, related_name="game_player")
    opponent = models.OneToOneField(Player, on_delete=models.CASCADE, related_name="game_opponent", null=True, blank=True)
    computer_hand = models.ManyToManyField(Card, related_name="computer_hand")
    deck = models.ManyToManyField(Card, related_name="deck")
    rules = models.CharField(max_length=50, null=True, blank=True)
    opponent_hand = models.ManyToManyField(Card, related_name='opponent_cards', blank=True)
    turn_action_done = models.BooleanField(default=False)
    last_played_card = models.ForeignKey(Card, on_delete=models.SET_NULL, null=True, related_name="last_played")
    player_hand = models.ManyToManyField(Card, related_name="player_hand")
    discard_pile = models.ManyToManyField(Card, related_name='discard_pile')
    turn = models.CharField(max_length=10, choices=[('player', 'Gracz'), ('opponent', 'Przeciwnik')], default='player')
                                         
    def __str__(self):
        return f"Game with {self.player.nick}"

class Room(models.Model):
    code = models.CharField(max_length=6, unique=True)
    players = models.ManyToManyField('Player', related_name='rooms')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Room {self.code}"
    
class MultiplayerGame(models.Model):
    room_code = models.CharField(max_length=10, unique=True)
    players = models.ManyToManyField(Player, related_name="multiplayer_games")
    deck = models.ManyToManyField(Card, related_name="multiplayer_deck")
    discard_pile = models.ManyToManyField(Card, related_name="multiplayer_discard_pile")
    turn = models.ForeignKey(Player, on_delete=models.SET_NULL, null=True, related_name="current_turn")
    started = models.BooleanField(default=False)

    def __str__(self):
        return f"Multiplayer Room {self.room_code}"

