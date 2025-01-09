class Rules:
    def __init__(self, rules, custom_settings=None):
        self.rules = rules
        self.custom_settings = custom_settings

        def apply_rules(self, deck):
            if "Standard" in self.rules:
                self.apply_standard_rules(deck)
            if "Custom" in self.rules:
                self.apply_custom_rules(deck)

        def apply_standard_rules(self,deck):
            pass

        def apply_custom_rules(self, deck):
            pass