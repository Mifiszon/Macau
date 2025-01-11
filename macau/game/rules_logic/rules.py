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
            - Można położyć kartę o tym samym kolorze lub tym samym numerze.
            - Jeśli gracz nie może zagrać żadnej karty, dobiera jedną z talii głównej.
            - Gra kończy się, gdy gracz nie ma kart na ręce.
            """
            if not player_hand:
                return "win"
            
            top_card = discard_pile[-1]
            valid_moves = [card for card in player_hand if card.color == top_card.color or card.number == top_card.number]
            if valid_moves:
                return valid_moves
            else:
                if deck:
                    player_hand.append(deck.pop())
                return "draw"

        def apply_custom_rules(self, deck):
            pass