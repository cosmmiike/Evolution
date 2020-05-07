from random import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(style="darkgrid")


N_DAYS = 120
DEATH_RATE = 0.2
REPLICATION_RATE = 0.3

BLUE_I = 1
BLUE_B = 1
BLUE_D = 0.1
BLUE_R = 0.05
BLUE_M_G = 0.01
BLUE_M_R = 0.01

GREEN_I = 0
GREEN_B = 0
GREEN_D = 0.1
GREEN_R = 0.05

RED_I = 0
RED_B = 0
RED_D = 0.05
RED_R = 0.05
RED_M_O = 0.05

ORANGE_I = 0
ORANGE_B = 0
ORANGE_D = 0.05
ORANGE_R = 0.1


class World:
    def __init__(self):
        self.blue_birth_rate = BLUE_B
        self.green_birth_rate = GREEN_B
        self.red_birth_rate = RED_B

        self.blue_init = BLUE_I
        self.green_init = GREEN_I
        self.red_init = RED_I

        self.creations = []

        for _ in range(self.blue_init):
            self.creations.append(BlueCreation())

    def evolve(self):
        self.spontaneous_birth()
        self.death()
        self.replication()
        self.mutation()

    def spontaneous_birth(self):
        if random() < self.blue_birth_rate:
            self.creations.append(BlueCreation())
        if random() < self.green_birth_rate:
            self.creations.append(GreenCreation())
        if random() < self.red_birth_rate:
            self.creations.append(RedCreation())

    def death(self):
        for creation in self.creations:
            if creation.is_dead():
                self.creations.remove(creation)

    def replication(self):
        new_creations = []
        for creation in self.creations:
            baby = creation.replicate()
            if baby is not None:
                new_creations.append(baby)
        self.creations += new_creations

    def mutation(self):
        new_creations = []
        for creation in self.creations:
            baby = creation.mutate()
            if baby is not None:
                new_creations.append(baby)
        self.creations += new_creations


class Creation:
    def __init__(self):
        self.death_rate = DEATH_RATE
        self.replication_rate = REPLICATION_RATE

    def is_dead(self):
        if random() < self.death_rate:
            return True
        return False

    def replicate(self):
        pass

    def mutate(self):
        pass


class BlueCreation(Creation):
    def __init__(self):
        super().__init__()
        self.death_rate = BLUE_D
        self.replication_rate = BLUE_R
        self.mutation_rate_green = BLUE_M_G
        self.mutation_rate_red = BLUE_M_R
        self.color = 'blue'

    def replicate(self):
        if random() < self.replication_rate:
            return BlueCreation()
        return None

    def mutate(self):
        if random() < self.mutation_rate_green:
            return GreenCreation()
        if random() < self.mutation_rate_red:
            return RedCreation()
        return None



class GreenCreation(Creation):
    def __init__(self):
        super().__init__()
        self.death_rate = GREEN_D
        self.replication_rate = GREEN_R
        self.color = 'green'

    def replicate(self):
        if random() < self.replication_rate:
            return GreenCreation()
        return None


class RedCreation(Creation):
    def __init__(self):
        super().__init__()
        self.death_rate = RED_D
        self.replication_rate = RED_R
        self.color = 'red'
        self.mutation_rate_orange = RED_M_O

    def replicate(self):
        if random() < self.replication_rate:
            return RedCreation()
        return None

    def mutate(self):
        if random() < self.mutation_rate_orange:
            return OrangeCreation()
        return None


class OrangeCreation(Creation):
    def __init__(self):
        super().__init__()
        self.death_rate = ORANGE_D
        self.replication_rate = ORANGE_R
        self.color = 'orange'

    def replicate(self):
        if random() < self.replication_rate:
            return OrangeCreation()
        return None


def show_analytics(data):
    df = pd.DataFrame(data, columns=['Day', 'Population', 'Average', 'Blue', 'Green', 'Red', 'Orange'])
    df.set_index('Day', inplace=True)
    print(df.head(30))

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
        data.append((day, len(world.creations), accum / day,
                     len([cr for cr in world.creations if cr.color == 'blue']),
                     len([cr for cr in world.creations if cr.color == 'green']),
                     len([cr for cr in world.creations if cr.color == 'red']),
                     len([cr for cr in world.creations if cr.color == 'orange'])))
        print('{:>7}  | {:>12}  '.format(day, len(world.creations)))

    show_analytics(data)


if __name__ == '__main__':
    main()
