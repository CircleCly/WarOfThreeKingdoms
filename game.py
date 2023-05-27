import random

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
    
    def can_target(self, user, target) -> bool:
        if self.name == "fire":
            return target.hero.alive and user.id != target.id
        return True
        
    def __str__(self):
        return f"({self.suit}, {self.num}, {self.name})"
    
    def __repr__(self):
        return str(self)
    
class Game():
    def __init__(self, seed: int):
        random.seed(seed)

        self.players: list[Player] = [Player(0, "commander"), Player(1, "impostor")]
        self.players[0].choose_hero(Hero(4, 4, self))
        self.players[1].choose_hero(Hero(4, 4, self))
        
        self.card_pile: list[Card] = Game.get_fire_dodge_pile()
        self.discard_pile: list[Card] = []

        for player in self.players:
            for i in range(4):
                player.hero.hand.append(self.draw_card())

    def get_fire_dodge_pile():
        pile = []
        for i in range(1, 14):
            pile.append(Card("heart", i, "dodge"))
            pile.append(Card("diamond", i, "dodge"))
            pile.append(Card("spade", i, "fire"))
            pile.append(Card("club", i, "fire"))
        random.shuffle(pile)
        return pile
    
    def play_game(self):
        cur_player_id = 0
        while True:
            cur_player = self.players[cur_player_id]
            if cur_player.hero.alive:
                cur_player.hero.do_round()
            cur_player_id = (cur_player_id + 1) % len(self.players)

    
    def draw_card(self) -> Card:
        return self.card_pile.pop(0)
    
    def recycle_card(self, card):
        print(f"-1t {card}")
        self.discard_pile.append(card)

    def check_win_condition(self):
        alive_state = [v.hero.alive for v in self.players]
        if sum(alive_state) == 1:
            for i in range(len(self.players)):
                if alive_state[i]:
                    print(f"Player {i} won!")
                    exit(0)

class Player():
    '''
    Player class for WTK
    '''
    def __init__(self, player_id: int, identity: str):
        self.identity = identity
        self.id = player_id
        self.hero: Hero = None
    
    def choose_hero(self, hero):
        self.hero = hero
        hero.player = self

    def __str__(self):
        return f"{self.id}: {self.hero.hp} / {self.hero.max_hp}, {len(self.hero.hand)} card(s)"
    
    def __repr__(self):
        return str(self)

def number_query(prompt, is_valid):
    '''
    Queries for a number until a valid input has been given
    '''
    valid = False
    while not valid:
        try:
            val = int(input(prompt))
            valid = is_valid(val)
            if not valid:
                print("Invalid Input.")
        except ValueError:
            valid = False
            print("Invalid Input.")
    return val

class Hero():
    def __init__(self, hp: int, max_hp: int, game: Game):
        self.hp = hp
        self.max_hp = max_hp
        self.alive: bool = True
        self.player: Player = None
        self.game = game
        self.hand: list[Card] = []
        pass

    def do_round(self):
        self.prepare()
        self.judge()
        self.draw()
        self.deal()
        self.discard()
        self.end()
        
    def prepare(self):
        pass
        
    def judge(self):
        pass

    def draw(self):
        self.hand.append(self.game.draw_card())
        self.hand.append(self.game.draw_card())

    def deal(self):
        index = None
        while index != -1:
            print(f"Player {self.player.id}'s turn!")
            print("Players:")
            print(self.game.players)
            print("Cards:")
            print(self.hand)

            index = number_query("Card Index (-1 to pass):",
                                 lambda x: x == -1 or
                                 (0 <= x < len(self.hand) and self.hand[x].usable_in_round()))
                                 
            if index == -1:
                break
            card = self.hand.pop(index)

            target_id = number_query("Target Id:",
                                     lambda x: 0 <= x < len(self.game.players) and
                                     card.can_target(self.player, self.game.players[x]))
            target_player = self.game.players[target_id]

            target_player.hero.respond(card, self)
            self.game.discard_pile.append(card)
        pass

    def discard(self):
        while len(self.hand) > self.hp:
            print(f"Please discard {len(self.hand) - self.hp} card(s).")
            print(self.hand)
            index = number_query("Card Index to discard:", lambda x: 0 <= x < len(self.hand))
            self.game.recycle_card(self.hand.pop(index))
    
    def end(self):
        pass

    def respond(self, card, source):
        print("Cards:")
        print(self.hand)

        index = number_query("Card Index to respond(Enter -1 to do nothing):",
                             lambda x: x == -1 or self.hand[x].usable_out_round())
        if index == -1:
            self.take_damage(1)
        else:
            self.game.recycle_card(self.hand.pop(index))

    def take_damage(self, amount: int):
        self.hp -= amount
        if self.hp <= 0:
            self.alive = False
            self.game.check_win_condition()

if __name__ == "__main__":
    g = Game(seed=0)
    g.play_game()