class PiggyBank:
    # create __init__ and add_money methods
    def __init__(self, dollars, cents):
        self.dollars = dollars
        self.cents = cents

    def add_money(self, deposit_dollars, deposit_cents):
        self.dollars = self.dollars + deposit_dollars
        self.cents = self.cents + deposit_cents
        if self.cents > 99:
            self.dollars = self.dollars + self.cents // 100
            self.cents = self.cents % 100