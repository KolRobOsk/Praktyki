import portion
from math import inf
from collections import namedtuple
import random
import math


Atomic = namedtuple('Atomic', ['left', 'lower', 'upper', 'right'])

def mylen(interval):
    '''
    Funkcja licząca długość interwału potrzebna do funkcji is_half_out\n
    :param interval: interwał do zmierzenia długości\n
    :return: długość interwału\n
    :rtype: float
    '''
    if interval == my_closed(math.inf, -math.inf) or isinstance(interval, int) or isinstance(interval, float) or interval.empty:
        return 0
    else:
        length = interval.upper - interval.lower if interval.lower > 0 else abs(interval.upper + interval.lower)
        return length

class myInterval(portion.Interval):
    '''
    Klasa dziedzicząca z funkcji interwał\n
    :param eps: liczba potrzebna do przycięcia pudełek,
    bez tego są liczone jako przecinające się nawet jak
    tylko nachodzą na siebie granicami
    '''

    def __init__(self):
        super().__init__()
        self.eps = 1e-7


    @property
    def upper_eps(self):
        '''
        Atrybut upper_eps\n
        :return: górną  granicę interwału + eps(ilon)\n
        :rtype: float
        '''
        return self.upper + self.eps if mylen(self) > 0 else self.lower

    @property
    def upper_meps(self):
        '''
        Atrybut upper_meps\n
        :return: górną  granicę interwału - eps(ilon)\n
        :rtype: float
        '''
        return self.upper - self.eps if mylen(self) > 0 else self.lower

    @property
    def lower_eps(self):
        '''
        Atrybut lower_eps\n
        :return: dolną  granicę interwału + eps(ilon)\n
        :rtype: float
        '''
        return self.lower + self.eps if mylen(self) > 0 else self.lower

    @property
    def lower_meps(self):
        '''
        Atrybut lower_meps\n
        :return: dolną  granicę interwału - eps(ilon)\n
        :rtype: float
        '''
        return self.lower - self.eps if mylen(self) > 0 else self.lower

    @lower_eps.setter
    def lower_eps(self):
        '''
        Funkcja set dla wartości lower\n
        :return: wartość lower interwału + eps(ilon)\n
        :rtype: float
        '''
        self.lower_eps = self.lower + self.eps if mylen(self) > 0 else self.lower

    @lower_meps.setter
    def lower_meps(self):
        '''
        Funkcja get dla wartości lower\n
        :return: wartość lower interwału - eps(ilon)\n
        :rtype: float
        '''
        self.lower_meps = self.lower - self.eps if mylen(self) > 0 else self.lower

    @upper_eps.setter
    def upper_eps(self):
        '''
        Funkcja set dla wartości upper\n
        :return: wartość upper interwału + eps(ilon)\n
        :rtype: float
        '''
        self.upper_eps = self.upper + self.eps if mylen(self) > 0 else self.lower

    @upper_meps.setter
    def upper_meps(self):
        '''
        Funkcja set dla wartości upper\n
        :return: wartość upper interwału - eps(ilon)\n
        :rtype: float
        '''
        self.upper_meps = self.upper - self.eps if mylen(self) > 0 else self.lower

    @lower_eps.getter
    def get_lower_eps(self):
        '''
        Funkcja get dla wartości lower\n
        :return: wartość lower_eps(ilon)\n
        :rtype: float
        '''
        return self.lower_eps

    @lower_meps.getter
    def get_lower_meps(self):
        '''
        Funkcja get dla wartości lower\n
        :return: wartość lower_meps(ilon)\n
        :rtype: float
        '''
        return self.lower_meps

    @upper_eps.getter
    def get_upper_eps(self):
        '''
        Funkcja get dla wartości upper\n
        :return: wartość upper_eps(ilon)\n
        :rtype: float
        '''
        return self.upper_eps

    @upper_meps.getter
    def get_upper_meps(self):
        '''
        Funkcja set dla wartości upper\n
        :return: wartość upper_meps(ilon)\n
        :rtype: float
        '''
        return self.upper_meps

    def box_cut_execute(self, myInt):
        '''
        Funkcja która przycina jeden interwał\n
        :param interval: interwał do przycięcia\n
        :return: interwał przycięty o epsilon z obu wartości granicznych\n
        :rtype: myInterval
        '''
        interval = my_closed(myInt.get_lower_eps, myInt.get_upper_meps) if not mylen(myInt) == 0 else myInt
        return interval

    def box_cut(self, box1):
        '''
        Funkcja przycinająca pudełko\n
        :param box1: pudełko przed przycięciem\n
        :return: pudełko po przycięciu\n
        :rtype: box3D
        '''
        x, y, z = box1.interval_x, box1.interval_y, box1.interval_z
        x = my_closed(x.lower, x.upper)
        y = my_closed(y.lower, y.upper)
        z = my_closed(z.lower, z.upper)
        x = self.box_cut_execute(x)
        y = self.box_cut_execute(y)
        z = self.box_cut_execute(z)
        box = box3D(x, y, z)
        return box

    def box_uncut_execute(self, myInt):
        '''
        Funkcja która cofa przycięcie jednego interwału\n
        :param interval: interwał przycięty o epsilon, produkt funkcji box_cut_execute\n
        :return: interwał w stanie takim samym jak przed przycięciem\n
        :rtype: myInterval
        '''
        interval = my_closed(round(myInt.lower), round(myInt.upper))
        return interval

    def box_uncut(self, box1):
        '''
        Funkcja cofająca przycięcie pudełka\n
        :param box1: pudełko, w którym chcemy cofnąć przycięcie interwałów o epsilon\n
        :return: pudełko z cofniętym przycięciem interwałów\n
        :rtype: box3D
        '''
        x, y, z = box1.interval_x, box1.interval_y, box1.interval_z
        x = my_closed(x.lower, x.upper)
        y = my_closed(y.lower, y.upper)
        z = my_closed(z.lower, z.upper)
        x = self.box_uncut_execute(x)
        y = self.box_uncut_execute(y)
        z = self.box_uncut_execute(z)
        box = box3D(x, y, z)
        return box

    @staticmethod
    def my_from_atomic(left, lower, upper, right):
        '''
    	Funkcja nadpisująca funkcję from_atomic\n
    	:return: interwał na podstawie podanych danych\n
    	:rtype: myInterval
    	'''
        instance = myInterval()
        left = left if lower not in [inf, -inf] else portion.Bound.OPEN
        right = right if upper not in [inf, -inf] else portion.const.Bound.OPEN
        instance._intervals = [Atomic(left, lower, upper, right)]
        #if instance.empty:
        #    return myInterval()
        return instance

