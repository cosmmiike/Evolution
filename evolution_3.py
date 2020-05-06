from random import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(style="darkgrid")


N_INIT = 2
N_DAYS = 80
BIRTH_RATE = 0
DEATH_RATE = 0.2
REPLICATION_RATE = 0.3


class World:
    def __init__(self):
        self.birth_rate = BIRTH_RATE  # chance of a new spontaneously born creation
        self.creations = []
        self.n_init = N_INIT

        for _ in range(self.n_init):
            self.creations.append(Creation())

    def evolve(self):
        self.spontaneous_birth()
        self.death()
        self.replication()

    def spontaneous_birth(self):
        if random() < self.birth_rate:
            self.creations.append(Creation())

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


class Creation:
    def __init__(self):
        self.death_rate = DEATH_RATE
        self.replication_rate = REPLICATION_RATE

    def replicate(self):
        if random() < self.replication_rate:
            return Creation()
        return None

    def is_dead(self):
        if random() < self.death_rate:
            return True
        return False


def show_analytics(data):
    df = pd.DataFrame(data, columns=['Day', 'Population', 'Average'])
    df.set_index('Day', inplace=True)
    sns.lineplot(data=df, ds='steps', dashes=False)
    plt.show()


def main():
    days = N_DAYS
    world = World()

    print('\n    Day  |   Population  ')
    print('-------------------------')

    data = []
    accum = 0
    for day in range(1, days + 1):
        world.evolve()
        accum += len(world.creations)
        data.append((day, len(world.creations), accum / day))
        print('{:>7}  | {:>12}  '.format(day, len(world.creations)))

    show_analytics(data)


if __name__ == '__main__':
    main()
