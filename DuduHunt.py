import os
import random
import sys
import time

import pygame

from helpers import AAfilledRoundedRect


# TODO na kiedyś - scoreboard
play_again = True


def wait():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return True


class Settings:
    change_time = 1
    change_randomized = 0.2


class Image(pygame.sprite.Sprite):
    def __init__(self, image_files, left=0, top=0, scale=None):
        super().__init__()
        self.images = [pygame.image.load(image_file) for image_file in image_files]
        if scale:
            self.images = [pygame.transform.scale(image, scale) for image in self.images]
        self.image = self.images[0]
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
        duck_font = pygame.font.Font('Sprites/duckhunt.ttf', 16)
        text = 'R = {}'.format(Game.round_count)
        textsurface = duck_font.render(text, False, (0, 255, 0), (0, 0, 0))
        GameBoard.display_surf.blit(textsurface, (55, 384))
        AAfilledRoundedRect(GameBoard.display_surf, (50, 410, 62, 42), 'green', )
        AAfilledRoundedRect(GameBoard.display_surf, (51, 411, 60, 40), 'black', )
        AAfilledRoundedRect(GameBoard.display_surf, (140, 410, 262, 42), 'green', )
        AAfilledRoundedRect(GameBoard.display_surf, (141, 411, 260, 40), 'black', )
        AAfilledRoundedRect(GameBoard.display_surf, (440, 410, 110, 42), 'green', )
        AAfilledRoundedRect(GameBoard.display_surf, (441, 411, 108, 40), 'black', )
        menu_font = pygame.font.Font('Sprites/menu.ttf', 11)
        text_shot = 'SHOT'
        textsurface_shot = menu_font.render(text_shot, False, (63, 191, 255), (0, 0, 0))
        GameBoard.display_surf.blit(textsurface_shot, (59, 438))
        menu_font_big = pygame.font.Font('Sprites/menu.ttf', 13)
        text_hit = 'HIT'
        textsurface_hit = menu_font_big.render(text_hit, False, (0, 255, 0), (0, 0, 0))
        GameBoard.display_surf.blit(textsurface_hit, (150, 418))
        for i in range(4 * Game.curr_min_duck_count):
            pygame.draw.rect(GameBoard.display_surf, (63, 191, 255), [196 + 5 * i, 435, 3, 12])
        textsurface_sv = menu_font_big.render(str(Game.score), False, (255, 255, 255), (0, 0, 0))
        GameBoard.display_surf.blit(textsurface_sv, (542 - 12 * len(str(Game.score)), 418))
        textsurface_score = menu_font_big.render('SCORE', False, (255, 255, 255), (0, 0, 0))
        GameBoard.display_surf.blit(textsurface_score, (480, 435))

    @staticmethod
    def duck_fly_away():
        AAfilledRoundedRect(GameBoard.display_surf, (240, 140, 120, 20), 'green', )
        AAfilledRoundedRect(GameBoard.display_surf, (241, 141, 118, 18), 'black', )
        menu_font = pygame.font.Font('Sprites/menu.ttf', 11)
        text_shot = 'FLY AWAY'
        textsurface_shot = menu_font.render(text_shot, False, (63, 191, 255), (0, 0, 0))
        GameBoard.display_surf.blit(textsurface_shot, (255, 145))

    @staticmethod
    def perfect_bonus():
        AAfilledRoundedRect(GameBoard.display_surf, (240, 130, 120, 40), 'green', )
        AAfilledRoundedRect(GameBoard.display_surf, (241, 131, 118, 38), 'black', )
        menu_font = pygame.font.Font('Sprites/menu.ttf', 11)
        text_shot = 'PERFECT'
        textsurface_shot = menu_font.render(text_shot, False, (63, 191, 255), (0, 0, 0))
        GameBoard.display_surf.blit(textsurface_shot, (255, 135))
        textsurface_shot = menu_font.render(str(Round.perfect_bonus()), False, (63, 191, 255), (0, 0, 0))
        GameBoard.display_surf.blit(textsurface_shot, (265, 150))

    @staticmethod
    def welcome():
        GameBoard.display_surf.fill((0, 0, 0))
        menu_font = pygame.font.Font('Sprites/menu.ttf', 20)
        textsurface = menu_font.render('NAJBARDZIEJ CHUJOWA', False, (255, 255, 255), (0, 0, 0))
        GameBoard.display_surf.blit(textsurface, (135, 105))
        textsurface = menu_font.render('GRA SWIATA', False, (255, 255, 255), (0, 0, 0))
        GameBoard.display_surf.blit(textsurface, (185, 155))
        menu_font = pygame.font.Font('Sprites/Royalacid.ttf', 20)
        textsurface = menu_font.render('The Rolling Stone', False, (255, 255, 255), (0, 0, 0))
        GameBoard.display_surf.blit(textsurface, (285, 235))

    @staticmethod
    def welcome2():
        GameBoard.display_surf.fill((0, 0, 0))
        menu_font = pygame.font.Font('Sprites/menu.ttf', 20)
        textsurface = menu_font.render('MEHEHEHEHEHEH', False, (255, 255, 255), (0, 0, 0))
        GameBoard.display_surf.blit(textsurface, (135, 105))
        menu_font = pygame.font.Font('Sprites/Royalacid.ttf', 20)
        textsurface = menu_font.render('The Times', False, (255, 255, 255), (0, 0, 0))
        GameBoard.display_surf.blit(textsurface, (285, 185))

    @staticmethod
    def welcome3():
        GameBoard.display_surf.fill((0, 0, 0))
        menu_font = pygame.font.Font('Sprites/menu.ttf', 20)
        textsurface = menu_font.render('THAT\'S SOMETHING', False, (255, 255, 255), (0, 0, 0))
        GameBoard.display_surf.blit(textsurface, (135, 105))
        menu_font = pygame.font.Font('Sprites/Royalacid.ttf', 20)
        textsurface = menu_font.render('Filthy Casuals', False, (255, 255, 255), (0, 0, 0))
        GameBoard.display_surf.blit(textsurface, (285, 185))

    @staticmethod
    def welcome_menu():
        GameBoard.display_surf.fill((0, 0, 0))
        menu_font = pygame.font.Font('Sprites/duckhunt.ttf', 80)
        textsurface = menu_font.render('DUDU', False, (255, 255, 255), (0, 0, 0))
        GameBoard.display_surf.blit(textsurface, (135, 85))
        textsurface = menu_font.render('HUNT', False, (255, 255, 255), (0, 0, 0))
        GameBoard.display_surf.blit(textsurface, (235, 175))
        menu_font = pygame.font.Font('Sprites/menu.ttf', 20)
        textsurface = menu_font.render('PRESS SPACE TO START', False, (255, 255, 255), (0, 0, 0))
        GameBoard.display_surf.blit(textsurface, (135, 305))

    @staticmethod
    def game_over():
        GameBoard.display_surf.fill((0, 0, 0))
        menu_font = pygame.font.Font('Sprites/duckhunt.ttf', 80)
        textsurface = menu_font.render('GAME', False, (255, 255, 255), (0, 0, 0))
        GameBoard.display_surf.blit(textsurface, (135, 85))
        textsurface = menu_font.render('OVER', False, (255, 255, 255), (0, 0, 0))
        GameBoard.display_surf.blit(textsurface, (235, 175))
        menu_font = pygame.font.Font('Sprites/menu.ttf', 20)
        textsurface = menu_font.render('PRESS SPACE', False, (255, 255, 255), (0, 0, 0))
        GameBoard.display_surf.blit(textsurface, (135, 305))
        textsurface = menu_font.render('TO PLAY AGAIN', False, (255, 255, 255), (0, 0, 0))
        GameBoard.display_surf.blit(textsurface, (155, 335))


