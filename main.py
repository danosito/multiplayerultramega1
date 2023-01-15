import os
import sys
import random
import pygame


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


pygame.init()
size = width, height = 20 * 50, 14 * 50
screen = pygame.display.set_mode(size)
player = None
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
wall_group = pygame.sprite.Group()
barrier_group = pygame.sprite.Group()
water_group = pygame.sprite.Group()
dirt_group = pygame.sprite.Group()
ice_btn_group = pygame.sprite.Group()
fire_btn_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
tile_images = {
    'wall': load_image('brick.png'),
    "stairs": load_image("stair.png"),
    "key": load_image("key.png"),
    "ice": load_image("ice.png"),
    "fire": load_image("fire.png"),
    "keyhole": load_image("keyhole.png"),
    'portal': load_image("portal.png"),
    "hit_brick": load_image("break_brick.png"),
    "water": load_image("water.png"),
    "fire_btn": load_image("fire_button.png"),
    "ice_btn": load_image("ice_button.png"),
    "barrier": load_image("barrier.png"),
    "dirt": load_image("grass.png"),
    "dendro": load_image("dendro-column.png")
}
hydro_image = load_image('hydro.png')
electro_image = load_image('electroman.png')
pyro_image = load_image('fireman.png')
cryo_image = load_image('crioman.png')
anemo_image = load_image('anemoman.png')
geo_image = load_image('geoman.png')
dendro_image = load_image('dendroman.png')
hydro_info = load_image('hydro_info.png')
electro_info = load_image('electro_info.png')
pyro_info = load_image('piro_info.png')
cryo_info = load_image('crio_info.png')
anemo_info = load_image('anemo_info.png')
geo_info = load_image('geo_info.png')
dendro_info = load_image('dendro_info.png')
scaled = [load_image("hydro_scaled.png"), load_image("fireman_scaled.png"), load_image("geoman_scaled.png"), load_image("crioman_scaled.png"), load_image("dendroman_scaled.png"), load_image("electroman_scaled.png"), load_image("anemoman_scaled.png")]
perss = [hydro_image, pyro_image, geo_image, cryo_image, dendro_image, electro_image, anemo_image]
persi = [hydro_info, pyro_info, geo_info, cryo_info, dendro_info, electro_info, anemo_info]
stairs_group = pygame.sprite.Group()
hit_brick_group = pygame.sprite.Group()
key_group = pygame.sprite.Group()
ice_group = pygame.sprite.Group()
fire_group = pygame.sprite.Group()
keyhole_group = pygame.sprite.Group()
portal_group = pygame.sprite.Group()
isOvered = False
tile_width = tile_height = 50

def generate_level(level, sel1, sel2):
    new_player, x, y, new_player2 = None, None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == 'b':
                Tile("wall", x, y)
            if level[y][x] == '@':
                new_player = Player(x, y, sel1)
            if level[y][x] == '*':
                new_player2 = Player(x, y, sel2)
            if level[y][x] == 's':
                Tile("stairs", x, y)
            if level[y][x] == 'k':
                Tile("key", x, y)
            if level[y][x] == 'i':
                Tile("ice", x, y)
            if level[y][x] == 'f':
                Tile("fire", x, y)
            if level[y][x] == 'u':
                Tile("keyhole", x, y)
            if level[y][x] == 'p':
                Tile("portal", x, y)
            if level[y][x] == 'h':
                Tile("hit_brick", x, y)
            if level[y][x] == 'h':
                Tile("hit_brick", x, y)
            if level[y][x] == 'o':
                Tile("barrier", x, y)
            if level[y][x] == 'x':
                Button("ice_btn", x, y)
            if level[y][x] == 'y':
                Button("fire_btn", x, y)
            if level[y][x] == "w":
                Tile("water", x, y)
            if level[y][x] == 'd':
                Tile("dirt", x, y)
    return new_player, x, y, new_player2


def load_level(filename):
    filename = "data/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def terminate():
    pygame.quit()
    sys.exit()

