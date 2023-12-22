import pygame
from sys import exit
from player import Player
from enemy import Enemy
from rescued_people import RescuedPeeps
from rock_tile import Rock
from state import State
from pygame import mixer


class Game(State):
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.background_image = pygame.image.load('assets/trail1.png')
        self.background_image = pygame.transform.scale(
            self.background_image, (800, 600))
        self.clock = pygame.time.Clock()
        self.player = Player(400, 300)
        self.enemy = Enemy(150, 300, 150)
        self.rock = Rock(250, 300)
        self.rescuedpeeps = []
        self.paused = False
        self.setup_prisoners()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    self.pause()

    def setup_prisoners(self):
        self.rescuedpeeps.append(RescuedPeeps(
            50, 150, self, 'assets/sprites/peeps_sprite/Peeps-2.png.png'))
        self.rescuedpeeps.append(RescuedPeeps(
            50, 240, self, 'assets/sprites/peeps_sprite/Peeps-4.png.png'))
        self.rescuedpeeps.append(RescuedPeeps(
            50, 350, self, 'assets/sprites/peeps_sprite/Peeps-3.png.png'))
        self.rescuedpeeps.append(RescuedPeeps(
            50, 440, self, 'assets/sprites/peeps_sprite/Peeps-5.png.png'))

    def increase_enemy_difficulty(self):
        self.enemy.increase_difficulty()

    def update(self):
        peeps_to_remove = []

        if self.player.player_collision_rect.colliderect(self.enemy.enemy_collision_rect):
            State.currentPage = "GAMEOVER"

        elif not self.rescuedpeeps:
            print("You won")
            State.currentPage = "GAMEWON"

        if self.enemy.enemy_collision_rect.colliderect(self.rock.rock_collision_rect):
            self.enemy.send_to_guard_post()

        if self.player.player_collision_rect.colliderect(self.rock.rock_collision_rect):
            self.player.deplete_stamina()
        self.player.update(self.rock.rock_collision_rect)
        self.enemy.update(self.player.get_position().center)

        for peeps in self.rescuedpeeps:
            if not peeps.visible:
                peeps_to_remove.append(peeps)
            else:
                peeps.update(self.player.get_position())

        for peep in peeps_to_remove:
            self.rescuedpeeps.remove(peep)

    def draw(self):
        self.screen.blit(self.background_image, (0, 0))
        self.draw_sprites()

        for peeps in self.rescuedpeeps:
            peeps.draw(self.screen)

        pygame.display.update()

    def draw_sprites(self):
        drawables = [self.rock, self.enemy, self.player]
        drawables.sort(key=lambda x: x.get_position().centery, reverse=False)
        for drawable in drawables:
            drawable.draw(self.screen)
        # if (self.player.get_position().centery > self.enemy.get_position().centery):
        #     self.draw_order(self.enemy)
        #     self.draw_order(self.player)

        # else:
        #     self.draw_order(self.player)
        #     self.draw_order(self.enemy)

    def draw_order(self, surface):
        if surface.get_position().centery >= self.rock.get_position().centery:
            self.rock.draw(self.screen)
            self.rock.draw_collision_box(self.screen)
            surface.draw(self.screen)

        else:
            surface.draw(self.screen)
            self.rock.draw(self.screen)
            self.rock.draw_collision_box(self.screen)

    def run(self):
        while State.currentPage == "PLAY":
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)

    def pause(self):
        self.paused = True
        clock = pygame.time.Clock()
        pauseScreen = pygame.Surface((
            self.screen.get_width(), self.screen.get_height()))

        pauseScreen.fill((0, 0, 0))
        pauseScreen.set_alpha(120)

        pauseFont = pygame.font.Font('./assets/fonts/Pixeltype.ttf', 120)
        subFont = pygame.font.Font('./assets/fonts/Pixeltype.ttf', 65)

        pauseText = pauseFont.render("Paused", True, "white")
        pausePos = pauseText.get_rect(center=(self.screen.get_width()/2, 170))

        pressPText = subFont.render("Press 'P' to unpause", True, "white")
        pressPPos = pressPText.get_rect(
            center=(self.screen.get_width()/2, pausePos.bottom+40))

        self.screen.blit(pauseScreen, (0, 0))
        self.screen.blit(pauseText, pausePos)
        self.screen.blit(pressPText, pressPPos)

        while self.paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        self.paused = False
            pygame.display.update()

            clock.tick(60)
