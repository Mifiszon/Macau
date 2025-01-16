from django.db import models

class Card(models.Model):
    COLORS = [('pik', 'Pik'), ('kier', 'Kier'), ('karo', 'Karo'), ('trefl', 'Trefl')]
    MARKINGS = [('walet', 'Walet'), ('dama', 'Dama'), ('krol', 'Król'), ('as', 'As')]

    color = models.CharField(max_length=10, choices=COLORS)
    number = models.IntegerField(null=True, blank=True)
    marking = models.CharField(max_length=10, choices=MARKINGS, null=True, blank=True)
    function = models.CharField(max_length=100, null=True, blank=True)
    image = models.ImageField(upload_to="cards/", null=True)

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
    computer_hand = models.ManyToManyField(Card, related_name="computer_hand")
    deck = models.ManyToManyField(Card, related_name="deck")
    last_played_card = models.ForeignKey(Card, on_delete=models.SET_NULL, null=True, related_name="last_played")
    player_hand = models.ManyToManyField(Card, related_name="player_hand")
                                         
    def __str__(self):
        return f"Game with {self.player.nick}"