def start_screen():
    intro_text = ["ДОБРО ПОЖАЛОВАТЬ!:)", "",
                  "Правила игры",
                  "игра на двух игроков.",
                  "Вначале выберите персонажа",
                  "и уровень,",
                  "они открываются последовательно.",
                  "нажмите на кнопку i,",
                  "чтобы посмотреть информацию",
                  "о выбранном персонаже/уровне.",
                  "управление для первого игрока:",
                  "a-влево, d-вправо, w-прыжок",
                  "s-специальное действие*.",
                  "управление для второго игрока:",
                  "←-влево, →-вправо, ↑-прыжок",
                  "↓-специальное действие*.",
                  "",
                  "",
                  "*специальные действия есть у некоторых персонажей. читайте их описание"]

    fon = pygame.transform.scale(load_image('preview.png'), (width, height  ))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font("ARIALUNI.TTF", 15)
    text_coord = 15
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 0
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock1.tick(60)


def urovgen():
    map = open(f"data\{input('название уровня')}.txt", "w")
    s = int(input("количество ячеек"))
    maplist = []
    for i in range(s):
        maplist.append([])
        for j in range(s):
            maplist[i].append(".")
            if random.randint(1, 10) < 5:
                maplist[i][j] = "#"
    maplist[random.randint(0, s - 1)][random.randint(0, s - 1)] = "@"
    for i in range(len(maplist)):
        map.write("".join(maplist[i]))
        if i != s - 1:
            map.write("\n")


def checker(self):
    global isOvered
    if self.player_type == anemo_image:
        if pygame.sprite.spritecollideany(self, ice_group):
            isOvered = True
        if pygame.sprite.spritecollideany(self, fire_group):
            isOvered = True
        if pygame.sprite.spritecollideany(self, water_group):
            isOvered = True
    if self.player_type == dendro_image:
        if pygame.sprite.spritecollideany(self, fire_group):
            isOvered = True
    if self.player_type == electro_image:
        if pygame.sprite.spritecollideany(self, fire_group) or pygame.sprite.spritecollideany(self, water_group):
            isOvered = True
    if self.player_type == hydro_image:
        if pygame.sprite.spritecollideany(self, ice_group):
            isOvered = True
        if pygame.sprite.spritecollideany(self, fire_group):
            pygame.sprite.spritecollideany(self, fire_group).kill()
    if self.player_type == cryo_image:
        if pygame.sprite.spritecollideany(self, water_group):
            Tile("ice", pygame.sprite.spritecollideany(self, water_group).pos_x, pygame.sprite.spritecollideany(self, water_group).pos_y)
            pygame.sprite.spritecollideany(self, water_group).kill()
        if pygame.sprite.spritecollideany(self, fire_group):
            isOvered = True
        if pygame.sprite.spritecollideany(self, water_group):
            isOvered = True
    if self.player_type == pyro_image:
        if pygame.sprite.spritecollideany(self, ice_group):
            pygame.sprite.spritecollideany(self, ice_group).kill()
        if pygame.sprite.spritecollideany(self, water_group):
            isOvered = True
    if self.player_type == geo_image:
        if pygame.sprite.spritecollideany(self, hit_brick_group):
            pygame.sprite.spritecollideany(self, hit_brick_group).kill()
        if pygame.sprite.spritecollideany(self, water_group):
            isOvered = True
    if pygame.sprite.spritecollideany(self, keyhole_group):
        if self.hasKey:
            self.hasKey -= 1
            pygame.sprite.spritecollideany(self, keyhole_group).kill()


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        if tile_type != "wall":
            self.pos_x = pos_x
            self.pos_y = pos_y
            self.image = tile_images[tile_type]
            self.rect = self.image.get_rect().move(
                tile_width * pos_x, tile_height * pos_y)
            if tile_type == "hit_brick":
                super().__init__(hit_brick_group, wall_group, tiles_group, all_sprites)
            if tile_type == "stairs" or tile_type == "dendro":
                super().__init__(stairs_group, tiles_group, all_sprites)
            elif tile_type == "key":
                super().__init__(key_group, tiles_group, all_sprites)
            elif tile_type == "ice":
                super().__init__(ice_group, wall_group, tiles_group, all_sprites)
            elif tile_type == "fire":
                super().__init__(fire_group, tiles_group, all_sprites)
            elif tile_type == "keyhole":
                super().__init__(keyhole_group, wall_group, tiles_group, all_sprites)
            elif tile_type == "portal":
                super().__init__(portal_group, tiles_group, all_sprites)
            elif tile_type == "barrier":
                super().__init__(barrier_group, wall_group, tiles_group, all_sprites)
            elif tile_type == "water":
                super().__init__(water_group, tiles_group, all_sprites)
            elif tile_type == "dirt":
                super().__init__(dirt_group, wall_group, tiles_group, all_sprites)
        else:
            Wall(tile_type, pos_x, pos_y)


