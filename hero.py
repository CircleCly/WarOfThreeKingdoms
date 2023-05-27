from player import Player
class Hero():
    def __init__(self, hp: int, max_hp: int, player: Player):
        self.hp = hp
        self.max_hp = max_hp
        self.player = player
        pass
        
    def prepare(self):
        pass
        
    def judge(self):
        pass

    def draw(self):
        pass

    def deal(self):
        pass

    def discard(self):
        pass
    
    def end(self):
        pass

    def respond(self, card, source):
        pass
