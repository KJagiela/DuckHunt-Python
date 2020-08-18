import os
import random
import time

import pygame
from helpers import AAfilledRoundedRect


class Settings:
    change_time = 1
    change_randomized = 0.2


class Image(pygame.sprite.Sprite):
    def __init__(self, image_files, left=0, top=0, scale=None):
        super().__init__()
        self.images = [pygame.image.load(image_file) for image_file in image_files]
        self.image = self.images[0]
        if scale:
            self.images = [pygame.transform.scale(image, scale) for image in self.images]
        self.rect = self.image.get_rect()
        self.rect.left = left
        self.rect.top = top


class GameBoard(Image):
    background = Image(['Sprites/background_cut.png'])
    size = width, height = 599, 468
    display_surf = pygame.display.set_mode(size, pygame.HWSURFACE | pygame.DOUBLEBUF)

    @staticmethod
    def render():
        GameBoard.display_surf.blit(GameBoard.background.image, (0, 0))
        myfont = pygame.font.Font('Sprites/duckhunt.ttf', 16)
        text = 'R = {}'.format(Game.round_count)
        textsurface = myfont.render(text, False, (0, 255, 0), (0, 0, 0))
        GameBoard.display_surf.blit(textsurface, (55, 384))
        AAfilledRoundedRect(GameBoard.display_surf, (50, 410, 62, 42), 'green', )
        AAfilledRoundedRect(GameBoard.display_surf, (51, 411, 60, 40), 'black', )
        AAfilledRoundedRect(GameBoard.display_surf, (145, 410, 252, 42), 'green', )
        AAfilledRoundedRect(GameBoard.display_surf, (146, 411, 250, 40), 'black', )
        AAfilledRoundedRect(GameBoard.display_surf, (440, 410, 110, 42), 'green', )
        AAfilledRoundedRect(GameBoard.display_surf, (441, 411, 108, 40), 'black', )
        pygame.display.update()


