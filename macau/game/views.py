from django.shortcuts import render, redirect
from .models import Card
from .forms import PlayerForm

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

def home(request):
    form = PlayerForm
    if request.method == "POST":
        form = PlayerForm(request.POST)
        if form.is_valid():
            nick = form.cleaned_data['nick']
            request.session['nick'] = nick
            return redirect('rules')
    return render(request, 'home.html', {'form': form})

def rules(request):
    if request.method == "POST":
        selected_rules = request.POST.getlist('rules')
        custom_settings = request.POST.get('custom_settings', None)
        return redirect('game')
    return render(request, rules.html)
