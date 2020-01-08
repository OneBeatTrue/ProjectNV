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
            elif level[y][x] == '*':
                Tile('empty', x, y)
                new_button = Button(x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                xp = x
                yp = y
    new_player = Player(xp, yp)
    # вернем игрока, а также размер поля в клетках
    return new_player, x, y, new_button


def start_screen():
    play_text = ["S.T.A.R.T. G.A.M.E."]
    load_text = ["L.O.A.D. G.A.M.E."]
    options_text = ["O.P.T.I.O.N.S."]
    quit_text = ["Q.U.I.T."]
    fon = pygame.transform.scale(load_image('fon2.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    #pygame.draw.polygon(screen, pygame.Color('gray'), [(50, 150), (50, 200), (250, 200), (250, 150)])
    #pygame.draw.polygon(screen, pygame.Color('gray'), [(50, 210), (50, 260), (250, 260), (250, 210)])
    #pygame.draw.polygon(screen, pygame.Color('gray'), [(50, 270), (50, 320), (250, 320), (250, 270)])
    #pygame.draw.polygon(screen, pygame.Color('gray'), [(50, 330), (50, 380), (250, 380), (250, 330)])

    def update(*args):
        a = args[0][0]
        b = args[0][1]
        x1_1 = args[1][0]
        x2_1 = args[1][1]
        y1_1 = args[1][2]
        y2_1 = args[1][3]
        if x1_1 <= a <= x2_1 and y1_1 <= b <= y2_1:
            pygame.draw.polygon(screen, pygame.Color('red'), [(50, 150), (50, 200), (250, 200), (250, 150)])
            font = pygame.font.Font(None, 30)
            text_coord = 50
            for line in play_text:
                string_rendered = font.render(line, 1, pygame.Color('white'))
                intro_rect = string_rendered.get_rect()
                text_coord += 110
                intro_rect.top = text_coord
                intro_rect.x = 55
                text_coord += intro_rect.height
                screen.blit(string_rendered, intro_rect)
        else:
            pygame.draw.polygon(screen, pygame.Color('black'), [(50, 150), (50, 200), (250, 200), (250, 150)])
            font = pygame.font.Font(None, 30)
            text_coord = 50
            for line in play_text:
                string_rendered = font.render(line, 1, pygame.Color('white'))
                intro_rect = string_rendered.get_rect()
                text_coord += 110
                intro_rect.top = text_coord
                intro_rect.x = 55
                text_coord += intro_rect.height
                screen.blit(string_rendered, intro_rect)

        x1_2 = args[2][0]
        x2_2 = args[2][1]
        y1_2 = args[2][2]
        y2_2 = args[2][3]
        if x1_2 <= a <= x2_2 and y1_2 <= b <= y2_2:
            pygame.draw.polygon(screen, pygame.Color('red'), [(50, 210), (50, 260), (250, 260), (250, 210)])
            font = pygame.font.Font(None, 30)
            text_coord = 50
            for line in load_text:
                string_rendered = font.render(line, 1, pygame.Color('white'))
                intro_rect = string_rendered.get_rect()
                text_coord += 170
                intro_rect.top = text_coord
                intro_rect.x = 55
                text_coord += intro_rect.height
                screen.blit(string_rendered, intro_rect)
        else:
            pygame.draw.polygon(screen, pygame.Color('black'), [(50, 210), (50, 260), (250, 260), (250, 210)])
            font = pygame.font.Font(None, 30)
            text_coord = 50
            for line in load_text:
                string_rendered = font.render(line, 1, pygame.Color('white'))
                intro_rect = string_rendered.get_rect()
                text_coord += 170
                intro_rect.top = text_coord
                intro_rect.x = 55
                text_coord += intro_rect.height
                screen.blit(string_rendered, intro_rect)

        x1_3 = args[3][0]
        x2_3 = args[3][1]
        y1_3 = args[3][2]
        y2_3 = args[3][3]
        if x1_3 <= a <= x2_3 and y1_3 <= b <= y2_3:
            pygame.draw.polygon(screen, pygame.Color('red'), [(50, 270), (50, 320), (250, 320), (250, 270)])
            font = pygame.font.Font(None, 30)
            text_coord = 50
            for line in options_text:
                string_rendered = font.render(line, 1, pygame.Color('white'))
                intro_rect = string_rendered.get_rect()
                text_coord += 230
                intro_rect.top = text_coord
                intro_rect.x = 55
                text_coord += intro_rect.height
                screen.blit(string_rendered, intro_rect)
        else:
            pygame.draw.polygon(screen, pygame.Color('black'), [(50, 270), (50, 320), (250, 320), (250, 270)])
            font = pygame.font.Font(None, 30)
            text_coord = 50
            for line in options_text:
                string_rendered = font.render(line, 1, pygame.Color('white'))
                intro_rect = string_rendered.get_rect()
                text_coord += 230
                intro_rect.top = text_coord
                intro_rect.x = 55
                text_coord += intro_rect.height
                screen.blit(string_rendered, intro_rect)

        x1_4 = args[4][0]
        x2_4 = args[4][1]
        y1_4 = args[4][2]
        y2_4 = args[4][3]
        if x1_4 <= a <= x2_4 and y1_4 <= b <= y2_4:
            pygame.draw.polygon(screen, pygame.Color('red'), [(50, 330), (50, 380), (250, 380), (250, 330)])
            font = pygame.font.Font(None, 30)
            text_coord = 50
            for line in quit_text:
                string_rendered = font.render(line, 1, pygame.Color('white'))
                intro_rect = string_rendered.get_rect()
                text_coord += 290
                intro_rect.top = text_coord
                intro_rect.x = 55
                text_coord += intro_rect.height
                screen.blit(string_rendered, intro_rect)
        else:
            pygame.draw.polygon(screen, pygame.Color('black'), [(50, 330), (50, 380), (250, 380), (250, 330)])
            font = pygame.font.Font(None, 30)
            text_coord = 50
            for line in quit_text:
                string_rendered = font.render(line, 1, pygame.Color('white'))
                intro_rect = string_rendered.get_rect()
                text_coord += 290
                intro_rect.top = text_coord
                intro_rect.x = 55
                text_coord += intro_rect.height
                screen.blit(string_rendered, intro_rect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
            if event.type == pygame.MOUSEMOTION:
                update(event.pos, [50, 250, 150, 200], [50, 250, 210, 260], [50, 250, 270, 320], [50, 250, 330, 380])
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

class Button(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(button_group, all_sprites)
        self.image = button_image_unclicked
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)

    def update(self):
        if pygame.sprite.spritecollideany(self, player_group):
            self.image = button_image_clicked


class Arrow(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.image = pygame.transform.scale(arrow_image, (40, 40))
        self.rect = self.image.get_rect()


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
        # self.rect = self.image.get_rect().move(tile_width * self.rect.x + 15, tile_height * self.rect.y + 5)

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
# pygame.mouse.set_visible(False)
screen.fill(pygame.Color('black'))
clock = pygame.time.Clock()
key = [False, False, False, False]
gravity = 1
FPS = 50
tile_images = {'wall': load_image('box.png'), 'stair': load_image('stair.png'), 'empty': load_image('grass.png')}
player_image_static = load_image('hero.png', -1)
player_image_jumping = load_image('herojump.png', -1)
player_image_climbing = load_image('heroback.png', -1)
button_image_unclicked = load_image('button1.png', -1)
button_image_clicked = load_image('button2.png', -1)
arrow_image = load_image("arrow.png")
arrow = Arrow(0, 0)
tile_width = tile_height = 50
# группы спрайтов
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
walls_group = pygame.sprite.Group()
stairs_group = pygame.sprite.Group()
button_group = pygame.sprite.Group()
camera = Camera()

start_screen()
player, level_x, level_y, button = generate_level(load_level('map.txt'))
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
        if event.type == pygame.MOUSEMOTION:
            x, y = event.pos
            arrow.rect.x = x
            arrow.rect.y = y
            # print(key)
    player.gravity()
    player_group.update(key)
    button_group.update()

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






