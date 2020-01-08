import pygame
import sys, os

pygame.init()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname).convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def load_level(filename):
    filename = "data/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))
    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def generate_level(level):
    new_player, x, y = None, None, None
    xp = 0
    yp = 0
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '%':
                Tile('stair', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                xp = x
                yp = y
    new_player = Player(xp, yp)
    # вернем игрока, а также размер поля в клетках
    return new_player, x, y


def start_screen():
    # intro_text = ["B.U.L.L.E.T."]
    fon = pygame.transform.scale(load_image('fon2.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    # font = pygame.font.Font(None, 30)
    # text_coord = 50
    # for line in intro_text:
        # string_rendered = font.render(line, 1, pygame.Color('black'))
        # intro_rect = string_rendered.get_rect()
        # text_coord += 10
        # intro_rect.top = text_coord
        # intro_rect.x = 10
        # text_coord += intro_rect.height
        # screen.blit(string_rendered, intro_rect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)


def terminate():
    pygame.quit()
    sys.exit()


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)
        if tile_type == "wall":
            self.add(walls_group)
        if tile_type == "stair":
            self.add(stairs_group)

class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self):
        self.dx = 0
        self.dy = 0

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    # позиционировать камеру на объекте target
    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - WIDTH // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - HEIGHT // 2)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = pygame.transform.scale(player_image_static, (40, 80))
        self.rect = self.image.get_rect().move(tile_width * pos_x + 15, tile_height * pos_y + 5)
        self.ground = False
        self.definition = True
        self.vx = 10
        self.vfall = 0

    def update(self, key):
        global gravity
        if key[0] and self.ground:
            self.vfall = -20
            if pygame.sprite.spritecollideany(self, walls_group):
                self.rect.y += self.vfall
                # print(0)
            if not pygame.sprite.spritecollideany(self, stairs_group):
                self.ground = False
            self.picture()

        if key[1]:
            self.rect.x += self.vx
            if pygame.sprite.spritecollideany(self, walls_group):
                self.rect.x -= self.vx
                # print(1)
        if key[2]:
            self.rect.y += self.vx
            if pygame.sprite.spritecollideany(self, walls_group):
                self.rect.y -= self.vx
                # print(2)
                # self.ground = False
        if key[3]:
            self.rect.x -= self.vx
            if pygame.sprite.spritecollideany(self, walls_group):
                self.rect.x += self.vx
                # print(3)
        # self.picture()

    def picture(self, definition=None):
        if self.ground:
            self.image = pygame.transform.scale(player_image_static, (40, 80))
        else:
            self.image = pygame.transform.scale(player_image_jumping, (60, 60))
        if pygame.sprite.spritecollideany(self, stairs_group):
            self.image = pygame.transform.scale(player_image_climbing, (40, 80))
        if not self.definition:
            self.image = pygame.transform.flip(self.image, True, False)
        if definition is not None:
            if definition != self.definition:
                self.image = pygame.transform.flip(self.image, True, False)
                self.definition = definition

    def gravity(self):
        global gravity
        self.rect.y += self.vfall
        if pygame.sprite.spritecollideany(self, walls_group):
            if pygame.sprite.spritecollide(self, walls_group, False)[0].rect.y <= self.rect.y:
                while pygame.sprite.spritecollideany(self, walls_group):
                    self.rect.y += 1
            else:
                while pygame.sprite.spritecollideany(self, walls_group):
                    self.rect.y -= 1
                # gravity = 0
                # self.image = pygame.transform.scale(player_image_static, (40, 80))
                self.ground = True
            self.vfall = 0
            self.picture()
        else:
            self.picture()
            self.ground = False
            self.vfall += gravity
            # if self.vfall != 1:
                # self.image = pygame.transform.rotate(self.image, 10)
        if pygame.sprite.spritecollideany(self, stairs_group):
            self.ground = True
            # self.picture()
            gravity = 0
            self.vfall = 0
        else:
            gravity = 1
            # self.picture()


size = WIDTH, HEIGHT = 1000, 500
screen = pygame.display.set_mode(size)
screen.fill(pygame.Color('black'))
clock = pygame.time.Clock()
key = [False, False, False, False]
gravity = 1
FPS = 50
tile_images = {'wall': load_image('box.png'), 'stair': load_image('stair.png'), 'empty': load_image('fill1.png')}
player_image_static = load_image('hero.png', -1)
player_image_jumping = load_image('herojump.png', -1)
player_image_climbing = load_image('heroback.png', -1)
tile_width = tile_height = 50
# группы спрайтов
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
walls_group = pygame.sprite.Group()
stairs_group = pygame.sprite.Group()
camera = Camera()

start_screen()
player, level_x, level_y = generate_level(load_level('map.txt'))
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                key[0] = True
                # player.picture()
            if event.key == pygame.K_d:
                key[1] = True
                player.picture(True)
            if event.key == pygame.K_s:
                key[2] = True
            if event.key == pygame.K_a:
                key[3] = True
                player.picture(False)
            # print(key)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                key[0] = False
                # player.picture()
            if event.key == pygame.K_d:
                key[1] = False
            if event.key == pygame.K_s:
                key[2] = False
            if event.key == pygame.K_a:
                key[3] = False

            # print(key)
    player.gravity()
    player_group.update(key)


    # изменяем ракурс камеры
    camera.update(player)
    # обновляем положение всех спрайтов
    for sprite in all_sprites:
        camera.apply(sprite)
    screen.fill((0, 0, 0))
    all_sprites.draw(screen)
    pygame.display.flip()
    clock.tick(FPS)
pygame.quit()






