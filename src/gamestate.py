

class GameState:
    def __init__(self):
        self.players = {}
    def add_player(name):
        # adds new player to the game
        if name in self.players:
            return
        self.players[name] = Player(name)
    def bump_score(name, num):
        # bumps name's score by num
        # returns new score
        for p in self.players:
            if p.name == name:
                p.score += num
                return p.score

class Player:
    def __init__(self, name):
        self.name = name
        self.score = 0
        self.latency = None
