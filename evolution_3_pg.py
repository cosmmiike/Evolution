from random import random
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(style="darkgrid")

import pygame
from pygame.locals import *
from random import randrange
import os


N_INIT             = 0
N_DAYS             = 10
BIRTH_RATE         = 1
DEATH_RATE         = 0
REPLICATION_RATE   = 0
SCREENRECT         = Rect(0, 0, 640, 480)

main_dir = os.path.split(os.path.abspath(__file__))[0]


class World:
    def __init__(self):
        self.birth_rate = BIRTH_RATE  # chance of a new spontaneously born creation
        self.creations = []
        self.creations_group = pygame.sprite.Group()
        self.n_init = N_INIT

        for _ in range(self.n_init):
            self.creations.append(Creation())

    def evolve(self):
        self.spontaneous_birth()
        self.death()
        self.replication()

    def spontaneous_birth(self):
        if random() < self.birth_rate:
            creation = Creation()
            while pygame.sprite.spritecollide(creation, self.creations_group, False):
                creation = Creation()
            self.creations_group.add(creation)
            self.creations.append(creation)

    def replication(self):
        new_creations = []
        for creation in self.creations:
            baby = creation.replicate()
            if baby is not None:
                new_creations.append(baby)
        self.creations += new_creations

    def death(self):
        for creation in self.creations:
            if creation.is_dead():
                self.creations.remove(creation)


class Creation(pygame.sprite.Sprite):
    images = ''

    def __init__(self):
        super().__init__()
        self.death_rate = DEATH_RATE
        self.replication_rate = REPLICATION_RATE
        self.image = load_image("nusha.png")
        self.rect = self.image.get_rect()
        self.rect.x = randrange(SCREENRECT.width - self.rect.width)
        self.rect.y = randrange(SCREENRECT.height - self.rect.height)

    def replicate(self):
        if random() < self.replication_rate:
            return Creation()
        return None

    def is_dead(self):
        if random() < self.death_rate:
            return True
        return False


def load_image(file):
    "loads an image, prepares it for play"
    file = os.path.join(main_dir, 'data', file)
    try:
        surface = pygame.image.load(file)
    except pygame.error:
        raise SystemExit('Could not load image "%s" %s'%(file, pygame.get_error()))
    return surface.convert()


def load_images(*files):
    imgs = []
    for file in files:
        imgs.append(load_image(file))
    return imgs


def show_analytics(data):
    df = pd.DataFrame(data, columns=['Day', 'Population', 'Average'])
    df.set_index('Day', inplace=True)
    sns.lineplot(data=df, ds='steps', dashes=False)
    plt.show()


def main():
    pygame.init()
    screen = pygame.display.set_mode(SCREENRECT.size)
    running = True

    days = N_DAYS
    world = World()

    print('\n    Day  |   Population  ')
    print('-------------------------')

    data = []
    accum = 0
    day = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pass
        world.evolve()
        day += 1
        if day == 10:
            running = False
        accum += len(world.creations)
        data.append((day, len(world.creations), accum / day))
        print('{:>7}  | {:>12}  '.format(day, len(world.creations)))
        screen.fill((0, 0, 0))
        world.creations_group.draw(screen)
        pygame.display.flip()
        pygame.time.wait(300)

    show_analytics(data)
    pygame.time.wait(10000)
    pygame.quit()


if __name__ == '__main__':
    main()