def my_closed(lower, upper):
    '''
    Funkcja tworząca interwał zastępująca oryginalny closed\n
    :param lower: wartość lower dla nowo powstającego interwału\n
    :param upper: wartość upper dla nowo powstającego interwału\n
    :return: nowy interwał o dodanych właściwościach\n
    :rtype: myInterval
    '''
    return myInterval.my_from_atomic(portion.const.Bound.CLOSED, lower, upper, portion.const.Bound.CLOSED)


class box3D:
    '''Klasa przechowująca instrukcje dot. pudełek'''

    def __init__(self, interval_x, interval_y, interval_z):
        '''
        :param interval_x: interwał opisujący położenie pudełka na płaszczyźnie x \n
        :param interval_y: interwał opisujący położenie pudełka na płaszczyźnie y \n
        :param interval_z: interwał opisujący położenie pudełka na płaszczyźnie z \n
        Inicjalizacja z interwałami x, y, z
        '''
        self.interval_x = interval_x
        self.interval_y = interval_y
        self.interval_z = interval_z
        self.is_wall = True if sum([(mylen(interval_x) == 0), (mylen(interval_y) == 0), (mylen(interval_z) == 0)]) == 1 else False

    def set_is_wall(self):
        self.is_wall = True if sum([(mylen(self.interval_x) == 0), (mylen(self.interval_y) == 0), (mylen(self.interval_z) == 0)]) == 1 else False

    def get_is_wall(self):
        return self.is_wall

    def get_wall_xy(self, z):
        return box3D(self.interval_x, self.interval_y, my_closed(z, z))

    def get_wall_xz(self, y):
        return box3D(self.interval_x, my_closed(y, y),  self.interval_z)

    def get_wall_yz(self, x):
        return box3D( my_closed(x, x), self.interval_y, self.interval_z,)

    def get_interval_x(self):
        '''
        Funkcje get dla jednego z interwałów\n
        :return: interwał pudełka wskazujący położenie na osi x\n
        :rtype: portion.Interval
        '''
        return self.interval_x

    def get_interval_y(self):
        '''
        Funkcje get dla jednego z interwałów\n
        :return: interwał pudełka wskazujący położenie na osi y\n
        :rtype: portion.Interval
        '''
        return self.interval_y

    def get_interval_z(self):
        '''
        Funkcje get dla jednego z interwałów\n
        :return: interwał pudełka wskazujący położenie na osi z\n
        :rtype: portion.Interval
        '''
        return self.interval_z


    def __contains__(self, num):
        '''
        Funkcja sprawdzająca czy punkt jest w pudełku\n
        :param num: tablica zawierająca 3 wartości punktu sprawdzanego - x, y, z\n
        :rtype: bool
        '''
        if self.is_wall:
            if mylen(self.interval_x) == 0:
                return True if sum([(num[1] in self.interval_y), (num[2] in self.interval_z), num[0] == self.interval_x]) == 3 else False
            elif mylen(self.interval_y) == 0:
                return True if sum([(num[0] in self.interval_x), (num[2] in self.interval_z), num[1] == self.interval_y]) == 3 else False
            elif mylen(self.interval_z) == 0:
                return True if sum([(num[0] in self.interval_x), (num[1] in self.interval_y), num[2] == self.interval_z]) == 3 else False
        elif all([mylen(self.interval_x), mylen(self.interval_y), mylen(self.interval_z)]):
            return True if (num[0] in self.interval_x) & (num[1] in self.interval_y) & (num[2] in self.interval_z) else False

    def __ror__(self, num):
        '''
        Funkcja sprawdzająca czy punkt jest na granicy pudełek\n
        :param num: tablica zawierająca 3 wartości punktu sprawdzanego - x, y, z\n
        :rtype: bool
        '''
        x, y, z = num[0], num[1], num[2]
        if self.is_wall:
            if mylen(self.interval_x) == 0:
                is_on_border = True if y in set([self.interval_y.lower, self.interval_y.upper]) or \
                               z in set([self.interval_z.lower, self.interval_z.upper]) else False
            elif mylen(self.interval_y) == 0:
                is_on_border = True if x in set([self.interval_x.lower, self.interval_x.upper]) or \
                               z in set([self.interval_z.lower, self.interval_z.upper]) else False

            elif mylen(self.interval_z) == 0:
                is_on_border = True if x in set([self.interval_x.lower, self.interval_x.upper]) or \
                               y in set([self.interval_y.lower, self.interval_y.upper]) else False
        elif all([mylen(self.interval_x) != 0, mylen(self.interval_y) != 0 , mylen(self.interval_z) != 0]):
            is_on_border = x in set([self.interval_x.lower, self.interval_x.upper]) or y in set([self.interval_y.lower, self.interval_y.upper]) or z in set([self.interval_z.lower, self.interval_z.upper])
        is_inside_box = self.__contains__(num)
        return True if is_on_border & is_inside_box else False


    def __str__(self):
        '''
        Funkcja wypisująca interwały pudełka
        '''
        x = self.get_interval_x()
        y = self.get_interval_y()
        z = self.get_interval_z()
        lista = [x.lower, x.upper, y.lower, y.upper, z.lower, z.upper]
        intervals = '[' + str(lista[0]) + ',' + str(lista[1]) + ']' + ' x ' + '[' + str(lista[2]) + ',' + str(lista[3]) + ']' + ' x ' + '[' + str(lista[4]) + ',' + str(lista[5]) + ']' + '\n'
        return intervals

    @staticmethod
    def random(corner_range=100, side_range=20):
        """
        Generuje losowe pudełko, w którym interwały są determinowane przez pseudolosowe liczby całkowite z przedziału podanego przez użytkownika \n
        :param corner_range: dolna granica każdego interwału pudełka jest liczbą pseudolosową z przedziału  [0, corner_range]\n
        :param side_range: górna granica każdego interwału pudełka jest liczbą pseudolosową z przedziału [1 + corner_range, side_range + corner_range]\n
        :return: losowe pudełko\n
        :rtype: box3D
        """
        side_x, side_y, side_z = random.randint(1, side_range), random.randint(1, side_range), random.randint(1, side_range)
        corner_x, corner_y, corner_z = random.randint(0, corner_range), random.randint(0, corner_range), random.randint(0, corner_range)
        return box3D(my_closed(corner_x, corner_x + side_x), my_closed(corner_y, corner_y + side_y), my_closed(corner_z, corner_z + side_z))
        
    
    @staticmethod
    def factory(x1, y1, z1, x2, y2, z2):
        '''
        metoda statyczna tworząca pudełko na podstawie interwałów\n
        podanych w kolejności wszystkie lower, potem wszystkie upper\n
        :param x1: wartość lower dla interwału na osi x\n
        :param y1: wartość lower dla interwału na osi y\n
        :param z1: wartość lower dla interwału na osi z\n
        :param x2: wartość upper dla interwału na osi x\n
        :param y2: wartość upper dla interwału na osi y\n
        :param z2: wartość upper dla interwału na osi z\n
        :return: nowy obiekt pudełko\n
        :rtype: box3D
        '''
        return box3D(my_closed(x1, x2), my_closed(y1, y2), my_closed(z1, z2))

