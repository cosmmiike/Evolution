from random import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(style="darkgrid")


class World:
    def __init__(self):
        self.birth_rate = 1  # chance of a new spontaneously born creation is 100 %
        self.creations = []

    def evolve(self):
        self.spontaneous_birth()
        self.replication()
        self.death()

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
        self.death_rate = 0.1  # chance of death is set to 10 %
        self.repoduction_rate = 0  # chance of replication is set to 0

    def replicate(self):
        if random() < self.repoduction_rate:
            return Creation()
        return None

    def is_dead(self):
        if random() < self.death_rate:
            return True
        return False


def show_analytics(data):
    df = pd.DataFrame(data, columns=['Day', 'Population', 'Average'])
    df.set_index('Day', inplace=True)
    sns.lineplot(data=df)
    plt.show()


def main():
    days = 365
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
