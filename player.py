import pygame


class Player:
    def __init__(self, win, username):
        self.name = username
        self.x = 500
        self.y = 400
        self.speed = 5
        self.color = (255, 0, 0)
        self.radius = 10
        self.win = win
        self.win_width = 1000
        self.win_height = 800

    def draw(self):
        self.move()
        pygame.draw.circle(self.win, self.color, (self.x, self.y), self.radius)

    def move(self):
        userinput = pygame.key.get_pressed()
        if userinput[pygame.K_LEFT] and self.x > self.radius:
            self.x -= self.speed
        if userinput[pygame.K_RIGHT] and self.x < self.win_width-self.radius:
            self.x += self.speed
        if userinput[pygame.K_UP] and self.y > self.radius:
            self.y -= self.speed
        if userinput[pygame.K_DOWN] and self.y < self.win_height-self.radius:
            self.y += self.speed

    def get_pos(self):
        return self.x, self.y

    def get_name(self):
        return self.name


