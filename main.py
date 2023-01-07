import os
import sys
import random
import pygame

pygame.init()
size = width, height = 1920, 1080
screen = pygame.display.set_mode(size)
player = None
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
wall_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
snow_group = pygame.sprite.Group()
gift_group = pygame.sprite.Group()
savepoint_group = pygame.sprite.Group()
button_group = pygame.sprite.Group()
snegovik_group = pygame.sprite.Group()
level1 = []

def generate_level(level):
    new_player, x, y, new_player2 = None, None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            if level[y][x] == '#':
                if y != 0:
                    if level[y][x] == '#' and level[y - 1][x] == '#':
                        Tile('wall', x, y)
                    if level[y][x] == '#' and level[y - 1][x] != '#':
                        Tile('wall1', x, y)
                else:
                    Tile('wall', x, y)
            if level[y][x] == "s":
                Tile('empty', x, y)
                Tile("snowb", x, y)
            if level[y][x] == "g":
                Tile('empty', x, y)
                Tile("giftb", x, y)
            if level[y][x] == "q":
                SP(x, y)
            if level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y, "snow")
            if level[y][x] == '*':
                Tile('empty', x, y)
                new_player2 = Player(x, y, "gift")
            if level[y][x] == '1':
                Tile('empty', x, y)
                Button(x, y, [(17, 66)])
            if level[y][x] == '2':
                Tile('empty', x, y)
                Button(x, y, [(15, 63)])
            if level[y][x] == '3':
                Tile('empty', x, y)
                listofline = [(13, 63), (12, 64), (11, 65)]
                for i in range(66, 85):
                    listofline.append((10, i))
                Button(x, y, listofline)
            if level[y][x] == '4':
                Tile('empty', x, y)
                Button(x, y, [(17, 104), (16, 103), (15, 102), (14, 101), (14, 100), (14, 99)])
            if level[y][x] == '5':
                Tile('empty', x, y)
                listofline = [(13, 103), (12, 104), (11, 105), (10, 106)]
                for i in range(107, 127):
                    listofline.append((9, i))
                Button(x, y, listofline)
            if level[y][x] == '6':
                Tile('empty', x, y)
                Tile("snegovik", x, y)
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

tile_images = {
    'wall': load_image('box.png'),
    'wall1': load_image('box1.png'),
    'empty': load_image('grass.png'),
    'empty1': load_image('grass.png'),
    'snowb' : load_image('snowb.png'),
    "giftb": load_image('giftplace.png'),
    'button': load_image('button.png'),
    'snegovik' : load_image('snegovik.png')
}
snow_image = load_image('snowball.png')
gift_image = load_image('gift.png')
isOvered = False
tile_width = tile_height = 50


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        if tile_type not in ["wall", "wall1"]:
            self.pos_x = pos_x
            self.pos_y = pos_y
            if tile_type == "empty":
                super().__init__(tiles_group, all_sprites)
            if tile_type == "snowb":
                super().__init__(snow_group, all_sprites)
            if tile_type == "giftb":
                super().__init__(gift_group, all_sprites)
            if tile_type == "snegovik":
                super().__init__(snegovik_group, all_sprites)
            self.image = tile_images[tile_type]
            self.rect = self.image.get_rect().move(
                tile_width * pos_x, tile_height * pos_y)
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
        self.pos_x = pos_x
        self.pos_y = pos_y
        super().__init__(player_group, all_sprites)
        if player_type == "snow":
            self.image = snow_image
        if player_type == "gift":
            self.image = gift_image
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
                if self.player_type == "snow":
                    wall_group.add(player2)
                else:
                    wall_group.add(player)

                self.rect.y += 5
                if pygame.sprite.spritecollideany(self, wall_group):
                    self.isJumping = True
                    self.jumpingForce = 20
                self.rect.y -= 5
                if self.player_type == "snow":
                    wall_group.remove(player2)
                else:
                    wall_group.remove(player)
        if event.key == 97 or event.key == 1073741904:
            self.isLeft = True
        if event.key == 115 or event.key == 1073741905:
            if pygame.sprite.spritecollideany(self, button_group) != None:
                for i in pygame.sprite.spritecollideany(self, button_group).poses:
                    print(i[0] + 10)
                    n = list(level1[i[0] + 10])
                    n[i[1]] = "#"
                    level1[i[0] + 10] = "".join(n)
                return level1
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
        if self.player_type == "snow":
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
        if self.player_type == "snow":
            wall_group.remove(player2)
        else:
            wall_group.remove(player)
        if chg1 != None:
            self.isLeft = chg1
        if chg2 != None:
            self.isRight = chg2
        if pygame.sprite.spritecollideany(self, savepoint_group) != None:
            for i in range(len(level1)):
                if "@" in level1[i]:
                    level1[i] = "".join(level1[i]).replace("@", ".")
                if "*" in level1[i]:
                    level1[i] = "".join(level1[i]).replace("*", ".")
            n = list(level1[pygame.sprite.spritecollideany(self, savepoint_group).posts[1]])
            n[pygame.sprite.spritecollideany(self, savepoint_group).posts[0]] = "@"
            level1[pygame.sprite.spritecollideany(self, savepoint_group).posts[1]] = "".join(n)
            n = list(level1[pygame.sprite.spritecollideany(self, savepoint_group).posts[1] - 1])
            n[pygame.sprite.spritecollideany(self, savepoint_group).posts[0]] = "*"
            level1[pygame.sprite.spritecollideany(self, savepoint_group).posts[1] - 1] = "".join(n)
        if self.player_type == "gift":
            if pygame.sprite.spritecollideany(self, snow_group):
                return True
            else:
                return False
        else:
            if pygame.sprite.spritecollideany(self, gift_group):
                return True
            else:
                return False


class SP(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.posts = pos_x, pos_y
        super().__init__(tiles_group, savepoint_group, all_sprites)
        self.image = tile_images["empty"]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Button(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, *new_poses):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.poses = new_poses[0]
        self.posts = pos_x, pos_y
        self.type = type
        super().__init__(tiles_group, all_sprites, button_group)
        self.image = tile_images["button"]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


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
        self.dx = -(target.rect.x + target.rect.w // 2 - width // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - height // 2)



running = True
player2 = None
level1 = load_level("map1.txt")
player, level_x, level_y, player2 = generate_level(level1)
camera = Camera()
gameover_group = pygame.sprite.Group()
gameover = pygame.sprite.Sprite()
gameover.image = load_image("gameover.png")
gameover.rect = gameover.image.get_rect()
gameover_group.add(gameover)
gameover.rect.x = -1920
gameover.rect.y = 0
clock1 = pygame.time.Clock()
# изображение должно лежать в папке data
while running:
    if not(isOvered):
        screen.fill((0, 0, 0))
        # изменяем ракурс камеры
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
        camera.update(player)
        # обновляем положение всех спрайтов
        for sprite in all_sprites:
            camera.apply(sprite)
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
                gameover.rect.x = -1200
        if gameover.rect.x < 0:
            gameover.rect.x += 600 / 60
        screen.fill((0, 0, 0))
        all_sprites.draw(screen)
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                running = False
        player_group.draw(screen)
        player.update(chg1=False, chg2=False)
        player2.update(chg1=False, chg2=False)
        gameover_group.draw(screen)
        clock1.tick(60)
        pygame.display.flip()