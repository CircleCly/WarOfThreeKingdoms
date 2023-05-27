from game import Hero
class Card():
    def __init__(self, suit: str, num: int, name: str):
        self.suit = suit
        self.num = num
        self.name = name

    def usable_in_round(self) -> bool:
        if self.name == "fire":
            return True
        else:
            return False
    
    def usable_out_round(self):
        if self.name == "dodge":
            return True
        return False
    
    def can_target(self, user: Hero, target: Hero) -> bool:
        if self.name == "fire":
            return user != target
        return True
        
    def __str__(self):
        return f"({self.suit}, {self.num}, {self.name})"
    
    def __repr__(self):
        return str(self)
