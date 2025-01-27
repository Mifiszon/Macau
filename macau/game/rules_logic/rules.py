class Rules:
    def __init__(self, rules, custom_settings=None):
        if rules is None:
            rules = []
        self.rules = rules
        self.custom_settings = custom_settings

    def apply_rules(self, card, top_card):
        """
        Aplikuje aktywne zasady do gry.
        """
        if "Standard" in self.rules:
            if self.apply_standard_rules(card, top_card):
                return True
        if "War" in self.rules:
            if self.apply_war_rules(card, top_card):
                return True
        if "Custom" in self.rules:
            if self.apply_custom_rules(card, top_card):
                return True
        return False

    def apply_standard_rules(self, card, top_card, ):
        """
        Zasady standardowe Makao:
        - Można położyć kartę o tym samym kolorze lub tym samym numerze
        """
        if card.number and top_card.number:
            if card.number == top_card.number:
                return True
    
        if card.marking and top_card.marking:
            if card.marking == top_card.marking:
                return True
        
        if card.color == top_card.color:
            return True
        
        return False

        
    def apply_war_rules(self, card, top_card):
        """
        Zasady Makao bitwa (war):
        - Można położyć kartę o tym samym kolorze lub tym samym numerze
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
        if card.number and top_card.number:
            if card.number == top_card.number:
                return True
    
        if card.marking and top_card.marking:
            if card.marking == top_card.marking:
                return True
        
        if card.color == top_card.color:
            return True

        if card.number == 2:
            return "draw_2_cards"

        if card.number == 3:
            return "draw_3_cards"

        if card.number == 4:
            return "play_4_or_skip"

        if card.marking == 'walet':
            return "ask_for_card"

        if card.marking == 'dama':
            if card.color in ['kier', 'pik']:
                return "bitna"
            elif card.color in ['karo', 'trefl']:
                return "niebitna"

        if card.marking == 'krol':
            if card.color in ['kier', 'pik']:
                return "bitny, draw_5_cards"
            elif card.color in ['karo', 'trefl']:
                return "niebitny, cancel_bitny"

        return False


    def apply_custom_rules(self, card, top_card):
        """
        Zasady własne
        """
        pass