import random


class Ship:
    __HEALTH = 1
    __HIT = 2

    def __init__(self, length, tp=1, x=None, y=None):
        if x != None or y != None:
            self.__check_val(x, y)
        self._x = x
        self._y = y
        self._length = length
        self._tp = tp
        self._is_move = True
        self._cells = [self.__HEALTH for _ in range(length)]
        self._path = []

    def __check_val(self, x, y):
        try:
            if not all(isinstance(obj, int) for obj in (x, y)) or not all(obj >= 0 for obj in (x, y)):
                raise TypeError("x и y должны быть положительными целыми числами")
        except TypeError as e:
            print(e)

    def get_start_coords(self):
        return self._x, self._y

    def set_start_coords(self, x, y):
        self.__check_val(x, y)
        self._x = x
        self._y = y

    def __check_step(self, val):
        try:
            if val not in (1, -1):
                raise Exception("Введите число 1 или -1")
        except Exception as e:
            print(e)

    def move(self, go):
        self.__check_step(go)
        if go == 1 and self._is_move == True:
            self._x = self._x + 1 if self._tp == 1 else self._x
            self._y = self._y + 1 if self._tp == 2 else self._y
            return self
        if go == -1 and self._is_move == True:
            self._x = self._x - 1 if self._tp == 1 else self._x
            self._y = self._y - 1 if self._tp == 2 else self._y
            return self

    def is_collide(self, ship):
        y_up_1, x_up_1 = self._y - 1, self._x - 1
        y_dw_1 = self._y + 1 if self._tp == 1 else self._y + self._length
        x_dw_1 = self._x + self._length if self._tp == 1 else self._x + 1

        y_up_2, x_up_2 = ship._y - 1, ship._x - 1
        y_dw_2 = ship._y + 1 if ship._tp == 1 else ship._y + ship._length
        x_dw_2 = ship._x + ship._length if ship._tp == 1 else ship._x + 1

        if not (y_up_1 >= y_dw_2 or y_up_2 >= y_dw_1 or x_up_1 >= x_dw_2 or x_up_2 >= x_dw_1):
            return True
        return False

    def __eq__(self, other):
        return self._length == other._length and self._tp == other._tp and self._x == other._x and self._y == other._y

    def __hash__(self):
        return hash((self._length, self._tp, self._y, self._x))

    def is_out_pole(self, size):
        is_x = tuple(range(0, size + 1 - self._length))
        is_y = tuple(range(size))
        if self._y in is_y and self._tp == 1 and self._x in is_x:
            return False
        if self._y in is_x and self._tp == 2 and self._x in is_y:
            return False
        return True

    def __getitem__(self, item):
        return self._cells[item]

    def __setitem__(self, key, value):
        self._cells[key] = value
        self._is_move = False


class GamePole:
    __POINT = 0
    __t = 0
    __s = 0
    __ships_length = (4, 3, 3, 2, 2, 2, 1, 1, 1, 1)

    def __init__(self, size=10):
        self._size = size
        self._ships = []
        self._game_pole = []

    def init(self):
        [self._ships.append(Ship(x, random.randint(1, 2))) for x in self.__ships_length]
        self._game_pole = [[self.__POINT] * self._size for _ in range(self._size)]

        while self.__t != 10:
            ship = self._ships[self.__t]
            ship._x = random.randint(0, 9)
            ship._y = random.randint(0, 9)

            if not ship.is_out_pole(self._size) and self.__t == 0:
                if ship._tp == 1:
                    for i, x in enumerate(ship._cells):
                        self._game_pole[ship._y][ship._x + i] = x
                    self.__t += 1
                else:
                    for i, x in enumerate(ship._cells):
                        self._game_pole[ship._y + i][ship._x] = x
                    self.__t += 1

                continue

            if not ship.is_out_pole(self._size):
                if all(not x.is_collide(ship) for x in self._ships if x._x != None and hash(x) != hash(ship)):
                    if ship._tp == 1:
                        for i, x in enumerate(ship._cells):
                            self._game_pole[ship._y][ship._x + i] = x
                        self.__t += 1
                    else:
                        for i, x in enumerate(ship._cells):
                            self._game_pole[ship._y + i][ship._x] = x
                        self.__t += 1

                continue

            else:
                continue

    def move_ships(self):
        while self.__s != 10:
            go = random.choice([1, -1])
            ship = self._ships[self.__s]
            if ship._is_move == False:
                self.__s += 1
                continue

            if 1 in ship._path and -1 in ship._path:
                self.__s += 1
                ship._path.clear()
                continue

            ship = ship.move(go)
            if not ship.is_out_pole(self._size) and all(
                    not x.is_collide(ship) for x in self._ships if hash(x) != hash(ship)):
                if ship._tp == 1 and go == 1:
                    self._game_pole[ship._y][ship._x - 1] = self.__POINT
                    for i, x in enumerate(ship._cells):
                        self._game_pole[ship._y][ship._x + i] = x
                    self.__s += 1
                    continue
                if ship._tp == 1 and go == -1:
                    self._game_pole[ship._y][ship._x + ship._length] = self.__POINT
                    for i, x in enumerate(ship._cells):
                        self._game_pole[ship._y][ship._x + i] = x
                    self.__s += 1
                    continue
                if ship._tp == 2 and go == 1:
                    self._game_pole[ship._y - 1][ship._x] = self.__POINT
                    for i, x in enumerate(ship._cells):
                        self._game_pole[ship._y + i][ship._x] = x
                    self.__s += 1
                    continue
                if ship._tp == 2 and go == -1:
                    self._game_pole[ship._y + ship._length][ship._x] = self.__POINT
                    for i, x in enumerate(ship._cells):
                        self._game_pole[ship._y + i][ship._x] = x
                    self.__s += 1
                    continue

            else:
                if go == 1:
                    ship._path.append(1)
                    ship.move(-1)
                    continue
                if go == -1:
                    ship._path.append(-1)
                    ship.move(1)
                    continue

    def __iter__(self):
        for x in self._game_pole:
            yield x

    def show(self):
        for x in self._game_pole:
            print(*x)

    def get_pole(self):
        return tuple(tuple(x) for x in self._game_pole)

    def get_ships(self):
        return self._ships