class Wall(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        self.pos_x = pos_x
        self.pos_y = pos_y
        super().__init__(tiles_group, wall_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, player_type):
        self.hasKey = 0
        self.pos_x = pos_x
        self.pos_y = pos_y
        super().__init__(player_group, all_sprites)
        self.image = player_type
        self.player_type = player_type
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)
        self.isRight = False
        self.isLeft = False
        self.isJumping = False
        self.jumpingForce = 0
        self.isFinished = False

    def move(self, event):
        if event.key == 119 or event.key == 1073741906:
            if not(self.isJumping):
                self.rect.y += 5
                if pygame.sprite.spritecollideany(self, wall_group):
                    self.isJumping = True
                    if player.player_type == anemo_image or player2.player_type == anemo_image:
                        self.jumpingForce = 30
                    else:
                        self.jumpingForce = 20
                self.rect.y -= 5
                if self == player:
                    wall_group.remove(player2)
                else:
                    wall_group.remove(player)
        if event.key == 97 or event.key == 1073741904:
            self.isLeft = True
        if event.key == 115 or event.key == 1073741905:
            if self.player_type == dendro_image:
                self.rect.y += 25
                if pygame.sprite.spritecollideany(self, dirt_group):
                    self.rect.y -= 25
                    Tile("dendro", round(self.rect.x / 50), round(self.rect.y / 50) - 2)
                else:
                    self.rect.y -= 25
            if self.player_type == electro_image:
                self.rect.x += 5
                self.rect.y += 5
                if pygame.sprite.spritecollideany(self, keyhole_group):
                    pygame.sprite.spritecollideany(self, keyhole_group).kill()
                self.rect.x -= 10
                self.rect.y -= 10
                if pygame.sprite.spritecollideany(self, keyhole_group):
                    pygame.sprite.spritecollideany(self, keyhole_group).kill()
                self.rect.x += 5
                self.rect.y += 5
        if event.key == 100 or event.key == 1073741903:
            self.isRight = True

    def stopmove(self, event):
        if event.key == 97 or event.key == 1073741904:
            self.isLeft = False
        if event.key == 115 or event.key == 1073741905:
            pass  # down
        if event.key == 100 or event.key == 1073741903:
            self.isRight = False

    def update(self, chg1=None, chg2=None):
        if self.isLeft:
            if player.player_type == anemo_image or player2.player_type == anemo_image:
                self.rect.x -= 8
            else:
                self.rect.x -= 5
            if pygame.sprite.spritecollideany(self, wall_group):
                if player.player_type == anemo_image or player2.player_type == anemo_image:
                    self.rect.x += 8
                else:
                    self.rect.x += 5
        if self.isRight:
            if player.player_type == anemo_image or player2.player_type == anemo_image:
                self.rect.x += 8
            else:
                self.rect.x += 5
            if pygame.sprite.spritecollideany(self, wall_group):
                if player.player_type == anemo_image or player2.player_type == anemo_image:
                    self.rect.x -= 8
                else:
                    self.rect.x -= 5
        if self.isJumping:
            if pygame.sprite.spritecollideany(self, stairs_group):
                self.jumpingForce = 0
                if pygame.sprite.spritecollideany(self, wall_group):
                    self.rect.y += 10
                self.rect.y -= 5
            else:
                if self.jumpingForce != 0:
                    self.rect.y -= 5
                    self.jumpingForce -= 1
                    if pygame.sprite.spritecollideany(self, wall_group):
                        self.rect.y += 5
                else:
                    self.isJumping = False
        else:
            if not(pygame.sprite.spritecollideany(self, wall_group)):
                self.rect.y += 5
            if pygame.sprite.spritecollideany(self, wall_group):
                self.rect.y -= 5
        if self == player:
            wall_group.remove(player2)
        else:
            wall_group.remove(player)
        if chg1 != None:
            self.isLeft = chg1
        if chg2 != None:
            self.isRight = chg2
        if pygame.sprite.spritecollideany(self, key_group):
            self.hasKey += 1
            pygame.sprite.spritecollideany(self, key_group).kill()
        self.rect.y += 5
        self.rect.x += 5
        checker(self)
        self.rect.y -= 10
        self.rect.x -= 10
        checker(self)
        self.rect.y += 5
        self.rect.x += 5
        if pygame.sprite.spritecollideany(self, portal_group):
            self.isFinished = True
            pygame.sprite.spritecollideany(self, portal_group).kill()
            self.kill()


