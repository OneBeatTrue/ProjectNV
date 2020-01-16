import pygame, sys, os, random
from os import path

pygame.init()
size = WIDTH, HEIGHT = 1600, 900
# size = WIDTH, HEIGHT = 1280, 1024
# screen = pygame.display.set_mode(size)
screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
# pygame.mouse.set_visible(False)
screen.fill(pygame.Color('black'))


def create_particles(position, sprite=None):
    # количество создаваемых частиц
    particle_count = 100
    # возможные скорости
    for i in range(particle_count):
        if i == particle_count - 1 and sprite is not None:
            Particle(position, random.choice(range(-4, 4)), random.choice(range(-10, 2)), sprite)
        else:
            Particle(position, random.choice(range(-4, 4)), random.choice(range(-10, 2)))


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
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    # max_width = max(map(len, level_map))
    return level_map


def generate_level(level):
    global player_image_static, player_image_jumping, player_image_climbing
    new_player, x, y = None, None, None
    xp = 0
    yp = 0
    xb = 0
    yb = 0
    doors = list()
    enemies = list()
    peaks = list()
    boss = None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '_':
                Tile('space', x, y)
            elif level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '%':
                Tile('stair', x, y)
            elif level[y][x] == '^':
                Tile('empty', x, y)
                peaks.append([x, y])
            elif level[y][x] == '*':
                Tile('empty', x, y)
                button = Button(x, y)
            elif level[y][x] == ')':
                Tile('empty', x, y)
                enemies.append([x, y, True])
            elif level[y][x] == '&':
                Tile('empty', x, y)
                xb = x
                yb = y
            elif level[y][x] == '(':
                Tile('empty', x, y)
                enemies.append([x, y, False])
            elif level[y][x] == '>':
                doors.append(Door(x, y, True))
            elif level[y][x] == '<':
                doors.append(Door(x, y, False))
            elif level[y][x] == '@':
                Tile('empty', x, y)
                xp = x
                yp = y
    enemies = [Enemy(i[0], i[1], i[2]) for i in enemies]
    peaks = [Peak(i[0], i[1]) for i in peaks]
    if xb != 0 and  yb != 0:
        boss = Boss(xb, yb)
    new_player = Player(xp, yp)
    player_image_static = load_image('hero.png', -1)
    player_image_jumping = load_image('herojump.png', -1)
    player_image_climbing = load_image('heroback.png', -1)
    pygame.mixer.music.stop()
    pygame.mixer.music.load(tracklist[now_level])
    pygame.mixer.music.play(loops=-1)
    return new_player, enemies, boss, peaks, x, y, button, doors, False


def clean():
    global player, enemies, boss, peaks, level_x, level_y, button, doors, next_level, key, alive, event_counter # , check_cam
    for i in all_sprites:
        all_sprites.remove(i)
        i.kill()
    event_counter = 0
    key = [False, False, False, False]
    alive = True
    print(now_level)
    player, enemies, boss, peaks, level_x, level_y, button, doors, next_level = generate_level(load_level(levels_list[now_level]))


with open("data/options.txt", 'r') as f:
    dop = str([line.strip() for line in f][0])
    volume = int(dop[0])
    blood = int(dop[1])