class GoalDuck(Image):
    def __init__(self, duck_no):
        left = 195 + duck_no * 20
        super().__init__(['Sprites/duck_white.jpg', 'Sprites/duckred.jpg', 'Sprites/duck_black.jpg'], left=left,
                         top=415, scale=(16, 16))
        self.status = True
        self.time_since_last_blink = 0

    def update(self):
        if self.time_since_last_blink > 15:
            self.time_since_last_blink = 0
            if self.status:
                self.image = self.images[2]
                self.status = False
            else:
                self.image = self.images[0]
                self.status = True
        else:
            self.time_since_last_blink += 1


class Bullet(Image):
    def __init__(self, bullet_no):
        width = 16
        left = 57 + bullet_no * width
        super().__init__(['Sprites/bullet.png'], left=left, top=415, scale=(width, 20))


class Cursor(Image):
    def __init__(self):
        super().__init__(['Sprites/cursor.png'], left=200, top=234)
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
    def __init__(self, duck):
        image = duck.selected_image[0]
        dog = self.select_dog_laugh(duck)
        super().__init__([image, dog[0]], left=300, top=250, scale=(50, 50))
        self.image.set_colorkey(self.image.get_at((0, 0)), pygame.constants.RLEACCEL)
        self.dogLoseSound = pygame.mixer.Sound(os.path.join(os.getcwd(), 'Sounds', dog[1], '{}.wav'.format(
            random.randrange(1, 5))))

    def celebration(self, cel_type):
        GameBoard.display_surf.blit(GameBoard.background.image, (0, 0))
        if cel_type == 'loss':
            self.image = self.images[1]
            self.dogLoseSound.play()
        GameBoard.display_surf.blit(self.image, self.rect)
        pygame.display.update()

    def select_dog_laugh(self, duck):
        dogs = ['janek', 'ola', 'slawek', 'korwin']
        dog_image = {
            'janek': [
                ['Sprites/janek/janek1.png'],
                ['Sprites/janek/janek2.png'],
                ['Sprites/janek/janek3.png'],
                ['Sprites/janek/janek4.png'],
            ],
            'ola': [
                ['Sprites/ola/ola.png'],
                ['Sprites/ola/ola2.png'],
                ['Sprites/ola/ola3.png'],
                ['Sprites/ola/ola4.png'],
            ],
            'slawek': [
                ['Sprites/slawek/slawek1.png'],
                ['Sprites/slawek/slawek2.png'],
                ['Sprites/slawek/slawek3.png'],
            ],
            'korwin': [
                ['Sprites/korwin/korwin1.png'],
                ['Sprites/korwin/korwin2.png'],
                ['Sprites/korwin/korwin31.png', 'Sprites/korwin/korwin32.png'],
                ['Sprites/korwin/korwin41.png', 'Sprites/korwin/korwin42.png']
            ],
        }
        dogs.remove(duck.duck_type)
        selected_dog = random.choice(dogs)
        return random.choice(dog_image[selected_dog])[0], selected_dog