class Info():
    def __init__(self, isSprite, playerNum=None, levelnum=None):
        self.info_sprites = pygame.sprite.Group()
        if isSprite:
            char1 = pygame.sprite.Sprite()
            char1.image = scaled[playerNum]
            char1.rect = char1.image.get_rect()
            self.info_sprites.add(char1)
            char1.rect.x = 100
            char1.rect.y = 100
            char2 = pygame.sprite.Sprite()
            char2.image = persi[playerNum]
            char2.rect = char2.image.get_rect()
            self.info_sprites.add(char2)
            char2.rect.x = 400
            char2.rect.y = 50
            strelka1 = pygame.sprite.Sprite()
            strelka1.image = load_image("triangle1.png")
            strelka1.rect = strelka1.image.get_rect()
            self.info_sprites.add(strelka1)
            strelka1.rect.x = 0
            strelka1.rect.y = 0
        else:
            pass


class Button(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.tile_type = tile_type
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        if tile_type == "ice_btn":
            super().__init__(ice_btn_group, tiles_group, all_sprites)
        else:
            super().__init__(fire_btn_group, tiles_group, all_sprites)

    def updatee(self):
        if pygame.sprite.spritecollideany(self, player_group):
            if pygame.sprite.spritecollideany(self, player_group).player_type == cryo_image if self.tile_type == "ice_btn" else pyro_image:
                return True
        else:
            return False


running = True
player2 = None
level1 = load_level("lvl1.txt")
level2 = load_level("lvl2.txt")
level3 = load_level("lvl3.txt")
level4 = load_level("lvl4.txt")
level5 = load_level("lvl5.txt")
levels = [level1, level2, level3, level4, level5]
menu_sprites = pygame.sprite.Group()
strelka1 = pygame.sprite.Sprite()
strelka1.image = load_image("triangle1.png")
strelka1.rect = strelka1.image.get_rect()
menu_sprites.add(strelka1)
strelka1.rect.x = 0
strelka1.rect.y = 200
strelka2 = pygame.sprite.Sprite()
strelka2.image = load_image("triangle.png")
strelka2.rect = strelka2.image.get_rect()
menu_sprites.add(strelka2)
strelka2.rect.x = 200
strelka2.rect.y = 200
strelka3 = pygame.sprite.Sprite()
strelka3.image = load_image("triangle1.png")
strelka3.rect = strelka3.image.get_rect()
menu_sprites.add(strelka3)
strelka3.rect.x = 300
strelka3.rect.y = 200
strelka4 = pygame.sprite.Sprite()
strelka4.image = load_image("triangle.png")
strelka4.rect = strelka4.image.get_rect()
menu_sprites.add(strelka4)
strelka4.rect.x = 500
strelka4.rect.y = 200
strelka5 = pygame.sprite.Sprite()
strelka5.image = load_image("triangle1.png")
strelka5.rect = strelka5.image.get_rect()
menu_sprites.add(strelka5)
strelka5.rect.x = 600
strelka5.rect.y = 200
strelka6 = pygame.sprite.Sprite()
strelka6.image = load_image("triangle.png")
strelka6.rect = strelka6.image.get_rect()
menu_sprites.add(strelka6)
strelka6.rect.x = 800
strelka6.rect.y = 200
info1 = pygame.sprite.Sprite()
info1.image = load_image("info.png")
info1.rect = info1.image.get_rect()
menu_sprites.add(info1)
info1.rect.x = 400
info1.rect.y = 50
info2 = pygame.sprite.Sprite()
info2.image = load_image("info.png")
info2.rect = info2.image.get_rect()
menu_sprites.add(info2)
info2.rect.x = 100
info2.rect.y = 50
info3 = pygame.sprite.Sprite()
info3.image = load_image("info.png")
info3.rect = info3.image.get_rect()
menu_sprites.add(info3)
info3.rect.x = 700
info3.rect.y = 50
start_button = pygame.sprite.Sprite()
start_button.image = load_image("start.png")
start_button.rect = start_button.image.get_rect()
menu_sprites.add(start_button)
start_button.rect.x = 350
start_button.rect.y = 350
gameover_group = pygame.sprite.Group()
menu_group = pygame.sprite.Group()
gameover = pygame.sprite.Sprite()
gameover.image = load_image("gameover.png")
gameover.rect = gameover.image.get_rect()
gameover_group.add(gameover)
gameover.rect.x = -20 * 50
gameover.rect.y = 0
clock1 = pygame.time.Clock()
state = 0
g = open("data/lastlevel.txt")
readed = int(g.read())
nowlevelsel = readed + 1 if readed != 5 else readed
fon_group = pygame.sprite.Group()
fon = pygame.sprite.Sprite()
fon.image = load_image("fon.png")
fon.rect = fon.image.get_rect()
fon_group.add(fon)
char1 = pygame.sprite.Sprite()
char1.image = perss[0]
char1.rect = char1.image.get_rect()
menu_sprites.add(char1)
char1.rect.x = 425
char1.rect.y = 200
char2 = pygame.sprite.Sprite()
char2.image = perss[1]
char2.rect = char2.image.get_rect()
menu_sprites.add(char2)
char2.rect.x = 725
char2.rect.y = 200
g.close()
chr12 = [0, 1]
message = ""
start_screen()
while running:
    if state == 1:
        if not(isOvered):
            fon_group.draw(screen)
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    running = False
                if ev.type == pygame.KEYDOWN:
                    if ev.key in [97, 100, 119, 115]:
                        player.move(ev)
                    else:
                        player2.move(ev)
                if ev.type == pygame.KEYUP:
                    if ev.key in [97, 100, 119, 115]:
                        player.stopmove(ev)
                    else:
                        player2.stopmove(ev)
            if not player.isFinished:
                player.update()
            if not player2.isFinished:
                player2.update()
            if player.isFinished and player2.isFinished:
                state = 0
                g = open("data\lastlevel.txt", "w")
                message = f"поздравляем с завершением {str(nowlevelsel)} уровня!"
                if nowlevelsel > readed:
                    g.write(str(nowlevelsel))
                    readed = nowlevelsel
                g.close()
                for sprite in all_sprites:
                    sprite.kill()
                player.kill()
                player2.kill()
            clck1, clck2 = False, False
            for i in ice_btn_group:
                clck1 = i.updatee()
            for i in fire_btn_group:
                clck2 = i.updatee()
            if clck2 and clck1:
                for i in barrier_group:
                    i.kill()
            all_sprites.draw(screen)
            player_group.draw(screen)
            clock1.tick(60)
            pygame.display.flip()
        else:
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    running = False
                if ev.type == pygame.MOUSEBUTTONDOWN:
                    for sprite in all_sprites:
                        sprite.kill()
                    isOvered = False
                    state = 0
                    message = ""
                    gameover.rect.x = -1000
            if gameover.rect.x < 0:
                gameover.rect.x += 200 / 60
            fon_group.draw(screen)
            all_sprites.draw(screen)
            player_group.draw(screen)
            player.update(chg1=False, chg2=False)
            player2.update(chg1=False, chg2=False)
            gameover_group.draw(screen)
            clock1.tick(60)
            pygame.display.flip()
    if state == 0:
        screen.fill((128, 128, 128))
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                running = False
            if ev.type == pygame.MOUSEBUTTONDOWN:
                if ev.pos[1] in range(200, 300):
                    if ev.pos[0] in range(0, 100):
                        if nowlevelsel > 1:
                            nowlevelsel -= 1
                    if ev.pos[0] in range(200, 300):
                        if nowlevelsel < readed + 1 and readed != 5:
                            nowlevelsel += 1
                        elif readed == 5 and nowlevelsel < readed:
                            nowlevelsel += 1
                    if ev.pos[0] in range(300, 400):
                        if 0 < chr12[0]:
                            chr12[0] -= 1
                            char1.image = perss[chr12[0]]
                            if chr12[0] == chr12[1]:
                                chr12[1] += 1
                                char2.image = perss[chr12[1]]
                    if ev.pos[0] in range(500, 600):
                        if chr12[0] < readed + 1:
                            chr12[0] += 1
                            char1.image = perss[chr12[0]]
                            if chr12[0] == chr12[1]:
                                chr12[1] -= 1
                                char2.image = perss[chr12[1]]
                    if ev.pos[0] in range(600, 700):
                        if 0 < chr12[1]:
                            chr12[1] -= 1
                            char2.image = perss[chr12[1]]
                            if chr12[0] == chr12[1]:
                                chr12[0] += 1
                                char1.image = perss[chr12[0]]
                    if ev.pos[0] in range(800, 900):
                        if chr12[1] < readed + 1:
                            chr12[1] += 1
                            char2.image = perss[chr12[1]]
                            if chr12[0] == chr12[1]:
                                chr12[0] -= 1
                                char1.image = perss[chr12[0]]
                if ev.pos[1] in range(350, 450) and ev.pos[0] in range(350, 550):
                    state = 1
                    player, level_x, level_y, player2 = generate_level(levels[nowlevelsel - 1], perss[chr12[0]], perss[chr12[1]])
                if ev.pos[1] in range(50, 150):
                    if ev.pos[0] in range(100, 200):
                        state = 2
                        info = Info(False, levelnum=nowlevelsel)
                    if ev.pos[0] in range(400, 500):
                        state = 2
                        info = Info(True, chr12[0])
                    if ev.pos[0] in range(700, 800):
                        state = 2
                        info = Info(True, chr12[1])
        menu_sprites.draw(screen)
        font = pygame.font.Font(None, 100)
        font2 = pygame.font.Font(None, 50)
        text_coord = 0
        text_coord2 = 0
        string_rendered = font.render(str(nowlevelsel), 1, pygame.Color('white'))
        string_rendered2 = font2.render(message, 1, pygame.Color('red'))
        intro_rect = string_rendered.get_rect()
        text_coord += 0
        intro_rect.top = text_coord
        intro_rect.x = 125
        intro_rect.y = 225
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
        intro_rect2 = string_rendered.get_rect()
        text_coord2 += 0
        intro_rect2.top = text_coord2
        intro_rect2.x = 150
        intro_rect2.y = 600
        text_coord2 += intro_rect2.height
        screen.blit(string_rendered2, intro_rect2)
        pygame.display.flip()
    if state == 2:
        screen.fill((128, 128, 128))
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                running = False
            if ev.type == pygame.MOUSEBUTTONDOWN:
                if ev.pos[1] in range(0, 100) and ev.pos[0] in range(0, 100):
                    state = 0
                    message = ""

        info.info_sprites.draw(screen)
        pygame.display.flip()