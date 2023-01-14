import pygame
import sys
import random
import os


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk_1 = pygame.image.load(
            "img/player/walking_player_1.png"
        ).convert_alpha()
        player_walk_2 = pygame.image.load(
            "img/player/walking_player_2.png"
        ).convert_alpha()
        self.player_walk = [player_walk_1, player_walk_2]
        self.player_index = 0
        self.player_jump = pygame.image.load(
            "img/player/jumping_player.png"
        ).convert_alpha()

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom=(80, 300))
        self.gravity = 0

    def player_input(self):
        self.path = "audio/"
        self.all_wav = [
            os.path.join(self.path, f)
            for f in os.listdir(self.path)
            if f.endswith(".wav")
        ]
        self.rand_jump_sound = random.choice(self.all_wav)
        self.jump_sound = pygame.mixer.Sound(self.rand_jump_sound)
        self.jump_sound.set_volume(1.1)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20
            self.jump_sound.play()

    def apply_gravity(self):
        self.gravity += 1.15
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300

    def animation_state(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk):
                self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()

        if type == "bee":
            bee1 = pygame.image.load("img/bee/bee1.png").convert_alpha()
            self.frames = [bee1]
            y_pos = 210
        else:
            mushroom_1 = pygame.image.load("img/mushroom/mushroom1.png").convert_alpha()
            self.frames = [mushroom_1]
            y_pos = 300

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom=(random.randint(900, 1100), y_pos))

    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        self.animation_state()
        self.rect.x -= 6
        self.destroy()

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()


def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surf = test_font.render(f"ОЧКИ: {current_time}", False, (64, 64, 64))
    score_rect = score_surf.get_rect(center=(400, 50))
    screen.blit(score_surf, score_rect)
    return current_time


def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 5

            if obstacle_rect.bottom == 300:
                screen.blit(mushroom_surf, obstacle_rect)
            else:
                screen.blit(bee_surf, obstacle_rect)

        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]

        return obstacle_list
    else:
        return []


def collisions(player, obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect):
                return False
    return True


def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
        obstacle_group.empty()
        return False
    else:
        return True


def player_animation():
    global player_surf, player_index

    if player_rect.bottom < 300:
        player_surf = player_jump
    else:
        player_index += 0.1
        if player_index >= len(player_walk):
            player_index = 0
        player_surf = player_walk[int(player_index)]


pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption("Раннер")
clock = pygame.time.Clock()
test_font = pygame.font.Font("font/Pixeltype.ttf", 100)
game_active = False
start_time = 0
score = 0
highest_score = 0
bg_music = pygame.mixer.Sound("audio/music/main_music.wav")
bg_music.play(loops=-1)
bg_music.set_volume(0.7)

player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()

sky_surface = pygame.image.load("img/sky.png").convert()
ground_surface = pygame.image.load("img/ground.png").convert()

mushroom_frame_1 = pygame.image.load("img/mushroom/mushroom1.png").convert_alpha()
mushroom_frames = [mushroom_frame_1, mushroom_frame_1]
mushroom_frame_index = 0
mushroom_surf = mushroom_frames[mushroom_frame_index]

bee_frame1 = pygame.image.load("img/bee/bee1.png").convert_alpha()
bee_frames = [bee_frame1, bee_frame1]
bee_frame_index = 0
bee_surf = bee_frames[bee_frame_index]

obstacle_rect_list = []

player_walk_1 = pygame.image.load("img/player/walking_player_1.png").convert_alpha()
player_walk_2 = pygame.image.load("img/player/walking_player_2.png").convert_alpha()
player_walk = [player_walk_1, player_walk_2]
player_index = 0
player_jump = pygame.image.load("img/player/jumping_player.png").convert_alpha()

player_surf = player_walk[player_index]
player_rect = player_surf.get_rect(midbottom=(80, 300))
player_gravity = 0
player_stand = pygame.image.load("img/player/standing_player.png").convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
player_stand_rect = player_stand.get_rect(center=(400, 200))

game_name = test_font.render("Прыгалка", False, (96, 29, 205))
game_name_rect = game_name.get_rect(center=(400, 80))

game_message = test_font.render("Нажми пробел чтобы начать", False, (111, 196, 169))
game_message_rect = game_message.get_rect(center=(400, 330))
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)

mushroom_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(mushroom_animation_timer, 500)

bee_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(bee_animation_timer, 200)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if game_active:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if player_rect.collidepoint(event.pos) and player_rect.bottom >= 300:
                    player_gravity = -20

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom >= 300:
                    player_gravity = -20
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True

                start_time = int(pygame.time.get_ticks() / 1000)

        if game_active:
            if event.type == obstacle_timer:
                obstacle_group.add(
                    Obstacle(random.choice(["bee", "mushroom", "mushroom", "mushroom"]))
                )

            if event.type == mushroom_animation_timer:
                if mushroom_frame_index == 0:
                    mushroom_frame_index = 1
                else:
                    mushroom_frame_index = 0
                mushroom_surf = mushroom_frames[mushroom_frame_index]

            if event.type == bee_animation_timer:
                if bee_frame_index == 0:
                    bee_frame_index = 1
                else:
                    bee_frame_index = 0
                bee_surf = bee_frames[bee_frame_index]

    if game_active:
        screen.blit(sky_surface, (0, 0))
        screen.blit(ground_surface, (0, 300))
        score = display_score()

        player.draw(screen)
        player.update()

        obstacle_group.draw(screen)
        obstacle_group.update()

        game_active = collision_sprite()

    else:
        screen.fill((94, 129, 162))
        screen.blit(player_stand, player_stand_rect)
        obstacle_rect_list.clear()
        player_rect.midbottom = (80, 300)
        player_gravity = 0

        score_message = test_font.render(f"Ты набрал: {score}", False, (111, 196, 169))
        score_message_rect = score_message.get_rect(center=(400, 330))
        screen.blit(game_name, game_name_rect)

        if score == 0:
            screen.blit(game_message, game_message_rect)
        else:
            screen.blit(score_message, score_message_rect)

    pygame.display.update()
    clock.tick(60)
