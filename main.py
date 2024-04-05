import pygame
import json
import threading
from player import Player
from client import Client
import customtkinter
import ast

class Game:
    def __init__(self, username, color):
        self.client = Client()
        pygame.init()
        self.game_state = {}
        self.win_width = 1000
        self.win_height = 800
        self.win = pygame.display.set_mode((self.win_width, self.win_height))
        pygame.display.set_caption("Wander")
        pygame.display.set_icon(pygame.image.load("clown.jpg"))
        rgb = ast.literal_eval(color)
        self.player = Player(self.win, username, rgb)
        self.frame_rate = 60
        self.clock = pygame.time.Clock()

    def update_game_state(self):
        while True:
            try:
                data = self.client.receive()
                if data is not None:
                    self.game_state = json.loads(data)
            except:
                pass

    def run(self):
        run = True
        while run:
            self.clock.tick(self.frame_rate)
            self.win.fill((255, 255, 255))
            for player in self.game_state:
                try:
                    player_data = self.game_state[player]
                    if player_data["name"] != self.player.get_name():
                        pygame.draw.circle(self.win, rgb, player_data["pos"], 10)
                        font = pygame.font.Font('freesansbold.ttf', 12)
                        text = font.render(player_data["name"], True, (0, 0, 0))
                        text_rect = text.get_rect()
                        text_rect.center = (player_data["pos"][0], player_data["pos"][1]-15)
                        self.win.blit(text, text_rect)
                except:
                    print("Error drawing player")
                    #print(self.game_state)
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


def run_game(username, color, root):
    root.destroy()
    game = Game(username, color)
    update_thread = threading.Thread(target=game.update_game_state)
    update_thread.start()
    game.run()




if __name__ == "__main__":
    root = customtkinter.CTk()
    root.title("Join Game")
    root.geometry("400x500")
    root.resizable(False, False)

    title_label = customtkinter.CTkLabel(root, text="Game", font=("Helvetica", 64))
    title_label.place(x=120, y=75)
    username_entry = customtkinter.CTkEntry(root, width = 250,height=40, placeholder_text="Enter username", font=("Helvetica", 20), justify="center")
    username_entry.place(x=75, y=180)
    color_entry = customtkinter.CTkEntry(root, width=250, height=40, placeholder_text="Enter color (r, g, b)", font=("Helvetica", 20), justify="center")
    color_entry.place(x=75, y=235)
    submit_button = customtkinter.CTkButton(root, text="Enter", command=lambda: run_game(username_entry.get(), color_entry.get(), root), width=100, height=30, font=("Helvetica", 20))
    submit_button.place(x=150, y=285)

    root.mainloop()
