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
player_group = pygame.sprite.Group()
tile_images = {
    'wall': load_image('brick.png'),
    "stairs": load_image("stair.png"),
    "key": load_image("key.png"),
    "ice": load_image("ice.png"),
    "fire": load_image("fire.png"),
    "keyhole": load_image("keyhole.png"),
    'portal': load_image("portal.png")
}
hydro_image = load_image('hydro.png')
electro_image = load_image('electroman.png')
pyro_image = load_image('fireman.png')
cryo_image = load_image('krioman.png')
anemo_image = load_image('anemoman.png')
geo_image = load_image('geoman.png')
dendro_image = load_image('geoman.png')
perss = [hydro_image, pyro_image, cryo_image, anemo_image, geo_image, electro_image]
stairs_group = pygame.sprite.Group()
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
    intro_text = ["ЗАСТАВКА", "",
                  "Правила игры",
                  "Если в правилах несколько строк,",
                  "приходится выводить их построчно"]

    fon = pygame.transform.scale(load_image('fon.jpg'), (width, height  ))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
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


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        if tile_type != "wall":
            self.pos_x = pos_x
            self.pos_y = pos_y
            self.image = tile_images[tile_type]
            self.rect = self.image.get_rect().move(
                tile_width * pos_x, tile_height * pos_y)
            if tile_type == "stairs":
                super().__init__(stairs_group, tiles_group, all_sprites)
            elif tile_type == "key":
                super().__init__(key_group, tiles_group, all_sprites)
            elif tile_type == "ice":
                super().__init__(ice_group, tiles_group, all_sprites)
            elif tile_type == "fire":
                super().__init__(fire_group, tiles_group, all_sprites)
            elif tile_type == "keyhole":
                super().__init__(keyhole_group, wall_group, tiles_group, all_sprites)
            elif tile_type == "portal":
                super().__init__(portal_group, tiles_group, all_sprites)
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
        self.hasKey = False
        self.pos_x = pos_x
        self.pos_y = pos_y
        super().__init__(player_group, all_sprites)
        if player_type == "hydro":
            self.image = hydro_image
        if player_type == "electro":
            self.image = electro_image
        self.player_type = player_type
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)
        self.isRight = False
        self.isLeft = False
        self.isJumping = False
        self.jumpingForce = 0

    def move(self, event):
        if event.key == 119 or event.key == 1073741906:
            if not(self.isJumping):
                if self == player:
                    wall_group.add(player2)
                else:
                    wall_group.add(player)
                self.rect.y += 5
                if pygame.sprite.spritecollideany(self, wall_group):
                    self.isJumping = True
                    self.jumpingForce = 20
                self.rect.y -= 5
                if self == player:
                    wall_group.remove(player2)
                else:
                    wall_group.remove(player)
        if event.key == 97 or event.key == 1073741904:
            self.isLeft = True
        if event.key == 115 or event.key == 1073741905:
            pass
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
        if self == player:
            wall_group.add(player2)
        else:
            wall_group.add(player)
        if self.isLeft:
            self.rect.x -= 5
            if pygame.sprite.spritecollideany(self, wall_group):
                self.rect.x += 5
        if self.isRight:
            self.rect.x += 5
            if pygame.sprite.spritecollideany(self, wall_group):
                self.rect.x -= 5
        if self.isJumping:
            if pygame.sprite.spritecollideany(self, stairs_group):
                self.jumpingForce = 0
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
            self.hasKey = True
            pygame.sprite.spritecollideany(self, key_group).kill()
        self.rect.y += 5
        self.rect.x += 5
        if pygame.sprite.spritecollideany(self, keyhole_group):
            if self.hasKey:
                pygame.sprite.spritecollideany(self, keyhole_group).kill()
        self.rect.y -= 10
        self.rect.x -= 10
        if pygame.sprite.spritecollideany(self, keyhole_group):
            if self.hasKey:
                pygame.sprite.spritecollideany(self, keyhole_group).kill()
        self.rect.y += 5
        self.rect.x += 5
        if pygame.sprite.spritecollideany(self, portal_group):
            pass


running = True
player2 = None
level1 = load_level("lvl1.txt")
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
player, level_x, level_y, player2 = generate_level(level1, "hydro", "electro")
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
nowlevelsel = int(g.read()) + 1
fon_group = pygame.sprite.Group()
fon = pygame.sprite.Sprite()
fon.image = load_image("fon.jpg")
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
while running:
    if state == 1:
        if not(isOvered):
            fon_group.draw(screen)
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    running = False
                if ev.type == pygame.KEYDOWN:
                    if ev.key in [97, 100, 119, 115]:
                        g = player.move(ev)
                        if g != None:
                            for j in all_sprites:
                                j.kill()
                            player, level_x, level_y, player2 = generate_level(g)
                    else:
                        g = player2.move(ev)
                        if g != None:
                            for j in all_sprites:
                                j.kill()
                            player, level_x, level_y, player2 = generate_level(g)
                if ev.type == pygame.KEYUP:
                    if ev.key in [97, 100, 119, 115]:
                        player.stopmove(ev)
                    else:
                        player2.stopmove(ev)
            isOvered1 = player.update()
            isOvered2 = player2.update()
            isOvered = isOvered1 or isOvered2
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
                    player, level_x, level_y, player2 = generate_level(level1)
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
        menu_sprites.draw(screen)
        font = pygame.font.Font(None, 100)
        text_coord = 0
        string_rendered = font.render(str(nowlevelsel), 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 0
        intro_rect.top = text_coord
        intro_rect.x = 125
        intro_rect.y = 225
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
        pygame.display.flip()