class Duck(Image):
    def __init__(self):
        self.duck_type = random.choice(['janek', 'slawek', 'ola', 'korwin'])
        self.selected_image = self.select_duck()
        super().__init__(self.selected_image, left=250,
                         top=200, scale=(60, 60))
        self.image.set_colorkey(self.image.get_at((0, 0)), pygame.constants.RLEACCEL)
        self.velocity = 0.105 * Game.round_count + 0.895 if Game.round_count < 20 else 3.5
        self.velocity_dead = 3
        self.alive = True
        self.duck_gone = False
        self.duck_escaping = False
        self.direction = (random.choice((1, -1)), random.choice((1, -1, 0)))
        self.last_change_time = time.time()
        self.image_no = 0
        self.change_counter = 0

    def select_duck(self):
        duck_image = {
            'janek': [
                ['Sprites/janek/janek1.png'],
                ['Sprites/janek/janek2.png'],
                ['Sprites/janek/janek3.png'],
                ['Sprites/janek/janek4.png'],
            ],
            'ola': [
                ['Sprites/ola/ola.png'],
                ['Sprites/ola/ola2.png'],
                ['Sprites/ola/ola3.png'],
                ['Sprites/ola/ola4.png'],
            ],
            'slawek': [
                ['Sprites/slawek/slawek1.png'],
                ['Sprites/slawek/slawek2.png'],
                ['Sprites/slawek/slawek3.png'],
            ],
            'korwin': [
                ['Sprites/korwin/korwin1.png'],
                ['Sprites/korwin/korwin2.png'],
                ['Sprites/korwin/korwin31.png', 'Sprites/korwin/korwin32.png'],
                ['Sprites/korwin/korwin41.png', 'Sprites/korwin/korwin42.png']
            ],
        }
        return random.choice(duck_image[self.duck_type])

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
        if self.duck_escaping:
            self.update_escape()
        elif self.alive:
            self.update_alive()
        else:
            self.update_dead()

    def update_alive(self):
        self.rect.left += self.velocity * self.direction[0]
        self.rect.top += self.velocity * self.direction[1]
        self.change_direction()
        if len(self.images) > 1:
            self.change_counter += 1
            if self.change_counter > 30:
                self.image_no = 1 - self.image_no
                self.image = self.images[self.image_no]
                self.change_counter = 0

    def update_dead(self):
        self.rect.top += self.velocity_dead
        if self.rect.bottom >= Subround.playground.bottom:
            self.duck_gone = True

    def update_escape(self):
        self.rect.top -= self.velocity_dead
        if self.rect.top <= Subround.playground.top:
            self.duck_gone = True

    def on_click(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.alive = False
            Game.score += self.get_point_value()

    def get_point_value(self):
        curr_round = Game.round_count
        if curr_round <= 5:
            point_values = {"ola": 500, "korwin": 500, "slawek": 1000, "janek": 1500, }
        elif curr_round <= 10:
            point_values = {"ola": 800, "korwin": 800, "slawek": 1500, "janek": 2400, }
        else:
            point_values = {"ola": 1000, "korwin": 1000, "slawek": 2000, "janek": 3000, }
        return point_values[self.duck_type]


class Subround:
    playground = pygame.Rect(0, 0, 599, 302)

    def __init__(self, i):
        self._running = True
        self.duck_count = 2
        self.shots_left = 3
        self.countdown = 10
        self.crosshair = Cursor()
        self.duck = Duck()
        self.dog = Dog(self.duck)
        self.ducks_shot = 0
        self.start_time = time.time()
        self.bullets = [Bullet(0), Bullet(1), Bullet(2)]
        self.sub_no = i

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
        Round.duck_goals[self.sub_no].update()
        time_to_shoot = -0.34 * Game.round_count + 11.16
        if not self.duck.alive:
            if self.duck.duck_gone:
                Round.duck_goals[self.sub_no].image = Round.duck_goals[self.sub_no].images[0]
                self.ducks_shot += 1
                self.subround_end('win')
        elif self.shots_left <= 0 or time.time() - self.start_time > time_to_shoot:
            self.duck.duck_escaping = True
            if self.duck.duck_gone:
                Round.duck_goals[self.sub_no].image = Round.duck_goals[self.sub_no].images[1]
                self.subround_end('loss')

    def on_render(self):
        GameBoard.render()
        GameBoard.display_surf.blit(self.duck.image, self.duck.rect)
        if self.duck.alive:
            GameBoard.display_surf.blit(self.crosshair.image, self.crosshair.rect)
        for i in range(self.shots_left):
            GameBoard.display_surf.blit(self.bullets[i].image, self.bullets[i].rect)
        for i in range(10):
            GameBoard.display_surf.blit(Round.duck_goals[i].image, Round.duck_goals[i].rect)
        if self.duck.duck_escaping:
            GameBoard.duck_fly_away()
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
        pygame.event.set_blocked(pygame.MOUSEBUTTONUP)

        while pygame.mixer.get_busy():
            time.sleep(0.1)
        pygame.event.set_allowed(pygame.MOUSEBUTTONUP)
        self._running = False


class Round:
    ROUNDS = 10
    duck_goals = []

    def __init__(self):
        self.ducks_shot = 0
        for i in range(10):
            self.duck_goals.append(GoalDuck(i))

    def execute(self):

        for i in range(self.ROUNDS):
            subround = Subround(i)
            self.ducks_shot += subround.on_execute()
        return self.end_round(self.ducks_shot >= Game.curr_min_duck_count)

    def end_round(self, is_win):
        if self.ducks_shot == self.ROUNDS:
            Game.score += self.perfect_bonus()
            GameBoard.perfect_bonus()
        pygame.display.update()
        time.sleep(1)
        return is_win

    @staticmethod
    def perfect_bonus():
        if Game.round_count <= 10:
            return 10000
        if Game.round_count <= 15:
            return 15000
        if Game.round_count <= 20:
            return 20000
        return 30000


class Game:
    round_count = 0
    _running = True
    curr_min_duck_count = 0
    score = 0

    def on_init(self):
        pygame.mixer.pre_init(22050, -16, 2, 1024)
        pygame.init()
        pygame.font.init()
        pygame.mixer.quit()
        pygame.mixer.init(22050, -16, 2, 1024)
        pygame.display.set_caption('Dudu Hunt')
        GameBoard.welcome()
        pygame.display.update()
        time.sleep(2)
        GameBoard.welcome2()
        pygame.display.update()
        time.sleep(2)
        GameBoard.welcome3()
        pygame.display.update()
        time.sleep(2)
        GameBoard.welcome_menu()
        pygame.display.update()
        return wait()

    def get_min_duck_count(self):
        if self.round_count <= 10:
            return 6
        if self.round_count <= 12:
            return 7
        if self.round_count <= 14:
            return 8
        if self.round_count <= 19:
            return 9
        return 10

    @staticmethod
    def cleanup():
        GameBoard.game_over()
        pygame.display.update()
        if wait():
            play_again = True
        else:
            play_again = False

    def render(self):
        GameBoard.render()

    def execute(self):
        if not self.on_init():
            self._running = False

        while self._running:
            Game.round_count += 1
            Game.curr_min_duck_count = self.get_min_duck_count()
            self.render()
            game_round = Round()
            round_result = game_round.execute()
            self._running = round_result
        self.cleanup()


if __name__ == "__main__":
    while play_again:
        theApp = Game()
        theApp.execute()
