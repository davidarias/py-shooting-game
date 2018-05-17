import sys
import pygame

from utils import random_position
from entities import Alien, Explosion

clock = pygame.time.Clock()
FPS = 60

class Game:

    def __init__(self, width, height):
        self.size = (width, height)
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption('Shooting Game')

        # convert to the same pixel format as the display Surface.
        # This is always the fastest format for blitting.
        # It is a good idea to convert all Surfaces before they are
        # blitted many times.
        self.background = pygame.image.load("img/starfield.png").convert()

        self.aliens = pygame.sprite.Group()
        self.explosions = pygame.sprite.Group()

        self.add_alien() # first alien

        self.interval = 1000 # interval in which the aliens appear

        self.interval_decrement = 10
        self.time_to_next_alien = self.interval

        self.score = 0
        self.score_increment = 10

    def add_alien(self):
        self.aliens.add(
            Alien(position=random_position(0, self.size[0])))

    def start(self):
        while self.mainLoop():
            pass

        self.game_over()

    def mainLoop(self):

        # how many milliseconds have passed since the previous call
        dt = clock.tick(FPS)

        self.check_add_new_alien(dt)

        for event in pygame.event.get():
            self.handleEvent(event)

        self.render(dt)

        # game over
        if len(self.aliens) > 20:
            return False

        return True

    def check_add_new_alien(self, dt):
        self.time_to_next_alien -= dt
        if self.time_to_next_alien <= 0:
            self.add_alien()
            self.time_to_next_alien = self.interval

    def handleEvent(self, event):

        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

            for alien in self.aliens:
                if alien.rect.collidepoint(event.pos):

                    alien.kill()
                    self.explosions.add(Explosion(alien))

                    self.score += self.score_increment
                    self.score_increment += 10

                    self.interval -= self.interval_decrement

                    if self.interval > 350:
                        self.interval_decrement += 5
                    elif self.interval > 320:
                        self.interval_decrement = 1
                    else:
                        self.interval_decrement = 0


    def render(self, dt):

        self.screen.blit(self.background, (0,0))

        self.aliens.update(dt)
        self.aliens.draw(self.screen)

        self.explosions.update(dt)
        self.explosions.draw(self.screen)


        font = pygame.font.SysFont('Monospace bold', 30)

        # score text
        score_text = font.render(
            'Score: %s' % self.score, False, (255, 255, 255))
        self.screen.blit(score_text, (0, 0))

        # remaining aliens text
        num_aliens = len(self.aliens)

        if (num_aliens < 10):
            aliens_text_color = (255, 255, 255)
        elif num_aliens < 15:
            aliens_text_color = (255, 255, 0)
        else:
            aliens_text_color = (255, 0, 0)

        aliens_text = font.render(
            'Aliens: %s' % num_aliens , False, aliens_text_color)
        self.screen.blit(aliens_text, (0, 30))

        pygame.display.flip()

    def game_over(self):

        font = pygame.font.SysFont('Monospace bold', 80)
        score_text = font.render('GAME OVER', False, (255, 255, 255))
        self.screen.blit(score_text, (80, 200))

        pygame.display.flip()

        while 1:
            clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()



if __name__ == "__main__":
    pygame.init()
    pygame.font.init()

    game = Game(512, 512)
    game.start()
