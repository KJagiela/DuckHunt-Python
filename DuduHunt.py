import os
import random
import time

import pygame


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
<<<<<<< Updated upstream
=======
        # Play Gunshot Sound and add Total Sounds
        Cursor.clicked = True
>>>>>>> Stashed changes
        self.gunShotSound.play()


class Dog(Image):
    def __init__(self, subround):
        # TODO: różne pieski
        super().__init__(['Sprites/dog.PNG'], left=500, top=350)
        self.image.set_colorkey(self.image.get_at((0, 0)), pygame.constants.RLEACCEL)
        self.dogWinSound = pygame.mixer.Sound(os.path.join(os.getcwd(), 'Sounds', 'eve.oga'))
        self.dogLoseSound = pygame.mixer.Sound(os.path.join(os.getcwd(), 'Sounds', 'howlovely.wav'))
        self.subround = subround

    def celebration(self, cel_type):
        self.subround._display_surf.blit(self.subround.background.image, (0, 0))
        if cel_type == 'win':
            self.dogWinSound.play()
            self.subround._display_surf.blit(self.image, self.rect)
        elif cel_type == 'loss':
            self.subround._display_surf.blit(self.image, self.rect)
        pygame.display.update()


class Duck(Image):
    def __init__(self, playground, duck_type, level_no):
        ducks = {'ola': 'blue',
                 'korwin': 'blue',
                 'lysy': 'red',
                 'janek': 'black'
                 }
        # Point Values Based On Duck Color
<<<<<<< Updated upstream
        point_values = {"blue": 1000, "red": 1500, "black": 500}  # TODO zależnie od levelu się zmienia
        super().__init__(['Sprites/{}/duck1.png'.format(ducks[duck_type])], left=250, top=300, scale=(54, 57))
        self.image.set_colorkey(self.image.get_at((0, 0)), pygame.constants.RLEACCEL)
        self.velocity = 1
        self.alive = True
        self.direction = (1, 0)
        self.last_change_time = time.time()
        self.playground = playground

    def update(self):
        self.rect.left += self.velocity * self.direction[0]  # TODO zależne od lvl
        self.rect.top += self.velocity * self.direction[1]  # TODO zależne od lvl
        change_time = time.time() - self.last_change_time
        can_change_direction = (change_time > 1 and random.random() < 0.1)  # TODO nie hardkoduj tego
        can_change_direction = can_change_direction or not self.playground.contains(self.rect)  # TODO jak jesteś przy krawędzi, to wywal ją z losowania
        if can_change_direction:
            self.direction = (random.choice([-1, 1]), random.choice([-1, 0, 1]))
            self.last_change_time = time.time()
=======
        point_values = {"blue": 25, "red": 50, "black": 75}
        corner = self.image.get_at((0, 0))
        self.image.set_colorkey(corner, pygame.constants.RLEACCEL)
        super().__init__('Sprites/{}/duck1.png'.format(ducks[duck_type]), left=200, top=300)
        self.image = pygame.transform.scale(self.image, (72, 76))
        self.velocity = 1
        self.alive = True

    def update(self):
        self.rect.left += self.velocity

    def on_click(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.alive = False
>>>>>>> Stashed changes

    def on_click(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.alive = False


class Subround:

    def __init__(self, display, background):
        self._display_surf = display
        self.background = background
        self._running = True
        self.crosshair = None
<<<<<<< Updated upstream
        self.duck_count = 2
        self.shots_left = 3
        self.countdown = 10
        self.duck = None
        self.dog = None
        self.ducks_shot = 0
        self.playground = pygame.Rect(210, 0, 600, 440)
=======
        self.duck = None
>>>>>>> Stashed changes

    def on_init(self):
        self.crosshair = Cursor()
        self.duck = Duck(self.playground, 'janek', 1)  # TODO random
        self.dog = Dog(self)
        return True

    def on_event(self, event):
        if event.type == pygame.QUIT:
            Game.cleanup()
        if event.type == pygame.MOUSEBUTTONUP:
<<<<<<< Updated upstream
            self.shots_left -= 1
            if self.shots_left == 0 and self.duck_count > 0:
                self.subround_end('loss')
            self.duck.on_click()
            if not self.duck.alive:
                self.ducks_shot += 1
                self.subround_end('win')
=======
            self.crosshair.on_click()
            self.duck.on_click()
>>>>>>> Stashed changes
        if event.type == pygame.MOUSEMOTION:
            self.crosshair.update()

    def on_loop(self):
        self.crosshair.update()
        self.duck.update()

    def on_render(self):
        self._display_surf.blit(self.background.image, (0, 0))
        if self.duck.alive:
            self._display_surf.blit(self.duck.image, self.duck.rect)
        self._display_surf.blit(self.crosshair.image, self.crosshair.rect)
        pygame.display.update()

    def on_cleanup(self):
        pass

    def on_execute(self):
        self._running = self.on_init()
        while self._running:
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup()
        return self.ducks_shot

    def subround_end(self, type):
        # TODO: to będą 3 warunki, gdzieś je wrzucić
        # if self.duck_count == 0:
        # elif self.countdown == 0:
        # elif self.duck_count == 0:
        self.dog.celebration(type)
        time.sleep(2)
        self._running = False


class Round:
    ROUNDS = 2
    MIN_SUCCESS_COUNT = 0  # TODO: minimalna liczba kaczek do zastrzelenia ma rosnąć wraz z rundą

    def __init__(self, display, background):
        self._display_surf = display
        self.background = background

    def execute(self):
        ducks_shot = 0
        for i in range(self.ROUNDS):
            subround = Subround(display=self._display_surf, background=self.background)
            ducks_shot += subround.on_execute()
        return self.end_round(ducks_shot >= self.MIN_SUCCESS_COUNT)

    def end_round(self, is_win):
        pygame.font.init()
        myfont = pygame.font.SysFont('Comic Sans MS', 50)
        text = 'Round won!' if is_win else 'Round lost!'
        textsurface = myfont.render(text, False, (0, 0, 0))
        self._display_surf.blit(textsurface, (100, 100))
        pygame.display.update()
        time.sleep(1)
        return is_win


class Game:
    def __init__(self):
        self._running = True
        self._display_surf = None
        self.size = self.width, self.height = 1016, 711
        self.background = None

    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        pygame.display.set_caption('Dudu Hunt')
        self.background = Image(['Sprites/background.png'])
        return True

    @staticmethod
    def cleanup():
        # TODO display game over
        # TODO go to start screen?
        pygame.quit()

    def execute(self):
        if not self.on_init():
            self._running = False

        while self._running:
            game_round = Round(display=self._display_surf, background=self.background)
            round_result = game_round.execute()
            self._running = round_result
        self.cleanup()


if __name__ == "__main__":
    theApp = Game()
    theApp.execute()
