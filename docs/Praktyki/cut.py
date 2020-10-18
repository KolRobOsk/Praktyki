import portion

#klasa przechowująca instrukcje dot. pudełek
class box3D:

    #inicjalizacja z interwałami x, y, z
    def __init__(self, interval_x, interval_y, interval_z):
        self.interval_x = interval_x
        self.interval_y = interval_y
        self.interval_z = interval_z

    #funkcje get dla każdego z interwałów
    def get_interval_x(self):
        return self.interval_x

    def get_interval_y(self):
        return self.interval_y

    def get_interval_z(self):
        return self.interval_z

    #funkcja sprawdzająca czy punkt jest w pudełku
    def __contains__(self, num):
        return True if (num[0] in self.interval_x) & (num[1] in self.interval_y) & (num[2] in self.interval_z) else False

    #funkcja sprawdzająca czy punkt jest na granicy pudełek
    def __ror__(self, num):
        x, y, z = num[0], num[1], num[2]
        is_on_border = x in set([self.interval_x.lower, self.interval_x.upper]) or y in set([self.interval_y.lower, self.interval_y.upper]) or z or set([self.interval_z.lower, self.interval_z.upper])
        is_inside_box = self.__contains__(num)
        return True if is_on_border & is_inside_box else False

    #metoda statyczna tworząca pudełko na podstawie interwałów
    #podanych w kolejności wszystkie lower, potem wszystkie upper
    @staticmethod
    def factory(x1, y1, z1, x2, y2, z2):
        return box3D(portion.closed(x1, x2), portion.closed(y1, y2), portion.closed(z1, z2))

#funkcja tworząca interwał zastępująca oryginalny closed
def my_closed(lower, upper):
    return myInterval.from_atomic(portion.const.Bound.CLOSED, lower, upper, portion.const.Bound.CLOSED)

#rozszerzona funkcja dziedzicząca z funkcji interwał
class myInterval(portion.Interval):
    '''
    epsilon - liczba potrzebna do przycięcia pudełek,
    bez tego są liczone jako przecinające się nawet jak
    tylko nachodzą na siebie granicami
    '''
    eps = 1e-7

    '''
    funkcje deklarujące, gettery i settery
    granic interwałów
    '''
    @property
    def upper_eps(self):
        return self.upper + self.eps

    @property
    def upper_meps(self):
        return self.upper - self.eps

    @property
    def lower_eps(self):
        return self.lower + self.eps

    @property
    def lower_meps(self):
        return self.lower - self.eps


    @lower_eps.setter
    def lower_eps(self):
        self.lower_eps = self.lower + self.eps

    @lower_meps.setter
    def lower_meps(self):
        self.lower_meps = self.lower + self.eps

    @upper_eps.setter
    def upper_eps(self):
        self.upper_eps = self.upper + self.eps

    @upper_meps.setter
    def upper_meps(self):
        self.upper_meps = self.upper + self.eps


    @lower_eps.getter
    def get_lower_eps(self):
        return self.lower_eps

    @lower_meps.getter
    def get_lower_meps(self):
        return self.lower_meps

    @upper_eps.getter
    def get_upper_eps(self):
        return self.upper_eps

    @upper_meps.getter
    def get_upper_meps(self):
        return self.upper_meps

    #funkcja która przycina 1 interwał
    def box_cut_execute(self, interval):
        myInt = myInterval(interval)
        interval = my_closed(myInt.get_lower_eps, myInt.get_upper_meps)
        return interval

    #funkcja przycinająca pudełko
    def box_cut(self, box1):
        x = self.box_cut_execute(box1.interval_x)
        y = self.box_cut_execute(box1.interval_y)
        z = self.box_cut_execute(box1.interval_z)
        box = box3D(x, y, z)
        return box

    #funkcja która cofa przycięcie 1 interwału
    def box_uncut_execute(self, interval):
        myInt = myInterval(interval)
        interval = my_closed(myInt.get_lower_meps, myInt.get_upper_eps)
        return interval

    #funkcja cofająca przycięcie pudełka
    def box_uncut(self, box1):
        x = self.box_uncut_execute(box1.interval_x)
        y = self.box_uncut_execute(box1.interval_y)
        z = self.box_uncut_execute(box1.interval_z)
        box = box3D(x, y, z)
        return box