def start_screen(volume_restart=None):
    global volume, blood
    play_text = ["S.T.A.R.T. G.A.M.E."]
    load_text = ["L.O.A.D. G.A.M.E."]
    options_text = ["O.P.T.I.O.N.S."]
    quit_text = ["Q.U.I.T."]
    fon = pygame.transform.scale(load_image('fon2.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    if volume_restart is None:
        pygame.mixer.music.stop()
        pygame.mixer.music.load(tracklist[3])
        pygame.mixer.music.play(loops=-1)
    if volume == 1:
        pygame.mixer.music.set_volume(0.0)
    pygame.draw.polygon(screen, pygame.Color('black'), [(50, 250), (50, 300), (250, 300), (250, 250)])
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in play_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 210
        intro_rect.top = text_coord
        intro_rect.x = 55
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    pygame.draw.polygon(screen, pygame.Color('black'), [(50, 310), (50, 360), (250, 360), (250, 310)])
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in load_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 270
        intro_rect.top = text_coord
        intro_rect.x = 55
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    pygame.draw.polygon(screen, pygame.Color('black'), [(50, 370), (50, 420), (250, 420), (250, 370)])
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in options_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 330
        intro_rect.top = text_coord
        intro_rect.x = 55
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    pygame.draw.polygon(screen, pygame.Color('black'), [(50, 430), (50, 480), (250, 480), (250, 430)])
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in quit_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 390
        intro_rect.top = text_coord
        intro_rect.x = 55
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    def update(*args):
        global flag
        flag = 0
        a = args[0][0]
        b = args[0][1]
        x1_1 = args[1][0]
        x2_1 = args[1][1]
        y1_1 = args[1][2]
        y2_1 = args[1][3]
        if x1_1 <= a <= x2_1 and y1_1 <= b <= y2_1:
            flag = 1
            pygame.draw.polygon(screen, pygame.Color('red'), [(50, 250), (50, 300), (250, 300), (250, 250)])
            font = pygame.font.Font(None, 30)
            text_coord = 50
            for line in play_text:
                string_rendered = font.render(line, 1, pygame.Color('white'))
                intro_rect = string_rendered.get_rect()
                text_coord += 210
                intro_rect.top = text_coord
                intro_rect.x = 55
                text_coord += intro_rect.height
                screen.blit(string_rendered, intro_rect)
        else:
            pygame.draw.polygon(screen, pygame.Color('black'), [(50, 250), (50, 300), (250, 300), (250, 250)])
            font = pygame.font.Font(None, 30)
            text_coord = 50
            for line in play_text:
                string_rendered = font.render(line, 1, pygame.Color('white'))
                intro_rect = string_rendered.get_rect()
                text_coord += 210
                intro_rect.top = text_coord
                intro_rect.x = 55
                text_coord += intro_rect.height
                screen.blit(string_rendered, intro_rect)
        x1_2 = args[2][0]
        x2_2 = args[2][1]
        y1_2 = args[2][2]
        y2_2 = args[2][3]
        if x1_2 <= a <= x2_2 and y1_2 <= b <= y2_2:
            flag = 2
            pygame.draw.polygon(screen, pygame.Color('red'), [(50, 310), (50, 360), (250, 360), (250, 310)])
            font = pygame.font.Font(None, 30)
            text_coord = 50
            for line in load_text:
                string_rendered = font.render(line, 1, pygame.Color('white'))
                intro_rect = string_rendered.get_rect()
                text_coord += 270
                intro_rect.top = text_coord
                intro_rect.x = 55
                text_coord += intro_rect.height
                screen.blit(string_rendered, intro_rect)
        else:
            pygame.draw.polygon(screen, pygame.Color('black'), [(50, 310), (50, 360), (250, 360), (250, 310)])
            font = pygame.font.Font(None, 30)
            text_coord = 50
            for line in load_text:
                string_rendered = font.render(line, 1, pygame.Color('white'))
                intro_rect = string_rendered.get_rect()
                text_coord += 270
                intro_rect.top = text_coord
                intro_rect.x = 55
                text_coord += intro_rect.height
                screen.blit(string_rendered, intro_rect)
        x1_3 = args[3][0]
        x2_3 = args[3][1]
        y1_3 = args[3][2]
        y2_3 = args[3][3]
        if x1_3 <= a <= x2_3 and y1_3 <= b <= y2_3:
            flag = 3
            pygame.draw.polygon(screen, pygame.Color('red'), [(50, 370), (50, 420), (250, 420), (250, 370)])
            font = pygame.font.Font(None, 30)
            text_coord = 50
            for line in options_text:
                string_rendered = font.render(line, 1, pygame.Color('white'))
                intro_rect = string_rendered.get_rect()
                text_coord += 330
                intro_rect.top = text_coord
                intro_rect.x = 55
                text_coord += intro_rect.height
                screen.blit(string_rendered, intro_rect)
        else:
            pygame.draw.polygon(screen, pygame.Color('black'), [(50, 370), (50, 420), (250, 420), (250, 370)])
            font = pygame.font.Font(None, 30)
            text_coord = 50
            for line in options_text:
                string_rendered = font.render(line, 1, pygame.Color('white'))
                intro_rect = string_rendered.get_rect()
                text_coord += 330
                intro_rect.top = text_coord
                intro_rect.x = 55
                text_coord += intro_rect.height
                screen.blit(string_rendered, intro_rect)
        x1_4 = args[4][0]
        x2_4 = args[4][1]
        y1_4 = args[4][2]
        y2_4 = args[4][3]
        if x1_4 <= a <= x2_4 and y1_4 <= b <= y2_4:
            flag = 4
            pygame.draw.polygon(screen, pygame.Color('red'), [(50, 430), (50, 480), (250, 480), (250, 430)])
            font = pygame.font.Font(None, 30)
            text_coord = 50
            for line in quit_text:
                string_rendered = font.render(line, 1, pygame.Color('white'))
                intro_rect = string_rendered.get_rect()
                text_coord += 390
                intro_rect.top = text_coord
                intro_rect.x = 55
                text_coord += intro_rect.height
                screen.blit(string_rendered, intro_rect)
        else:
            pygame.draw.polygon(screen, pygame.Color('black'), [(50, 430), (50, 480), (250, 480), (250, 430)])
            font = pygame.font.Font(None, 30)
            text_coord = 50
            for line in quit_text:
                string_rendered = font.render(line, 1, pygame.Color('white'))
                intro_rect = string_rendered.get_rect()
                text_coord += 390
                intro_rect.top = text_coord
                intro_rect.x = 55
                text_coord += intro_rect.height
                screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                with open("data/options.txt", 'w', encoding='utf-8') as f:
                    f.write(str(volume) + str(blood))
                with open("data/now_level.txt", 'w', encoding='utf-8') as f:
                    f.write(str(now_level))
                terminate()
            if event.type == pygame.MOUSEMOTION:
                update(event.pos, [50, 250, 250, 300], [50, 250, 310, 360], [50, 250, 370, 420], [50, 250, 430, 480])
                x, y = event.pos
                arrow.update(x, y)
            if event.type == pygame.MOUSEBUTTONDOWN and flag == 1 or event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                clean()
                return
            if event.type == pygame.MOUSEBUTTONDOWN and flag == 4:
                with open("data/options.txt", 'w', encoding='utf-8') as f:
                    f.write(str(volume) + str(blood))
                with open("data/now_level.txt", 'w', encoding='utf-8') as f:
                    f.write(str(now_level))
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN and flag == 3:
                options()
                return
            if event.type == pygame.MOUSEBUTTONDOWN and flag == 2:
                load()
                return
        pygame.display.flip()
        clock.tick(FPS)


def options():
    opt_text = ["<.B.A.C.K."]
    global volume
    global blood
    if volume == 1:
        volume_text = ["V.O.L.U.M.E. O.F.F."]
    else:
        volume_text = ["V.O.L.U.M.E. O.N."]

    if blood == 1:
        blood_text = ["B.L.O.O.D. O.F.F."]
    else:
        blood_text = ["B.L.O.O.D. O.N."]
    fon = pygame.transform.scale(load_image('opt_fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    pygame.draw.polygon(screen, pygame.Color('black'), [(50, 250), (50, 300), (250, 300), (250, 250)])
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in opt_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 210
        intro_rect.top = text_coord
        intro_rect.x = 55
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    pygame.draw.polygon(screen, pygame.Color('black'), [(50, 310), (50, 360), (250, 360), (250, 310)])
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in volume_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 270
        intro_rect.top = text_coord
        intro_rect.x = 55
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    pygame.draw.polygon(screen, pygame.Color('black'), [(50, 370), (50, 420), (250, 420), (250, 370)])
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in blood_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 330
        intro_rect.top = text_coord
        intro_rect.x = 55
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    def update(*args):
        global flag1
        global volume
        global volume_text
        global blood
        if volume == 1:
            volume_text = ["V.O.L.U.M.E. O.F.F."]
        else:
            volume_text = ["V.O.L.U.M.E. O.N."]

        if blood == 1:
            blood_text = ["B.L.O.O.D. O.F.F."]
        else:
            blood_text = ["B.L.O.O.D. O.N."]
        flag1 = 0
        a = args[0][0]
        b = args[0][1]
        x1_1 = args[1][0]
        x2_1 = args[1][1]
        y1_1 = args[1][2]
        y2_1 = args[1][3]
        if x1_1 <= a <= x2_1 and y1_1 <= b <= y2_1:
            flag1 = 1
            pygame.draw.polygon(screen, pygame.Color('red'), [(50, 250), (50, 300), (250, 300), (250, 250)])
            font = pygame.font.Font(None, 30)
            text_coord = 50
            for line in opt_text:
                string_rendered = font.render(line, 1, pygame.Color('white'))
                intro_rect = string_rendered.get_rect()
                text_coord += 210
                intro_rect.top = text_coord
                intro_rect.x = 55
                text_coord += intro_rect.height
                screen.blit(string_rendered, intro_rect)
        else:
            pygame.draw.polygon(screen, pygame.Color('black'), [(50, 250), (50, 300), (250, 300), (250, 250)])
            font = pygame.font.Font(None, 30)
            text_coord = 50
            for line in opt_text:
                string_rendered = font.render(line, 1, pygame.Color('white'))
                intro_rect = string_rendered.get_rect()
                text_coord += 210
                intro_rect.top = text_coord
                intro_rect.x = 55
                text_coord += intro_rect.height
                screen.blit(string_rendered, intro_rect)
        x1_2 = args[2][0]
        x2_2 = args[2][1]
        y1_2 = args[2][2]
        y2_2 = args[2][3]
        if x1_2 <= a <= x2_2 and y1_2 <= b <= y2_2:
            flag1 = 2
            pygame.draw.polygon(screen, pygame.Color('red'), [(50, 310), (50, 360), (250, 360), (250, 310)])
            font = pygame.font.Font(None, 30)
            text_coord = 50
            for line in volume_text:
                string_rendered = font.render(line, 1, pygame.Color('white'))
                intro_rect = string_rendered.get_rect()
                text_coord += 270
                intro_rect.top = text_coord
                intro_rect.x = 55
                text_coord += intro_rect.height
                screen.blit(string_rendered, intro_rect)
        else:
            pygame.draw.polygon(screen, pygame.Color('black'), [(50, 310), (50, 360), (250, 360), (250, 310)])
            font = pygame.font.Font(None, 30)
            text_coord = 50
            for line in volume_text:
                string_rendered = font.render(line, 1, pygame.Color('white'))
                intro_rect = string_rendered.get_rect()
                text_coord += 270
                intro_rect.top = text_coord
                intro_rect.x = 55
                text_coord += intro_rect.height
                screen.blit(string_rendered, intro_rect)
        x1_3 = args[3][0]
        x2_3 = args[3][1]
        y1_3 = args[3][2]
        y2_3 = args[3][3]
        if x1_3 <= a <= x2_3 and y1_3 <= b <= y2_3:
            flag1 = 3
            pygame.draw.polygon(screen, pygame.Color('red'), [(50, 370), (50, 420), (250, 420), (250, 370)])
            font = pygame.font.Font(None, 30)
            text_coord = 50
            for line in blood_text:
                string_rendered = font.render(line, 1, pygame.Color('white'))
                intro_rect = string_rendered.get_rect()
                text_coord += 330
                intro_rect.top = text_coord
                intro_rect.x = 55
                text_coord += intro_rect.height
                screen.blit(string_rendered, intro_rect)
        else:
            pygame.draw.polygon(screen, pygame.Color('black'), [(50, 370), (50, 420), (250, 420), (250, 370)])
            font = pygame.font.Font(None, 30)
            text_coord = 50
            for line in blood_text:
                string_rendered = font.render(line, 1, pygame.Color('white'))
                intro_rect = string_rendered.get_rect()
                text_coord += 330
                intro_rect.top = text_coord
                intro_rect.x = 55
                text_coord += intro_rect.height
                screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                with open("data/options.txt", 'w', encoding='utf-8') as f:
                    # print(str(volume) + str(blood))
                    f.write(str(volume) + str(blood))
                with open("data/now_level.txt", 'w', encoding='utf-8') as f:
                    # print(str(volume) + str(blood))
                    f.write(str(now_level))
                terminate()
            if event.type == pygame.MOUSEMOTION:
                update(event.pos, [50, 250, 250, 300], [50, 250, 310, 360], [50, 250, 370, 420])
                x, y = event.pos
                arrow.update(x, y)
            if event.type == pygame.MOUSEBUTTONDOWN and flag1 == 1:
                start_screen(False)
                return

            if event.type == pygame.MOUSEBUTTONDOWN and flag1 == 2:
                if volume == 0:
                    vol = 0.0
                    volume = 1
                else:
                    vol = 0.5
                    volume = 0
                pygame.mixer.music.set_volume(abs(0.0 - vol))
                update(event.pos, [50, 250, 250, 300], [50, 250, 310, 360], [50, 250, 370, 420])
            if event.type == pygame.MOUSEBUTTONDOWN and flag1 == 3:
                if blood == 0:
                    blood = 1
                else:
                    blood = 0
                update(event.pos, [50, 250, 250, 300], [50, 250, 310, 360], [50, 250, 370, 420])
        pygame.display.flip()
        clock.tick(FPS)


flag3 = 0
exit = 0


def menu():
    opt_text = ["<.B.A.C.K."]
    global volume
    global blood
    global exit
    if volume == 1:
        volume_text = ["V.O.L.U.M.E. O.F.F."]
    else:
        volume_text = ["V.O.L.U.M.E. O.N."]
    if blood == 1:
        blood_text = ["B.L.O.O.D. O.F.F."]
    else:
        blood_text = ["B.L.O.O.D. O.N."]
    restart_text = ["<.R.E.T.R.Y."]
    exit_text = ["E.X.I.T"]
    fon = pygame.transform.scale(load_image('menu_fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    pygame.draw.polygon(screen, pygame.Color('black'), [(50, 250), (50, 300), (250, 300), (250, 250)])
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in opt_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 210
        intro_rect.top = text_coord
        intro_rect.x = 55
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    pygame.draw.polygon(screen, pygame.Color('black'), [(50, 310), (50, 360), (250, 360), (250, 310)])
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in volume_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 270
        intro_rect.top = text_coord
        intro_rect.x = 55
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    pygame.draw.polygon(screen, pygame.Color('black'), [(50, 370), (50, 420), (250, 420), (250, 370)])
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in blood_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 330
        intro_rect.top = text_coord
        intro_rect.x = 55
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    pygame.draw.polygon(screen, pygame.Color('black'), [(50, 430), (50, 480), (250, 480), (250, 430)])
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in exit_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 390
        intro_rect.top = text_coord
        intro_rect.x = 55
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    pygame.draw.polygon(screen, pygame.Color('black'), [(50, 490), (50, 540), (250, 540), (250, 490)])
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in restart_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 450
        intro_rect.top = text_coord
        intro_rect.x = 55
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    def update(*args):
        global flag3
        global volume
        global volume_text
        global blood
        if volume == 1:
            volume_text = ["V.O.L.U.M.E. O.F.F."]
        else:
            volume_text = ["V.O.L.U.M.E. O.N."]

        if blood == 1:
            blood_text = ["B.L.O.O.D. O.F.F."]
        else:
            blood_text = ["B.L.O.O.D. O.N."]
        flag3 = 0
        a = args[0][0]
        b = args[0][1]
        x1_1 = args[1][0]
        x2_1 = args[1][1]
        y1_1 = args[1][2]
        y2_1 = args[1][3]
        if x1_1 <= a <= x2_1 and y1_1 <= b <= y2_1:
            flag3 = 1
            pygame.draw.polygon(screen, pygame.Color('red'), [(50, 250), (50, 300), (250, 300), (250, 250)])
            font = pygame.font.Font(None, 30)
            text_coord = 50
            for line in opt_text:
                string_rendered = font.render(line, 1, pygame.Color('white'))
                intro_rect = string_rendered.get_rect()
                text_coord += 210
                intro_rect.top = text_coord
                intro_rect.x = 55
                text_coord += intro_rect.height
                screen.blit(string_rendered, intro_rect)
        else:
            pygame.draw.polygon(screen, pygame.Color('black'), [(50, 250), (50, 300), (250, 300), (250, 250)])
            font = pygame.font.Font(None, 30)
            text_coord = 50
            for line in opt_text:
                string_rendered = font.render(line, 1, pygame.Color('white'))
                intro_rect = string_rendered.get_rect()
                text_coord += 210
                intro_rect.top = text_coord
                intro_rect.x = 55
                text_coord += intro_rect.height
                screen.blit(string_rendered, intro_rect)
        x1_2 = args[2][0]
        x2_2 = args[2][1]
        y1_2 = args[2][2]
        y2_2 = args[2][3]
        if x1_2 <= a <= x2_2 and y1_2 <= b <= y2_2:
            flag3 = 2
            pygame.draw.polygon(screen, pygame.Color('red'), [(50, 310), (50, 360), (250, 360), (250, 310)])
            font = pygame.font.Font(None, 30)
            text_coord = 50
            for line in volume_text:
                string_rendered = font.render(line, 1, pygame.Color('white'))
                intro_rect = string_rendered.get_rect()
                text_coord += 270
                intro_rect.top = text_coord
                intro_rect.x = 55
                text_coord += intro_rect.height
                screen.blit(string_rendered, intro_rect)
        else:
            pygame.draw.polygon(screen, pygame.Color('black'), [(50, 310), (50, 360), (250, 360), (250, 310)])
            font = pygame.font.Font(None, 30)
            text_coord = 50
            for line in volume_text:
                string_rendered = font.render(line, 1, pygame.Color('white'))
                intro_rect = string_rendered.get_rect()
                text_coord += 270
                intro_rect.top = text_coord
                intro_rect.x = 55
                text_coord += intro_rect.height
                screen.blit(string_rendered, intro_rect)
        x1_3 = args[3][0]
        x2_3 = args[3][1]
        y1_3 = args[3][2]
        y2_3 = args[3][3]
        if x1_3 <= a <= x2_3 and y1_3 <= b <= y2_3:
            flag3 = 3
            pygame.draw.polygon(screen, pygame.Color('red'), [(50, 370), (50, 420), (250, 420), (250, 370)])
            font = pygame.font.Font(None, 30)
            text_coord = 50
            for line in blood_text:
                string_rendered = font.render(line, 1, pygame.Color('white'))
                intro_rect = string_rendered.get_rect()
                text_coord += 330
                intro_rect.top = text_coord
                intro_rect.x = 55
                text_coord += intro_rect.height
                screen.blit(string_rendered, intro_rect)
        else:
            pygame.draw.polygon(screen, pygame.Color('black'), [(50, 370), (50, 420), (250, 420), (250, 370)])
            font = pygame.font.Font(None, 30)
            text_coord = 50
            for line in blood_text:
                string_rendered = font.render(line, 1, pygame.Color('white'))
                intro_rect = string_rendered.get_rect()
                text_coord += 330
                intro_rect.top = text_coord
                intro_rect.x = 55
                text_coord += intro_rect.height
                screen.blit(string_rendered, intro_rect)
        x1_4 = args[4][0]
        x2_4 = args[4][1]
        y1_4 = args[4][2]
        y2_4 = args[4][3]
        if x1_4 <= a <= x2_4 and y1_4 <= b <= y2_4:
            flag3 = 4
            pygame.draw.polygon(screen, pygame.Color('red'), [(50, 430), (50, 480), (250, 480), (250, 430)])
            font = pygame.font.Font(None, 30)
            text_coord = 50
            for line in exit_text:
                string_rendered = font.render(line, 1, pygame.Color('white'))
                intro_rect = string_rendered.get_rect()
                text_coord += 390
                intro_rect.top = text_coord
                intro_rect.x = 55
                text_coord += intro_rect.height
                screen.blit(string_rendered, intro_rect)
        else:
            pygame.draw.polygon(screen, pygame.Color('black'), [(50, 430), (50, 480), (250, 480), (250, 430)])
            font = pygame.font.Font(None, 30)
            text_coord = 50
            for line in exit_text:
                string_rendered = font.render(line, 1, pygame.Color('white'))
                intro_rect = string_rendered.get_rect()
                text_coord += 390
                intro_rect.top = text_coord
                intro_rect.x = 55
                text_coord += intro_rect.height
                screen.blit(string_rendered, intro_rect)
        x1_5 = args[5][0]
        x2_5 = args[5][1]
        y1_5 = args[5][2]
        y2_5 = args[5][3]
        if x1_5 <= a <= x2_5 and y1_5 <= b <= y2_5:
            flag3 = 5
            pygame.draw.polygon(screen, pygame.Color('red'), [(50, 490), (50, 540), (250, 540), (250, 490)])
            font = pygame.font.Font(None, 30)
            text_coord = 50
            for line in restart_text:
                string_rendered = font.render(line, 1, pygame.Color('white'))
                intro_rect = string_rendered.get_rect()
                text_coord += 450
                intro_rect.top = text_coord
                intro_rect.x = 55
                text_coord += intro_rect.height
                screen.blit(string_rendered, intro_rect)
        else:
            pygame.draw.polygon(screen, pygame.Color('black'), [(50, 490), (50, 540), (250, 540), (250, 490)])
            font = pygame.font.Font(None, 30)
            text_coord = 50
            for line in restart_text:
                string_rendered = font.render(line, 1, pygame.Color('white'))
                intro_rect = string_rendered.get_rect()
                text_coord += 450
                intro_rect.top = text_coord
                intro_rect.x = 55
                text_coord += intro_rect.height
                screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                with open("data/options.txt", 'w', encoding='utf-8') as f:
                    f.write(str(volume) + str(blood))
                with open("data/now_level.txt", 'w', encoding='utf-8') as f:
                    f.write(str(now_level))
                terminate()
            if event.type == pygame.MOUSEMOTION:
                update(event.pos, [50, 250, 250, 300], [50, 250, 310, 360], [50, 250, 370, 420], [50, 250, 430, 480], [50, 250, 490, 540])
                x, y = event.pos
                arrow.update(x, y)
            if (event.type == pygame.MOUSEBUTTONDOWN and flag3 == 1) or event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
                return
            if event.type == pygame.MOUSEBUTTONDOWN and flag3 == 2:
                if volume == 0:
                    vol = 0.0
                    volume = 1
                else:
                    vol = 0.5
                    volume = 0
                pygame.mixer.music.set_volume(abs(0.0 - vol))
                update(event.pos, [50, 250, 250, 300], [50, 250, 310, 360], [50, 250, 370, 420], [50, 250, 430, 480], [50, 250, 490, 540])
            if event.type == pygame.MOUSEBUTTONDOWN and flag3 == 3:
                if blood == 0:
                    blood = 1
                else:
                    blood = 0
                update(event.pos, [50, 250, 250, 300], [50, 250, 310, 360], [50, 250, 370, 420], [50, 250, 430, 480], [50, 250, 490, 540])
            if event.type == pygame.MOUSEBUTTONDOWN and flag3 == 4:
                exit = 1
                start_screen()
                return
            if event.type == pygame.MOUSEBUTTONDOWN and flag3 == 5 or event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                clean()
                return
        pygame.display.flip()
        clock.tick(FPS)


flag2 = 0
with open("data/pass_levels.txt", 'r') as f:
    level = int([line.strip() for line in f][0])
update_level = not level == 3


def load():
    global flag2
    global level
    global now_level
    load_text = ["<.B.A.C.K."]
    l1_text = ["L.E.V.E.L. 1."]
    l2_text = ["L.E.V.E.L. 2."]
    l3_text = ["L.E.V.E.L. 3."]
    fon = pygame.transform.scale(load_image('load_fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    pygame.draw.polygon(screen, pygame.Color('black'), [(50, 250), (50, 300), (250, 300), (250, 250)])
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in load_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 210
        intro_rect.top = text_coord
        intro_rect.x = 55
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    if level >= 1:
        pygame.draw.polygon(screen, pygame.Color('black'), [(50, 310), (50, 360), (250, 360), (250, 310)])
        font = pygame.font.Font(None, 30)
        text_coord = 50
        for line in l1_text:
            string_rendered = font.render(line, 1, pygame.Color('white'))
            intro_rect = string_rendered.get_rect()
            text_coord += 270
            intro_rect.top = text_coord
            intro_rect.x = 55
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)
    if level >= 2:
        pygame.draw.polygon(screen, pygame.Color('black'), [(50, 370), (50, 420), (250, 420), (250, 370)])
        font = pygame.font.Font(None, 30)
        text_coord = 50
        for line in l2_text:
            string_rendered = font.render(line, 1, pygame.Color('white'))
            intro_rect = string_rendered.get_rect()
            text_coord += 330
            intro_rect.top = text_coord
            intro_rect.x = 55
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)
    if level >= 3:
        pygame.draw.polygon(screen, pygame.Color('black'), [(50, 430), (50, 480), (250, 480), (250, 430)])
        font = pygame.font.Font(None, 30)
        text_coord = 50
        for line in l3_text:
            string_rendered = font.render(line, 1, pygame.Color('white'))
            intro_rect = string_rendered.get_rect()
            text_coord += 390
            intro_rect.top = text_coord
            intro_rect.x = 55
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)

    def update(*args):
        global flag2
        flag2 = 0
        a = args[0][0]
        b = args[0][1]
        x1_1 = args[1][0]
        x2_1 = args[1][1]
        y1_1 = args[1][2]
        y2_1 = args[1][3]
        if x1_1 <= a <= x2_1 and y1_1 <= b <= y2_1:
            flag2 = 1
            pygame.draw.polygon(screen, pygame.Color('red'), [(50, 250), (50, 300), (250, 300), (250, 250)])
            font = pygame.font.Font(None, 30)
            text_coord = 50
            for line in load_text:
                string_rendered = font.render(line, 1, pygame.Color('white'))
                intro_rect = string_rendered.get_rect()
                text_coord += 210
                intro_rect.top = text_coord
                intro_rect.x = 55
                text_coord += intro_rect.height
                screen.blit(string_rendered, intro_rect)
        else:
            pygame.draw.polygon(screen, pygame.Color('black'), [(50, 250), (50, 300), (250, 300), (250, 250)])
            font = pygame.font.Font(None, 30)
            text_coord = 50
            for line in load_text:
                string_rendered = font.render(line, 1, pygame.Color('white'))
                intro_rect = string_rendered.get_rect()
                text_coord += 210
                intro_rect.top = text_coord
                intro_rect.x = 55
                text_coord += intro_rect.height
                screen.blit(string_rendered, intro_rect)
        if level >= 0:
            x1_2 = args[2][0]
            x2_2 = args[2][1]
            y1_2 = args[2][2]
            y2_2 = args[2][3]
            if x1_2 <= a <= x2_2 and y1_2 <= b <= y2_2:
                flag2 = 2
                pygame.draw.polygon(screen, pygame.Color('red'), [(50, 310), (50, 360), (250, 360), (250, 310)])
                font = pygame.font.Font(None, 30)
                text_coord = 50
                for line in l1_text:
                    string_rendered = font.render(line, 1, pygame.Color('white'))
                    intro_rect = string_rendered.get_rect()
                    text_coord += 270
                    intro_rect.top = text_coord
                    intro_rect.x = 55
                    text_coord += intro_rect.height
                    screen.blit(string_rendered, intro_rect)
            else:
                pygame.draw.polygon(screen, pygame.Color('black'), [(50, 310), (50, 360), (250, 360), (250, 310)])
                font = pygame.font.Font(None, 30)
                text_coord = 50
                for line in l1_text:
                    string_rendered = font.render(line, 1, pygame.Color('white'))
                    intro_rect = string_rendered.get_rect()
                    text_coord += 270
                    intro_rect.top = text_coord
                    intro_rect.x = 55
                    text_coord += intro_rect.height
                    screen.blit(string_rendered, intro_rect)
        if level >= 1:
            x1_3 = args[3][0]
            x2_3 = args[3][1]
            y1_3 = args[3][2]
            y2_3 = args[3][3]
            if x1_3 <= a <= x2_3 and y1_3 <= b <= y2_3:
                flag2 = 3
                pygame.draw.polygon(screen, pygame.Color('red'), [(50, 370), (50, 420), (250, 420), (250, 370)])
                font = pygame.font.Font(None, 30)
                text_coord = 50
                for line in l2_text:
                    string_rendered = font.render(line, 1, pygame.Color('white'))
                    intro_rect = string_rendered.get_rect()
                    text_coord += 330
                    intro_rect.top = text_coord
                    intro_rect.x = 55
                    text_coord += intro_rect.height
                    screen.blit(string_rendered, intro_rect)
            else:
                pygame.draw.polygon(screen, pygame.Color('black'), [(50, 370), (50, 420), (250, 420), (250, 370)])
                font = pygame.font.Font(None, 30)
                text_coord = 50
                for line in l2_text:
                    string_rendered = font.render(line, 1, pygame.Color('white'))
                    intro_rect = string_rendered.get_rect()
                    text_coord += 330
                    intro_rect.top = text_coord
                    intro_rect.x = 55
                    text_coord += intro_rect.height
                    screen.blit(string_rendered, intro_rect)
        if level >= 2:
            x1_4 = args[4][0]
            x2_4 = args[4][1]
            y1_4 = args[4][2]
            y2_4 = args[4][3]
            if x1_4 <= a <= x2_4 and y1_4 <= b <= y2_4:
                flag2 = 4
                pygame.draw.polygon(screen, pygame.Color('red'), [(50, 430), (50, 480), (250, 480), (250, 430)])
                font = pygame.font.Font(None, 30)
                text_coord = 50
                for line in l3_text:
                    string_rendered = font.render(line, 1, pygame.Color('white'))
                    intro_rect = string_rendered.get_rect()
                    text_coord += 390
                    intro_rect.top = text_coord
                    intro_rect.x = 55
                    text_coord += intro_rect.height
                    screen.blit(string_rendered, intro_rect)
            else:
                pygame.draw.polygon(screen, pygame.Color('black'), [(50, 430), (50, 480), (250, 480), (250, 430)])
                font = pygame.font.Font(None, 30)
                text_coord = 50
                for line in l3_text:
                    string_rendered = font.render(line, 1, pygame.Color('white'))
                    intro_rect = string_rendered.get_rect()
                    text_coord += 390
                    intro_rect.top = text_coord
                    intro_rect.x = 55
                    text_coord += intro_rect.height
                    screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                with open("data/options.txt", 'w', encoding='utf-8') as f:
                    # print(str(volume) + str(blood))
                    f.write(str(volume) + str(blood))
                with open("data/now_level.txt", 'w', encoding='utf-8') as f:
                    # print(str(volume) + str(blood))
                    f.write(str(now_level))
                terminate()
            if event.type == pygame.MOUSEMOTION:
                update(event.pos, [50, 250, 250, 300], [50, 250, 310, 360], [50, 250, 370, 420], [50, 250, 430, 480])
                x, y = event.pos
                arrow.update(x, y)
            if event.type == pygame.MOUSEBUTTONDOWN and flag2 == 1:
                start_screen(False)
                return
            if event.type == pygame.MOUSEBUTTONDOWN and flag2 == 2:
                now_level = 0
                clean()
                pygame.display.flip()
                # print(now_level)
                with open("data/now_level.txt", 'w', encoding='utf-8') as f:
                    f.write(str(now_level))
                if update_level:
                    level = now_level + 1
                    # print(level)
                    with open("data/pass_levels.txt", 'w', encoding='utf-8') as f:
                        f.write(str(level))
                return
            if event.type == pygame.MOUSEBUTTONDOWN and flag2 == 3:
                now_level = 1
                clean()
                pygame.display.flip()
                # print(now_level)
                with open("data/now_level.txt", 'w', encoding='utf-8') as f:
                    f.write(str(now_level))
                if update_level:
                    level = now_level + 1
                    # print(level)
                    with open("data/pass_levels.txt", 'w', encoding='utf-8') as f:
                        f.write(str(level))
                return
            if event.type == pygame.MOUSEBUTTONDOWN and flag2 == 4:
                now_level = 2
                clean()
                pygame.display.flip()
                # print(now_level)
                with open("data/now_level.txt", 'w', encoding='utf-8') as f:
                    f.write(str(now_level))
                if update_level:
                    level = now_level + 1
                    # print(level)
                    with open("data/pass_levels.txt", 'w', encoding='utf-8') as f:
                        f.write(str(level))
                return
        pygame.display.flip()
        clock.tick(FPS)


flag4 = 0


def contin():
    global flag4
    next_text = ["N.E.X.T.>"]
    exit_text = ["M.E.N.U."]
    fon = pygame.transform.scale(load_image('fon3.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    pygame.draw.polygon(screen, pygame.Color('black'), [(50, 250), (50, 300), (250, 300), (250, 250)])
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in next_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 210
        intro_rect.top = text_coord
        intro_rect.x = 55
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    pygame.draw.polygon(screen, pygame.Color('black'), [(50, 310), (50, 360), (250, 360), (250, 310)])
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in exit_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 270
        intro_rect.top = text_coord
        intro_rect.x = 55
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    def update(*args):
        global flag4
        a = args[0][0]
        b = args[0][1]
        x1_1 = args[1][0]
        x2_1 = args[1][1]
        y1_1 = args[1][2]
        y2_1 = args[1][3]
        if x1_1 <= a <= x2_1 and y1_1 <= b <= y2_1:
            flag4 = 1
            pygame.draw.polygon(screen, pygame.Color('red'), [(50, 250), (50, 300), (250, 300), (250, 250)])
            font = pygame.font.Font(None, 30)
            text_coord = 50
            for line in next_text:
                string_rendered = font.render(line, 1, pygame.Color('white'))
                intro_rect = string_rendered.get_rect()
                text_coord += 210
                intro_rect.top = text_coord
                intro_rect.x = 55
                text_coord += intro_rect.height
                screen.blit(string_rendered, intro_rect)
        else:
            pygame.draw.polygon(screen, pygame.Color('black'), [(50, 250), (50, 300), (250, 300), (250, 250)])
            font = pygame.font.Font(None, 30)
            text_coord = 50
            for line in next_text:
                string_rendered = font.render(line, 1, pygame.Color('white'))
                intro_rect = string_rendered.get_rect()
                text_coord += 210
                intro_rect.top = text_coord
                intro_rect.x = 55
                text_coord += intro_rect.height
                screen.blit(string_rendered, intro_rect)
        x1_2 = args[2][0]
        x2_2 = args[2][1]
        y1_2 = args[2][2]
        y2_2 = args[2][3]
        if x1_2 <= a <= x2_2 and y1_2 <= b <= y2_2:
            flag4 = 2
            pygame.draw.polygon(screen, pygame.Color('red'), [(50, 310), (50, 360), (250, 360), (250, 310)])
            font = pygame.font.Font(None, 30)
            text_coord = 50
            for line in exit_text:
                string_rendered = font.render(line, 1, pygame.Color('white'))
                intro_rect = string_rendered.get_rect()
                text_coord += 270
                intro_rect.top = text_coord
                intro_rect.x = 55
                text_coord += intro_rect.height
                screen.blit(string_rendered, intro_rect)
        else:
            pygame.draw.polygon(screen, pygame.Color('black'), [(50, 310), (50, 360), (250, 360), (250, 310)])
            font = pygame.font.Font(None, 30)
            text_coord = 50
            for line in exit_text:
                string_rendered = font.render(line, 1, pygame.Color('white'))
                intro_rect = string_rendered.get_rect()
                text_coord += 270
                intro_rect.top = text_coord
                intro_rect.x = 55
                text_coord += intro_rect.height
                screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                with open("data/options.txt", 'w', encoding='utf-8') as f:
                    f.write(str(volume) + str(blood))
                with open("data/now_level.txt", 'w', encoding='utf-8') as f:
                    f.write(str(now_level))
                terminate()
            if event.type == pygame.MOUSEMOTION:
                update(event.pos, [50, 250, 250, 300], [50, 250, 310, 360])
                x, y = event.pos
                arrow.update(x, y)
            if event.type == pygame.MOUSEBUTTONDOWN and flag4 == 1 or event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                return
            if event.type == pygame.MOUSEBUTTONDOWN and flag4 == 2:
                start_screen()
                return
        pygame.display.flip()
        clock.tick(FPS)


flag5 = 0


def died():
    global flag5
    retry_text = ["<.R.E.T.R.Y."]
    exit_text = ["M.E.N.U."]
    fon = pygame.transform.scale(load_image('died_fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    pygame.draw.polygon(screen, pygame.Color('black'), [(50, 250), (50, 300), (250, 300), (250, 250)])
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in retry_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 210
        intro_rect.top = text_coord
        intro_rect.x = 55
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    pygame.draw.polygon(screen, pygame.Color('black'), [(50, 310), (50, 360), (250, 360), (250, 310)])
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in exit_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 270
        intro_rect.top = text_coord
        intro_rect.x = 55
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    def update(*args):
        global flag5
        a = args[0][0]
        b = args[0][1]
        x1_1 = args[1][0]
        x2_1 = args[1][1]
        y1_1 = args[1][2]
        y2_1 = args[1][3]
        if x1_1 <= a <= x2_1 and y1_1 <= b <= y2_1:
            flag5 = 1
            pygame.draw.polygon(screen, pygame.Color('red'), [(50, 250), (50, 300), (250, 300), (250, 250)])
            font = pygame.font.Font(None, 30)
            text_coord = 50
            for line in retry_text:
                string_rendered = font.render(line, 1, pygame.Color('white'))
                intro_rect = string_rendered.get_rect()
                text_coord += 210
                intro_rect.top = text_coord
                intro_rect.x = 55
                text_coord += intro_rect.height
                screen.blit(string_rendered, intro_rect)
        else:
            pygame.draw.polygon(screen, pygame.Color('black'), [(50, 250), (50, 300), (250, 300), (250, 250)])
            font = pygame.font.Font(None, 30)
            text_coord = 50
            for line in retry_text:
                string_rendered = font.render(line, 1, pygame.Color('white'))
                intro_rect = string_rendered.get_rect()
                text_coord += 210
                intro_rect.top = text_coord
                intro_rect.x = 55
                text_coord += intro_rect.height
                screen.blit(string_rendered, intro_rect)
        x1_2 = args[2][0]
        x2_2 = args[2][1]
        y1_2 = args[2][2]
        y2_2 = args[2][3]
        if x1_2 <= a <= x2_2 and y1_2 <= b <= y2_2:
            flag5 = 2
            pygame.draw.polygon(screen, pygame.Color('red'), [(50, 310), (50, 360), (250, 360), (250, 310)])
            font = pygame.font.Font(None, 30)
            text_coord = 50
            for line in exit_text:
                string_rendered = font.render(line, 1, pygame.Color('white'))
                intro_rect = string_rendered.get_rect()
                text_coord += 270
                intro_rect.top = text_coord
                intro_rect.x = 55
                text_coord += intro_rect.height
                screen.blit(string_rendered, intro_rect)
        else:
            pygame.draw.polygon(screen, pygame.Color('black'), [(50, 310), (50, 360), (250, 360), (250, 310)])
            font = pygame.font.Font(None, 30)
            text_coord = 50
            for line in exit_text:
                string_rendered = font.render(line, 1, pygame.Color('white'))
                intro_rect = string_rendered.get_rect()
                text_coord += 270
                intro_rect.top = text_coord
                intro_rect.x = 55
                text_coord += intro_rect.height
                screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                with open("data/options.txt", 'w', encoding='utf-8') as f:
                    f.write(str(volume) + str(blood))
                with open("data/now_level.txt", 'w', encoding='utf-8') as f:
                    f.write(str(now_level))
                terminate()
            if event.type == pygame.MOUSEMOTION:
                update(event.pos, [50, 250, 250, 300], [50, 250, 310, 360])
                x, y = event.pos
                arrow.update(x, y)
            if event.type == pygame.MOUSEBUTTONDOWN and flag5 == 1 or event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                clean()
                return
            if event.type == pygame.MOUSEBUTTONDOWN and flag5 == 2:
                start_screen()
                return
        pygame.display.flip()
        clock.tick(FPS)


flag6 = 0


def end_screen():
    global flag6
    next_text = ["N.E.X.T.>"]
    fon = pygame.transform.scale(load_image('end.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    pygame.draw.polygon(screen, pygame.Color('black'), [(50, 250), (50, 300), (250, 300), (250, 250)])
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in next_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 210
        intro_rect.top = text_coord
        intro_rect.x = 55
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    def update(*args):
        global flag6
        a = args[0][0]
        b = args[0][1]
        x1_1 = args[1][0]
        x2_1 = args[1][1]
        y1_1 = args[1][2]
        y2_1 = args[1][3]
        if x1_1 <= a <= x2_1 and y1_1 <= b <= y2_1:
            flag6 = 1
            pygame.draw.polygon(screen, pygame.Color('red'), [(50, 250), (50, 300), (250, 300), (250, 250)])
            font = pygame.font.Font(None, 30)
            text_coord = 50
            for line in next_text:
                string_rendered = font.render(line, 1, pygame.Color('white'))
                intro_rect = string_rendered.get_rect()
                text_coord += 210
                intro_rect.top = text_coord
                intro_rect.x = 55
                text_coord += intro_rect.height
                screen.blit(string_rendered, intro_rect)
        else:
            pygame.draw.polygon(screen, pygame.Color('black'), [(50, 250), (50, 300), (250, 300), (250, 250)])
            font = pygame.font.Font(None, 30)
            text_coord = 50
            for line in next_text:
                string_rendered = font.render(line, 1, pygame.Color('white'))
                intro_rect = string_rendered.get_rect()
                text_coord += 210
                intro_rect.top = text_coord
                intro_rect.x = 55
                text_coord += intro_rect.height
                screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                with open("data/options.txt", 'w', encoding='utf-8') as f:
                    f.write(str(volume) + str(blood))
                with open("data/now_level.txt", 'w', encoding='utf-8') as f:
                    f.write(str(now_level))
                terminate()
            if event.type == pygame.MOUSEMOTION:
                update(event.pos, [50, 250, 250, 300], [50, 250, 310, 360])
                x, y = event.pos
                arrow.update(x, y)
            if (event.type == pygame.MOUSEBUTTONDOWN and flag6 == 1) or (event.type == pygame.KEYUP and event.key == pygame.K_SPACE):
                print(1)
                start_screen()
                return
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


class Door(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, definition):
        super().__init__(doors_group, all_sprites)
        self.image = pygame.transform.flip(door_image_closed, not definition, False)
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)
        self.definition = definition

    def update(self):
        global next_level
        self.image = pygame.transform.flip(door_image_opened, not self.definition, False)
        next_level = True


class Button(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(button_group, all_sprites)
        self.image = button_image_unclicked
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)

    def update(self):
        if pygame.sprite.spritecollideany(self, player_group) and (boss is None):
            self.image = button_image_clicked
            doors_group.update()


class Arrow(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(arrow_group, all_sprites)
        self.image = pygame.transform.scale(arrow_image, (40, 40))
        self.rect = self.image.get_rect()

    def update(self, pos_x, pos_y):
        self.rect.x = pos_x
        self.rect.y = pos_y


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, definition, boss=None):
        pygame.sprite.Sprite.__init__(self)
        if boss is not None:
            if boss > 0:
                self.image = pygame.transform.scale(bullet_turn_image, (20, 15))
            if boss < 0:
                self.image = pygame.transform.scale(bullet_turn_image, (20, 15))
                self.image = pygame.transform.flip(self.image, False, True)
            if boss == 0:
                self.image = pygame.transform.scale(bullet_image, (20, 10))
            self.rect = self.image.get_rect()
            self.speedy = boss
        else:
            self.image = pygame.transform.scale(bullet_image, (20, 10))
            self.rect = self.image.get_rect()
            self.speedy = 0
        self.disappear = False
        if definition:
            self.rect.centerx = x + 10
            self.speedx = 30
        else:
            self.rect.centerx = x - 10
            self.speedx = -30
            self.image = pygame.transform.flip(self.image, True, False)
        self.rect.centery = y - 15

    def update(self):
        self.rect.x += self.speedx
        self.rect.y -= self.speedy
        # убить, если он заходит за верхнюю часть экрана
        if self.disappear:
            self.kill()
        if pygame.sprite.spritecollideany(self, walls_group):
            self.kill()
        if pygame.sprite.spritecollideany(self, enemies_group):
            self.disappear = True
        if pygame.sprite.spritecollideany(self, boss_group):
            self.disappear = True


class Particle(pygame.sprite.Sprite):
    # сгенерируем частицы разного размера
    fire = [load_image("blood.png", -1)]
    for scale in (1, 2, 3):
        fire.append(pygame.transform.scale(fire[0], (scale, scale)))

    def __init__(self, pos, dx, dy, sprite=None):
        super().__init__(blood_group, all_sprites)
        self.image = random.choice(self.fire)
        self.rect = self.image.get_rect()
        # у каждой частицы своя скорость — это вектор
        self.velocity = [dx, dy]
        # и свои координаты
        self.rect.x, self.rect.y = pos
        self.g = 1
        self.sprite = sprite

    def update(self):
        # применяем гравитационный эффект:
        # движение с ускорением под действием гравитации
        self.velocity[1] += self.g
        # перемещаем частицу
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        # убиваем, если частица ушла за экран
        if pygame.sprite.spritecollideany(self, walls_group):
            self.kill()
            if self.sprite is not None:
                died()


class Peak(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(peaks_group, all_sprites)
        self.image = pygame.transform.scale(peak_image, (50, 50))
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)


class Area(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, definition):
        super().__init__(all_sprites)
        self.image = pygame.transform.scale(area_image, (800, 80))
        if definition:
            self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y - 30)
        else:
            self.rect = self.image.get_rect().move(tile_width * pos_x - 720, tile_height * pos_y - 30)


class Boss(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(boss_group, all_sprites)
        self.image = pygame.transform.scale(boss_image, (80, 80))
        self.definition = True
        self.hp = 10
        self.area = Area(pos_x, pos_y, self.definition)
        if not self.definition:
            self.image = pygame.transform.flip(self.image, True, False)
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)

    def update(self):
        if pygame.sprite.spritecollideany(self, bullets_group):
            self.hp -=1
            death_sound.play()
            if blood == 0 and self.hp <= 0:
                create_particles((self.rect.centerx, self.rect.centery))
            if self.hp <= 0:
                self.kill()
        if pygame.sprite.spritecollideany(self, walls_group):
            if pygame.sprite.spritecollide(self, walls_group, False)[0].rect.y <= self.rect.y:
                while pygame.sprite.spritecollideany(self, walls_group):
                    self.rect.y += 1
            else:
                while pygame.sprite.spritecollideany(self, walls_group):
                    self.rect.y -= 1

    def turn(self):
        if not pygame.sprite.spritecollideany(self.area, player_group):
            self.definition = not self.definition
            self.image = pygame.transform.flip(self.image, True, False)
            if self.definition:
                self.area.rect.x += 720
            else:
                self.area.rect.x -= 720

    def shoot(self):
        if pygame.sprite.spritecollideany(self.area, player_group):
            for i in [13, 0, -13]:
                if self.definition:
                    bullet = Bullet(self.rect.centerx + 41, self.rect.centery + 20, self.definition, i)
                else:
                    bullet = Bullet(self.rect.centerx - 41, self.rect.centery + 20, self.definition, i)
                all_sprites.add(bullet)
                bullets_group.add(bullet)
            shoot_sound.play()


class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, defenition):
        super().__init__(enemies_group, all_sprites)
        self.image = pygame.transform.scale(enemy_image, (80, 80))
        self.definition = defenition
        self.area = Area(pos_x, pos_y, self.definition)
        if not defenition:
            self.image = pygame.transform.flip(self.image, True, False)
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)

    def update(self):
        if pygame.sprite.spritecollideany(self, bullets_group):
            death_sound.play()
            if blood == 0:
                create_particles((self.rect.centerx, self.rect.centery))
            self.kill()
        if pygame.sprite.spritecollideany(self, walls_group):
            if pygame.sprite.spritecollide(self, walls_group, False)[0].rect.y <= self.rect.y:
                while pygame.sprite.spritecollideany(self, walls_group):
                    self.rect.y += 1
            else:
                while pygame.sprite.spritecollideany(self, walls_group):
                    self.rect.y -= 1

    def shoot(self):
        if pygame.sprite.spritecollideany(self.area, player_group):
            if self.definition:
                bullet = Bullet(self.rect.centerx + 41, self.rect.centery + 20, self.definition)
            else:
                bullet = Bullet(self.rect.centerx - 41, self.rect.centery + 20, self.definition)
            all_sprites.add(bullet)
            bullets_group.add(bullet)
            shoot_sound.play()


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = self.image = pygame.transform.scale(player_image_static, (40, 80))
        self.rect = self.image.get_rect().move(tile_width * pos_x + 15, tile_height * pos_y + 5)
        self.g = 1
        self.ground = False
        self.definition = True
        self.vx = 10
        self.vfall = 0

    def update(self, key):
        global next_level, fon_sound
        if key[0] and self.ground:
            self.vfall = -20
            if pygame.sprite.spritecollideany(self, walls_group):
                self.rect.y += self.vfall
            if not pygame.sprite.spritecollideany(self, stairs_group):
                self.ground = False
            self.picture()

        if key[1]:
            self.rect.x += self.vx
            if pygame.sprite.spritecollideany(self, walls_group):
                self.rect.x -= self.vx
        if key[2]:
            self.rect.y += self.vx
            if pygame.sprite.spritecollideany(self, walls_group):
                self.rect.y -= self.vx
        if key[3]:
            self.rect.x -= self.vx
            if pygame.sprite.spritecollideany(self, walls_group):
                self.rect.x += self.vx
        if len(pygame.sprite.spritecollide(self, doors_group, False)) == 4 and next_level:
            global player, level_x, level_y, button, doors, now_level, levels_list, update_level, level
            screen.fill(pygame.Color('black'))
            now_level += 1
            if len(levels_list) == now_level:
                now_level = 0
                end_screen()
                with open("data/now_level.txt", 'w', encoding='utf-8') as f:
                    f.write(str(now_level))
            else:
                contin()
                clean()
                pygame.display.flip()
                with open("data/now_level.txt", 'w', encoding='utf-8') as f:
                    f.write(str(now_level))
                if update_level:
                    level = now_level
                    with open("data/pass_levels.txt", 'w', encoding='utf-8') as f:
                        f.write(str(level))

        if (pygame.sprite.spritecollideany(self, bullets_group) or pygame.sprite.spritecollideany(self, enemies_group)
                or pygame.sprite.spritecollideany(self, peaks_group) or pygame.sprite.spritecollideany(self, boss_group)):
            global player_image_static, player_image_jumping, player_image_climbing, alive # , check_cam
            herodeath_sound.play()
            alive = False
            player_image_static = pygame.transform.scale(area_image, (40, 80))
            player_image_jumping = pygame.transform.scale(area_image, (40, 80))
            player_image_climbing = pygame.transform.scale(area_image, (40, 80))
            if pygame.sprite.spritecollideany(self, bullets_group):
                pygame.sprite.spritecollide(self, bullets_group, False)[0].kill()
            self.kill()
            key = [False, False, False, False]
            if blood == 0:
                create_particles((self.rect.centerx, self.rect.centery), self)
            else:
                died()

    def shoot(self):
        if self.definition:
            bullet = Bullet(self.rect.centerx + 30, self.rect.centery, self.definition)
        else:
            bullet = Bullet(self.rect.centerx - 30, self.rect.centery, self.definition)
        all_sprites.add(bullet)
        bullets_group.add(bullet)
        shoot_sound.play()

    def picture(self, definition=None):
        if self.ground:
            self.image = pygame.transform.scale(player_image_static, (40, 80))
        else:
            self.image = pygame.transform.scale(player_image_jumping, (40, 80))
            self.check_image = False
        if pygame.sprite.spritecollideany(self, stairs_group):
            self.image = pygame.transform.scale(player_image_climbing, (40, 80))
        if not self.definition:
            self.image = pygame.transform.flip(self.image, True, False)
        if definition is not None:
            if definition != self.definition:
                self.image = pygame.transform.flip(self.image, True, False)
                self.definition = definition

    def gravity(self):
        self.rect.y += self.vfall
        if pygame.sprite.spritecollideany(self, walls_group):
            if pygame.sprite.spritecollide(self, walls_group, False)[0].rect.y <= self.rect.y:
                while pygame.sprite.spritecollideany(self, walls_group):
                    self.rect.y += 1
            else:
                while pygame.sprite.spritecollideany(self, walls_group):
                    self.rect.y -= 1
                self.ground = True
            self.vfall = 0
            self.picture()
        else:
            self.picture()
            self.ground = False
            self.vfall += self.g
        if pygame.sprite.spritecollideany(self, stairs_group):
            self.ground = True
            self.g = 0
            self.vfall = 0
        else:
            self.g = 1


pygame.display.set_icon(load_image('icon.png'))
pygame.display.set_caption('B.U.L.L.E.T.')
clock = pygame.time.Clock()
key = [False, False, False, False]
FPS = 60
tile_images = {'wall': load_image('box.png'), 'stair': load_image('stair.png'),
               'empty': load_image('tile.png'), 'space': load_image('space.png', -1)}
player_image_static = load_image('hero.png', -1)
player_image_jumping = load_image('herojump.png', -1)
player_image_climbing = load_image('heroback.png', -1)
alive = True
boss_image = load_image('boss.png', -1)
enemy_image = load_image('enemy.png', -1)
peak_image = load_image('peak.png', -1)
bullet_image = load_image('bullet.png', -1)
bullet_turn_image = load_image('bullet2.png', -1)
button_image_unclicked = load_image('button1.png', -1)
button_image_clicked = load_image('button2.png', -1)
door_image_closed = load_image('door1.png')
door_image_opened = load_image('door2.png')
area_image = load_image("area.png", -1)
arrow_image = load_image("arrow2.png")
tile_width = tile_height = 50
levels_list = ['level1.txt', 'level2.txt', 'level3.txt']
shoot_sound = pygame.mixer.Sound(path.join('sounds', 'shoot.wav'))
death_sound = pygame.mixer.Sound(path.join('sounds', 'death.wav'))
herodeath_sound = pygame.mixer.Sound(path.join('sounds', 'herodeath.wav'))
tracklist = ['sounds/' + i for i in ['level1.mp3', 'level2.mp3', 'level3.mp3', 'main_theme.wav']]
pygame.mixer.music.load(tracklist[3])
pygame.mixer.music.set_volume(0.5)
MYEVENTTYPE = 30
hardness = 1200
event_counter = 0
pygame.time.set_timer(MYEVENTTYPE, hardness)
with open("data/now_level.txt", 'r') as mapFile:
    now_level = int([line.strip() for line in mapFile][0])
# группы спрайтов
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
walls_group = pygame.sprite.Group()
stairs_group = pygame.sprite.Group()
button_group = pygame.sprite.Group()
doors_group = pygame.sprite.Group()
arrow_group = pygame.sprite.Group()
bullets_group = pygame.sprite.Group()
boss_group = pygame.sprite.Group()
enemies_group = pygame.sprite.Group()
peaks_group = pygame.sprite.Group()
blood_group = pygame.sprite.Group()
camera = Camera()
arrow = Arrow(0, 0)

start_screen()
player, enemies, boss, peaks,  level_x, level_y, button, doors, next_level = None, None, None, None, None, None, None, None, None
clean()
running = True
while running:
    bullets_group.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            with open("data/options.txt", 'w', encoding='utf-8') as f:
                f.write(str(volume) + str(blood))
            with open("data/now_level.txt", 'w', encoding='utf-8') as f:
                f.write(str(now_level))
        if event.type == pygame.KEYDOWN:
            if alive:
                if event.key == pygame.K_SPACE:
                    player.shoot()
                if event.key == pygame.K_w:
                    key[0] = True
                if event.key == pygame.K_d:
                    key[1] = True
                    player.picture(True)
                if event.key == pygame.K_s:
                    key[2] = True
                if event.key == pygame.K_a:
                    key[3] = True
                    player.picture(False)
        if event.type == pygame.KEYUP:
            if alive:
                if event.key == pygame.K_w:
                    key[0] = False
                if event.key == pygame.K_d:
                    key[1] = False
                if event.key == pygame.K_s:
                    key[2] = False
                if event.key == pygame.K_a:
                    key[3] = False
        if event.type == pygame.MOUSEMOTION:
            x, y = event.pos
            arrow.update(x, y)
            if pygame.mouse.get_focused():
                arrow_group.draw(screen)
        if event.type == MYEVENTTYPE:
            event_counter += 1
            if alive:
                for sprite in enemies_group:
                    sprite.shoot()
                for sprite in boss_group:
                    sprite.shoot()
            if event_counter == 3:
                for sprite in boss_group:
                    sprite.turn()
                event_counter = 0
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE:
                menu()
                if exit == 1:
                    exit = 0

    if not alive:
        key = [False, False, False, False]
    if alive:
        player.gravity()
    player_group.update(key)
    if alive:
        button_group.update()
    boss_group.update()
    if len(boss_group) == 0:
        boss = None
    enemies_group.update()
    blood_group.update()
    # изменяем ракурс камеры
    if len(player_group) != 0:
        camera.update(player)
        # обновляем положение всех спрайтов
        for sprite in all_sprites:
            camera.apply(sprite)
    screen.fill((0, 0, 0))
    all_sprites.draw(screen)
    pygame.display.flip()
    clock.tick(FPS)
pygame.quit()
