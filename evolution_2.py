class World:
    def __init__(self):
        self.birth_rate = 1  # chance of a new spontaneously born creation
        self.creations = []

    def spontaneous_birth(self):
        self.creations.append(Creation())

    def reproduction(self):
        new_creations = []
        for creation in self.creations:
            new_creations.append(creation.reproduce())
        self.creations += new_creations


class Creation:
    def __init__(self):
        self.death_rate = 0  # chance of death is 0 %
        self.repoduction_rate = 1  # chance of reproduction is 100 %

    def reproduce(self):
        return Creation()


def main():
    days = 10
    world = World()

    print()
    print('    Day  |   Population  ')
    print('-------------------------')

    for day in range(1, days + 1):
        world.reproduction()
        world.spontaneous_birth()
        print('{:>7}  | {:>12}  '.format(day, len(world.creations)))

    print()


if __name__ == '__main__':
    main()
