from django.shortcuts import render
from .models import Card

def deck_generator():
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
