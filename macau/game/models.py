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
