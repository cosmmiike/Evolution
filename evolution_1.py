class World:
    def __init__(self):
        self.birth_rate = 1
        self.creations = []

    def spontaneous_birth(self):
        self.creations.append(Creation())


class Creation:
    def __init__(self):
        self.death_rate = 0


def main():
    days = 10
    world = World()

    print()
    print('    Day  |   Population  ')
    print('-------------------------')

    for day in range(1, days + 1):
        world.spontaneous_birth()
        print('{:>7}  | {:>12}  '.format(day, len(world.creations)))

    print()


if __name__ == '__main__':
    main()