class Cursor(Image):
    def __init__(self):
        super().__init__(['Sprites/cursor.png'], left=500, top=350)  # TODO
        # Load gunshot sound
        self.gunShotSound = pygame.mixer.Sound(os.path.join(os.getcwd(), 'Sounds', 'shot.wav'))
        # Hide mouse
        pygame.mouse.set_visible(False)
        self.clicked = False

    def update(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.rect.left = mouse_x - self.rect.size[0] / 2
        self.rect.top = mouse_y - self.rect.size[1] / 2

    def on_click(self):
        self.gunShotSound.play()


class Dog(Image):
    def __init__(self):
        # TODO: różne pieski
        super().__init__(['Sprites/dog.PNG', 'Sprites/dog_laugh.PNG'], left=500, top=350)
        self.image.set_colorkey(self.image.get_at((0, 0)), pygame.constants.RLEACCEL)
        self.dogWinSound = pygame.mixer.Sound(os.path.join(os.getcwd(), 'Sounds', 'howlovely.wav'))
        self.dogLoseSound = pygame.mixer.Sound(os.path.join(os.getcwd(), 'Sounds', 'eve.oga'))

    def celebration(self, cel_type):
        GameBoard.display_surf.blit(GameBoard.background.image, (0, 0))
        if cel_type == 'win':
            self.dogWinSound.play()
            GameBoard.display_surf.blit(self.image, self.rect)
        elif cel_type == 'loss':
            self.image = self.images[1]
            self.dogLoseSound.play()
            GameBoard.display_surf.blit(self.image, self.rect)
        pygame.display.update()


class Duck(Image):
    def __init__(self, duck_type, level_no):
        ducks = {'ola': 'blue',
                 'korwin': 'blue',
                 'lysy': 'red',
                 'janek': 'black'
                 }
        # Point Values Based On Duck Color
        point_values = {"blue": 1000, "red": 1500, "black": 500}  # TODO zależnie od levelu się zmienia
        self.scale = (54, 57)
        super().__init__(['Sprites/{}/duck1.png'.format(ducks[duck_type])], left=250, top=200, scale=self.scale)
        self.image.set_colorkey(self.image.get_at((0, 0)), pygame.constants.RLEACCEL)
        self.velocity = 1  # TODO zależne od lvl
        self.velocity_dead = 5
        self.alive = True
        self.duck_gone = False
        self.direction = (1, 0)
        self.last_change_time = time.time()

    def change_direction(self):
        direction_x = random.choice([-1, 1])
        direction_y = random.choice([-1, 0, 1])
        change_time = time.time() - self.last_change_time
        if not Subround.playground.contains(self.rect):
            if self.rect.left <= Subround.playground.left:
                direction_x = 1
            elif self.rect.right >= Subround.playground.right:
                direction_x = -1
            if self.rect.top <= Subround.playground.top:
                direction_y = random.choice([0, 1])
            elif self.rect.bottom >= Subround.playground.bottom:
                direction_y = random.choice([-1, 0])
        elif change_time > Settings.change_time and random.random() < Settings.change_randomized:
            self.last_change_time = time.time()
        else:
            return
        self.direction = (direction_x, direction_y)

    def update(self):
        if self.alive:
            self.update_alive()
        else:
            self.update_dead()

    def update_alive(self):
        self.rect.left += self.velocity * self.direction[0]
        self.rect.top += self.velocity * self.direction[1]
        self.change_direction()

    def update_dead(self):
        self.rect.top += self.velocity_dead
        if self.rect.bottom >= Subround.playground.bottom:
            self.duck_gone = True

    def on_click(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.alive = False


class Subround:
    playground = pygame.Rect(0, 0, 599, 302)

    def __init__(self):
        self._running = True
        self.duck_count = 2
        self.shots_left = 3
        self.countdown = 10
        self.crosshair = Cursor()
        self.duck = Duck('janek', 1)  # TODO random
        self.dog = Dog()
        self.ducks_shot = 0
        self.start_time = time.time()

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
            pygame.quit()
        if event.type == pygame.MOUSEBUTTONUP:
            self.shots_left -= 1
            self.crosshair.on_click()
            self.duck.on_click()
        if event.type == pygame.MOUSEMOTION:
            self.crosshair.update()

    def on_loop(self):
        self.crosshair.update()
        self.duck.update()
        if self.duck.duck_gone:
            self.ducks_shot += 1
            self.subround_end('win')
        elif self.shots_left <= 0 or time.time() - self.start_time > 7: # TODO variable
            self.subround_end('loss')

    def on_render(self):
        GameBoard.render()
        GameBoard.display_surf.blit(self.duck.image, self.duck.rect)
        if self.duck.alive:
            GameBoard.display_surf.blit(self.crosshair.image, self.crosshair.rect)
        pygame.display.update()

    def on_execute(self):
        self._running = True
        while self._running:
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        return self.ducks_shot

    def subround_end(self, end_type):
        self.dog.celebration(end_type)
        time.sleep(2)
        self._running = False


class Round:
    ROUNDS = 2
    MIN_SUCCESS_COUNT = 0  # TODO: minimalna liczba kaczek do zastrzelenia ma rosnąć wraz z rundą

    def execute(self):
        ducks_shot = 0
        for i in range(self.ROUNDS):
            subround = Subround()
            ducks_shot += subround.on_execute()
        return self.end_round(ducks_shot >= self.MIN_SUCCESS_COUNT)

    def end_round(self, is_win):
        myfont = pygame.font.SysFont('Comic Sans MS', 50)
        text = 'Round won!' if is_win else 'Round lost!'
        textsurface = myfont.render(text, False, (0, 0, 0))
        GameBoard.display_surf.blit(textsurface, (100, 100))
        pygame.display.update()
        time.sleep(1)
        return is_win


class Game:
    round_count = 0
    _running = True

    def on_init(self):
        pygame.mixer.pre_init(22050, -16, 2, 1024)
        pygame.init()
        pygame.font.init()
        pygame.mixer.quit()
        pygame.mixer.init(22050, -16, 2, 1024)
        pygame.display.set_caption('Dudu Hunt')
        return True

    @staticmethod
    def cleanup():
        # TODO display game over
        # TODO go to start screen?
        pygame.quit()

    def render(self):
        pass
        # TODO display round number
        # TODO display shots left
        # TODO display ducks hit + timer
        # TODO display score

    def execute(self):
        if not self.on_init():
            self._running = False

        while self._running:
            self.round_count += 1
            self.render()
            game_round = Round()
            round_result = game_round.execute()
            self._running = round_result
        self.cleanup()


if __name__ == "__main__":
    theApp = Game()
    theApp.execute()
