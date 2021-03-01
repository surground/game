import random
import pygame
import os
import sys

pygame.init()
size = height, width = 800, 600
screen = pygame.display.set_mode(size)
pygame.display.set_caption("'BusketDaydreamin'")
pygame.mixer.music.load('music.mp3')
pygame.mixer.music.play(-1)
SCORE = 0
some_text = list()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
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


def sort_list_of_achievements():
    file = open('achievements.txt', 'r')
    reader = file.read().splitlines()
    reader = reversed(sorted(reader, key=lambda x: int(x.split()[-1])))
    file.close()
    file = open('achievements.txt', 'w')
    for i in reader:
        file.write(f'{i}\n')
    file.close()


def save_achievement(total_score):
    with open('achievements.txt', 'a') as file:
        file.write(f'Игрок - {total_score}\n')


class EndScreen(pygame.sprite.Sprite):
    image = pygame.transform.scale(load_image('end_screen.png'), size)

    def __init__(self, *group):
        super().__init__(*group)
        self.image = EndScreen.image
        self.rect = self.image.get_rect()
        self.rect.y = -height
        self.stop = False

    def update(self):
        if self.rect.y + height < height:
            self.rect = self.rect.move(0, 10)
        else:
            for j, i in enumerate(some_text):
                text_2 = font.render('GAME OVER', True, pygame.Color('pink'))
                text_3 = font.render(str(j + 1) + '.' + i, True, pygame.Color('pink'))
                self.image.blit(text_3, (50, 410 + j * 30))
                self.image.blit(text_2, (300, 100))


class Land(pygame.sprite.Sprite):
    image = pygame.transform.scale(load_image("fon.jpg"), size)

    def __init__(self, *group):
        super().__init__(*group)
        self.image = Land.image
        self.rect = self.image.get_rect()


class Player(pygame.sprite.Sprite):
    image = pygame.transform.scale(load_image('busket.png'), (75, 43))

    def __init__(self, *group, fruit_group):
        super().__init__(*group)
        self.image = Player.image
        self.death = False
        self.rect = self.image.get_rect()
        self.rect.x = 400
        self.fruit_group = fruit_group
        self.rect.y = 470
        self.health = 5
        self.speed = 10

    def go_right(self):
        self.rect = self.rect.move(self.speed, 0)

    def go_left(self):
        self.rect = self.rect.move(-self.speed, 0)

    def update(self):
        global SCORE
        if self.health <= 0:
            self.death = True
        elif pygame.sprite.spritecollideany(self, self.fruit_group):
            pygame.sprite.spritecollide(self, self.fruit_group, True)
            SCORE += 1


class FallingFruit(pygame.sprite.Sprite):
    image_of_banana = pygame.transform.scale(load_image('banana.png'), (40, 40))
    image_of_pineapple = pygame.transform.scale(load_image('pineapple.png'), (40, 40))
    image_of_pear = pygame.transform.scale(load_image('pear.png'), (40, 40))
    count = 0

    def __init__(self, *group):
        super().__init__(*group)
        self.speed = 3
        self.image = random.choice(
            [FallingFruit.image_of_banana, FallingFruit.image_of_pineapple, FallingFruit.image_of_pear])
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, 700)
        self.rect.y = -50

    def update(self):
        self.rect = self.rect.move(0, self.speed)
        if self.rect.y > height:
            player.health -= 1
            self.kill()


all_sprites = pygame.sprite.Group()
fruit_group = pygame.sprite.Group()
fon_group = pygame.sprite.Group()
mountain = Land(all_sprites)
player = Player(all_sprites, fruit_group=fruit_group)
time = pygame.time.Clock()
count = 0
running = True
font = pygame.font.SysFont('comicsansms', 30)

while running:
    for event in pygame.event.get():
        if pygame.key.get_pressed()[pygame.K_d]:
            player.go_right()
        if pygame.key.get_pressed()[pygame.K_a]:
            player.go_left()
        if event.type == pygame.QUIT:
            running = False
        if pygame.time.get_ticks() > 10000 and count % 30 == 0:
            fruit = FallingFruit(fruit_group)
        elif count % 40 == 0:
            fruit = FallingFruit(fruit_group)
        count += 1
    if player.death:
        running = False
    text = font.render(f'Очки: {SCORE}', True, pygame.Color('#C0C0C0'))
    all_sprites.draw(screen)
    fruit_group.draw(screen)
    fruit_group.update()
    all_sprites.update()
    screen.blit(text, (10, 10))
    pygame.display.flip()
    time.tick(50)


all_sprites = pygame.sprite.Group()
end_screen = EndScreen(all_sprites)
save_achievement(SCORE)
sort_list_of_achievements()
run = True
pygame.mixer.music.load('final.mp3')
pygame.mixer.music.play(-1)
with open('achievements.txt', 'r') as file:
    reader = file.read().splitlines()
    for i in reader:
        some_text.append(i)
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    all_sprites.draw(screen)
    all_sprites.update()
    pygame.display.flip()
    time.tick(50)

if __name__ == '__main__':
    pygame.quit()
