class Rules:
    def __init__(self, rules, custom_settings=None):
        self.rules = rules
        self.custom_settings = custom_settings

    def apply_rules(self, deck, player_hand, discard_pile):
        if "Standard" in self.rules:
            self.apply_standard_rules(deck, player_hand, discard_pile)
        if "Custom" in self.rules:
            self.apply_custom_rules(deck, player_hand, discard_pile)

    def apply_standard_rules(self, deck, player_hand, discard_pile):
        """
        Zasady standardowe Makao:
        - Można położyć kartę o tym samym kolorze lub tym samym numerze
        - Jeśli gracz nie może zagrać żadnej karty, dobiera jedną z talii głównej
        - Gra kończy się, gdy gracz nie ma kart na ręce
        """
        if not player_hand:
            return "win"
        
        top_card = discard_pile[0]
        valid_moves = [card for card in player_hand if card.color == top_card.color or card.number == top_card.number]
        if valid_moves:
            return valid_moves
        else:
            if deck:
                player_hand.append(deck.pop())
            return "draw"
        
    def apply_war_rules(self, deck, player_hand, discard_pile):
        """
        Zasady Makao bitwa:
        - Można położyć kartę o tym samym kolorze lub tym samym numerze
        - Jeśli gracz nie może zagrać żadnej karty, dobiera jedną z talii głównej
        - Gra kończy się, gdy gracz nie ma kart na ręce
        - Karta 2 dowolnego koloru - nastepny gracz dobiera 2 karty
        - Karta 3 dowolnego koloru - nastepny gracz dobiera 3 karty
        - Karta 4 dowolnego koloru - nastepny gracz daje 4 albo pauzje
        - Karta Walet dowolnego koloru - gracz żąda karty
        - Karta Dama karo/pik - bitna
        - Karta Dama kier/trefl - niebitna
        - Karta Dama na wszystko, wszystko na dame
        - Karta Król karo/pik - bitny, nastepny gracz dobiera 5 kart
        - Karta Król trefl/kier - niebitny, analuje króla bitnego
        """
        if not player_hand:
            return "win"

        top_card = discard_pile[0]

        playable_cards = [
            card for card in player_hand 
            if top_card is None or card.color == top_card.color or card.number == top_card.number
        ]

        if playable_cards:
            played_card = playable_cards[0]
            player_hand.remove(played_card)
            discard_pile.append(played_card)

            if played_card.number == 2:
                self.force_draw(deck, 2)
            elif played_card.number == 3:
                self.force_draw(deck, 3)
            elif played_card.number == 4:
                pass
            elif played_card.marking == 'walet':
                pass
            elif played_card.marking == 'dama':
                if played_card.color in ['karo', 'pik']:
                    # Dama bitna
                    pass
                elif played_card.color in ['kier', 'trefl']:
                    # Dama niebitna
                    pass
            elif played_card.marking == 'krol':
                if played_card.color in ['karo', 'pik']:
                    # Król bitny
                    self.force_draw(deck, 5)
                elif played_card.color in ['kier', 'trefl']:
                    # Król niebitny
                    pass
        else:
            if deck:
                drawn_card = deck.pop(0)
                player_hand.append(drawn_card)

        if not player_hand:
            return "win"
        return "continue"

    def apply_custom_rules(self, deck):
        pass