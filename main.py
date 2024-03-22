import pygame
import json
import threading
from player import Player
from client import Client

class Game:
    def __init__(self, username):
        self.client = Client()
        pygame.init()
        self.game_state = {}
        self.win_width = 1000
        self.win_height = 800
        self.win = pygame.display.set_mode((self.win_width, self.win_height))
        pygame.display.set_caption("Game")
        pygame.display.set_icon(pygame.image.load("assets/clown.jpg"))
        self.player = Player(self.win, username)
        self.frame_rate = 60
        self.clock = pygame.time.Clock()

    def update_game_state(self):
        while True:
            self.client.receive()
            data = self.client.receive()
            self.game_state = json.loads(data)
            #print(self.game_state)


    def run(self):
        run = True
        while run:
            self.clock.tick(self.frame_rate)
            self.win.fill((255, 255, 255))
            for player in self.game_state:
                try:
                    player_data = json.loads(self.game_state[player])
                    if player_data["name"] != self.player.get_name():
                        pygame.draw.circle(self.win, (0, 0, 203), player_data["pos"], 10)
                except:
                    pass
            self.player.draw()
            pygame.display.update()
            data = json.dumps({"name": self.player.get_name(), "pos": self.player.get_pos()})
            self.client.send(data)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.client.close()
                    run = False
        pygame.quit()


if __name__ == "__main__":
    username = input("Enter your username: ")
    game = Game(username)
    update_thread = threading.Thread(target=game.update_game_state)
    update_thread.start()
    game.run()
