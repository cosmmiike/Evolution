from random import random

class World:
    def __init__(self):
        self.birth_rate = 1  # chance of a new spontaneously born creation
        self.creations = []

    def evolve(self):
        self.reproduction()
        self.death()
        self.spontaneous_birth()

    def spontaneous_birth(self):
        if random() < self.birth_rate:
            self.creations.append(Creation())

    def reproduction(self):
        new_creations = []
        for creation in self.creations:
            baby = creation.reproduce()
            if baby is not None:
                new_creations.append(baby)
        self.creations += new_creations

    def death(self):
        for creation in self.creations:
            if creation.is_dead():
                self.creations.remove(creation)


class Creation:
    def __init__(self):
        self.death_rate = 0.5  # chance of death is set to 50 %
        self.repoduction_rate = 0.5  # chance of reproduction is set to 50 %

    def reproduce(self):
        if random() < self.repoduction_rate:
            return Creation()
        return None

    def is_dead(self):
        if random() < self.death_rate:
            return True
        return False


def main():
    days = 10
    world = World()

    print()
    print('    Day  |   Population  ')
    print('-------------------------')

    for day in range(1, days + 1):
        world.evolve()
        print('{:>7}  | {:>12}  '.format(day, len(world.creations)))

    print()


if __name__ == '__main__':
    main()
