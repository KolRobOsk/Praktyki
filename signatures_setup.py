from split_intervals_3D import *
from cut_box_2D import *

class signatures:

    def io12(self, interval1, interval2):
        '''
        Funkcja sprawdzająca, jaką sygnaturę nadać danej parze interwałów\n
        :param interval1: interwał pierwszy do porównania\n
        :param interval2: interwał drugi do porównania\n
        :return: True jeśli interwały są w relacji out oraz drugi interwał jest ma przedział zaczynający się wyżej\n
        :rtype: bool
        '''
        len1, len2 = (mylen(interval1), mylen(interval2))
        difference = len2 - len1 if len1 > 0 else abs(len1 + len2)
        if ((interval1.upper < interval2.upper) & (self.is_out(interval1, interval2)))| (self.is_half_out(interval1, interval2) & (difference > 0)):
            return True
        else:
            return False

    def ii12(self, interval1, interval2):
        '''
        Funkcja sprawdzająca, jaką sygnaturę nadać danej parze interwałów\n
        :param interval1: interwał pierwszy do porównania\n
        :param interval2: interwał drugi do porównania\n
        :return: True jeśli interwały są w relacji in oraz drugi interwał jest ma przedział zaczynający się wyżej\n
        :rtype: bool
        '''
        return True if (self.is_in(interval1, interval2) & (interval1.upper < interval2.upper)) else False

    def io21(self, interval1, interval2):
        '''
        Funkcja sprawdzająca, jaką sygnaturę nadać danej parze interwałów\n
        :param interval1: interwał pierwszy do porównania\n
        :param interval2: interwał drugi do porównania\n
        :return: True jeśli interwały są w relacji out oraz pierwszy interwał jest ma przedział zaczynający się wyżej\n
        :rtype: bool
        '''
        len1, len2 = (mylen(interval1), mylen(interval2))
        difference = len1 - len2 if len2 > 0 else abs(len1 + len2)
        if ((interval2.upper < interval1.upper) & (self.is_out(interval1, interval2))) | ((self.is_half_out(interval1, interval2) & (difference > 0))):
            return True
        else:
            return False

    def ii21(self, interval1, interval2):
        '''
        Funkcja sprawdzająca, jaką sygnaturę nadać danej parze interwałów\n
        :param interval1: interwał pierwszy do porównania\n
        :param interval2: interwał drugi do porównania\n
        :return: True jeśli interwały są w relacji in oraz pierwszy interwał jest ma przedział zaczynający się wyżej\n
        :rtype: bool
        '''
        len1, len2 = mylen(interval1), mylen(interval2)
        return True if self.is_in(interval1, interval2) & (len1 - len2 > 0) else False

    def get_signatures_triple(self, box1, box2):
        '''
        Funkcja zwracająca listę z trzema sygnaturami interwałów\n
        :param box1: pierwsze z pudełek, na podstawie których program dobiera zestaw sygnatur\n
        :param box2: drugie z pudełek, na podstawie których program dobiera zestaw sygnatur\n
        :return: listę sygnatur relacji położenia interwałów dla pudełek wprowadzonych\n
        :rtype: list
        '''
        x1, y1, z1, x2, y2, z2 = box1.interval_x, box1.interval_y, box1.interval_z, box2.interval_x, box2.interval_y, box2.interval_z
        signatures = [self.get_signature(x1, x2), self.get_signature(y1, y2), self.get_signature(z1, z2)]
        return signatures

    def get_signatures_double(self, wall1, wall2):
        signatures_res, cut = [], myInterval()
        wall1, wall2, sign = cut.wall_uncut(wall1), cut.wall_uncut(wall2), signatures()
        wall1, wall2 = [wall1.interval_x, wall1.interval_y, wall1.interval_z], [wall2.interval_x, wall2.interval_y, wall2.interval_z]
        where_equal = self.check_if_box_2D_equal_and_in(wall1, wall2)
        for i in range(len(wall1)):
            signatures_res.append(sign.get_signature(wall1[i], wall2[i]))
        return signatures_res, where_equal

    def check_if_box_2D_equal_and_in(self, wall1, wall2):
        try:
            where_equal = [self.ie(wall1[0], wall2[0]), self.ie(wall1[1], wall2[1]), self.ie(wall1[2], wall2[2])].index(
                True)
            where_in = [self.ii21(wall1[0], wall2[0]), self.ii21(wall1[1], wall2[1]), self.ii21(wall1[2], wall2[2])].index(
                True)
        except:
            where_equal = where_in = None
        return where_equal

    def sort_signatures(self, box1, box2, in2sorted):
        '''
        Funkcja przygotowująca pudełka do posortowania interwałów\n
        :param box1: pierwsze pudełko z nieposortowanymi interwałami\n
        :param box2: drugie pudełko z nieposortowanymi interwałami\n
        :param in2sorted: lista z kolejnością do permutowania interwałów\n
        :return: dwie listy interwałów po permutacji według zadanej kolejności\n
        :rtype: list, list
        '''
        box_tab1 = [box1.interval_x, box1.interval_y, box1.interval_z]
        box_tab2 = [box2.interval_x, box2.interval_y, box2.interval_z]
        tri_sign, tri_sign_i = self.permute_signatures(box_tab1, in2sorted), self.permute_signatures(box_tab2, in2sorted)
        return tri_sign, tri_sign_i

    def permute_signatures(self, box_tab, sort_order):
        '''
        Funkcja permutująca interwały z listy\n
        :param box_tab: lista interwałów z pudełka\n
        :param sort_order: kolejność sortowania w postaci listy np. [3, 1, 2, 0]\n
        :return: lista interwałów po permutacji\n
        :rtype: list
        '''
        box_tab = self.permute(box_tab, sort_order)
        return box_tab

    def permute(self, sortin, permutation):
        '''
        Funkcja przeprowadzająca operację permutacji\n
        :param sortin: lista zmiennych do permutacji\n
        :param permutation: permutacja\n
        :return: lista po permutacji\n
        :rtype: list
        '''
        assert len(sortin) == len(permutation)
        return [sortin[i] for i in permutation]

    def my_sort(self, inputlist):
        '''
        Funkcja sortująca sygnatury interwałów\n
        :param inputlist: lista\n
        :return: 3 listy: posortowanych sygnatur, kolejność w jakiej należy ustawić sygnatury aby uzyskać kolejność po posortowaniu oraz przywrócić kolejność sprzed sortowania
        :rtype: list        
        '''
        inputlist = zip(inputlist, range(len(inputlist)))
        aux = sorted(inputlist, key=lambda x: x[0])
        sorted2in = [aux[i][1] for i in range(len(aux))]
        list2 = zip(sorted2in, range(len(sorted2in)))
        aux1 = sorted(list2, key=lambda x: x[0])
        in2sorted = [aux1[i][1] for i in range(len(aux1))]
        sort = [aux[i][0] for i in range(len(aux))]
        return sort, in2sorted, sorted2in

    def is_in(self, interval1, interval2):
        '''
        Funkcja sprawdzająca czy interwały są w relacji in\n
        :param interval1: pierwszy z interwałów do porównania\n
        :param interval2: drugi z interwałów do porównania\n
        :return: True jeśli pudełka są w relacji in, inaczej False\n
        :rtype: bool
        '''
        union = interval1 & interval2
        return True if ((union.lower == interval1.lower and union.upper == interval1.upper) or (union.lower == interval2.lower and union.upper == interval2.upper)) else False


    def is_equal(self, interval1, interval2):
        '''
        Funkcja sprawdzająca czy interwały są w relacji equal\n
        :param interval1: pierwszy z interwałów do porównania\n
        :param interval2: drugi z interwałów do porównania\n
        :return: True jeśli pudełka są w relacji equal, inaczej False\n
        :rtype: bool
        '''
        return True if interval1 == interval2 else False


    def is_out(self, interval1, interval2):
        '''
        Funkcja sprawdzająca czy interwały są w relacji out\n
        :param interval1: pierwszy z interwałów do porównania\n
        :param interval2: drugi z interwałów do porównania\n
        :return: True jeśli pudełka są w relacji out, inaczej False\n
        :rtype: bool
        '''
        cond_1 = True if (interval1.lower > interval2.lower) and (interval2.upper < interval1.upper) and (interval1 & interval2) else False
        cond_2 = True if (interval1.lower < interval2.lower) and (interval2.upper > interval1.upper) and (interval1 & interval2) else False
        return True if cond_1 or cond_2 else False


    def is_separate(self, int1, int2):
        '''
        Funkcja sprawdzająca czy interwały są w relacji separate\n
        :param interval1: pierwszy z interwałów do porównania\n
        :param interval2: drugi z interwałów do porównania\n
        :return: True jeśli pudełka są w relacji separate, inaczej False\n
        :rtype: bool
        '''
        intersect = int1 & int2
        return True if mylen(intersect) == 0 else False

    def is_half_out(self, int1, int2):
        '''
        Funkcja sprawdzająca czy interwały są w relacji half out\n
        :param interval1: pierwszy z interwałów do porównania\n
        :param interval2: drugi z interwałów do porównania\n
        :return: True jeśli pudełka są w relacji half out, inaczej False\n
        :rtype: bool
        '''
        return True if (int1.lower == int2.lower) ^ (int2.upper == int1.upper) else False

    def ie(self, interval1, interval2):
        '''
        Funkcja sprawdzająca, jaką sygnaturę nadać danej parze interwałów\n
        :param interval1: pierwszy z interwałów do porównania\n
        :param interval2: drugi z interwałów do porównania\n
        :return: True jeśli pudełka są w relacji equal, inaczej False\n
        :rtype: bool
        '''
        return True if self.is_equal(interval1, interval2) else False

    def get_signature(self, interval1, interval2):
        '''
        Funkcja nadająca sygnatury parom interwałów\n
        :param interval1: pierwszy z interwałów do porównania\n
        :param interval2: drugi z interwałów do porównania\n
        :return: sygnaturę zależnie od relacji porównywanych interwałów\n
        :rtype: string
        '''
        if self.ii12(interval1, interval2):
            return 'ii12'
        if self.ii21(interval1, interval2):
            return 'ii21'
        if self.io12(interval1, interval2):
            return 'io12'
        if self.io21(interval1, interval2):
            return 'io21'
        if self.ie(interval1, interval2):
            return 'ii12'


    def ret_original_order(self, split, sorted2in):
        '''
        Funkcja przywracająca oryginalny porządek interwałów\n
        :param split: lista posortowanych interwałów\n
        :param sorted2in: kolejność docelowej permutacji\n
        :return: listę pudełek z posortowanymi interwałami\n
        :rtype: list
        '''
        table = []
        for i in split:
            j = [i.interval_x, i.interval_y, i.interval_z]
            perm = self.permute_signatures(j, sorted2in)
            table.append(box3D(perm[0], perm[1], perm[2]))
        return table