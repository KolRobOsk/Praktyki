import portion
import math
from cut import *
from box3D import *

def mylen(interval):
    '''Funkcja licząca długość interwału potrzebna do funkcji is_half_out'''
    if interval == my_closed(math.inf, -math.inf):
        return 0
    else:
        length = interval.upper - interval.lower if interval.lower > 0 else abs(interval.upper + interval.lower)
        return length

class split:
    '''
    Klasa dzieląca pudełka
    zawiera ona 20 funkcji, z których każda rozbija pudełka
    Uwzględniłem możliwość wystąpienia half-out
    '''

    empty = my_closed(math.inf, -math.inf)

    def oI_II_oI_II_oI_II(self, box1, box2):
        x1, y1, z1 = my_closed(box1.interval_x.lower, box1.interval_x.upper), \
                     my_closed(box1.interval_y.lower, box1.interval_y.upper), \
                     my_closed(box1.interval_z.lower, box1.interval_z.upper)
        x2, y2, z2 = my_closed(box2.interval_x.lower, box2.interval_x.upper), \
                     my_closed(box2.interval_y.lower, box2.interval_y.upper), \
                     my_closed(box2.interval_z.lower, box2.interval_z.upper)
        table = [box3D(x1, y1, z1)]
        if x2 - x1 != self.empty:
            table.append(box3D(x2 - x1, y2 & y1, z2))
        if y2 - y1 != self.empty:
            table.append(box3D(x2, y2 - y1, z2))
        if z2 - z1 != self.empty:
            table.append(box3D(x1 & x2, y1 & y2, z2 - z1))
        return table

    def oI_II_oI_II_oII_I(self, box1, box2):
        x1, y1, z1 = my_closed(box1.interval_x.lower, box1.interval_x.upper), \
                     my_closed(box1.interval_y.lower, box1.interval_y.upper), \
                     my_closed(box1.interval_z.lower, box1.interval_z.upper)
        x2, y2, z2 = my_closed(box2.interval_x.lower, box2.interval_x.upper), \
                     my_closed(box2.interval_y.lower, box2.interval_y.upper), \
                     my_closed(box2.interval_z.lower, box2.interval_z.upper)
        table = [box3D(x1, y1, z1)]
        if x2 - x1 != self.empty:
            table.append(box3D(x2 - x1, y2, z2))
        if y2 - y1 != self.empty:
            table.append(box3D(x2 & x1, y2 - y1, z2))
        if z2 - z1 != self.empty:
            table.append(box3D(x1 & x2, y1 & y2, z2 - z1))
        return table

    def oI_II_oII_I_oII_I(self, box1, box2):
        x1, y1, z1 = my_closed(box1.interval_x.lower, box1.interval_x.upper), \
                     my_closed(box1.interval_y.lower, box1.interval_y.upper), \
                     my_closed(box1.interval_z.lower, box1.interval_z.upper)
        x2, y2, z2 = my_closed(box2.interval_x.lower, box2.interval_x.upper), \
                     my_closed(box2.interval_y.lower, box2.interval_y.upper), \
                     my_closed(box2.interval_z.lower, box2.interval_z.upper)
        table = [box3D(x2, y2, z2)]
        if z1 - z2 != self.empty:
            table.append(box3D(x1 & x2, y1 & y2, z1 - z2))
        if y1 - y2 != self.empty:
            table.append(box3D(x1, y1 - y2, z1))
        if x1 - x2 != self.empty:
            table.append(box3D(x1 - x2, y2 & y1, z1))
        return table

    def oII_I_oII_I_oII_I(self, box1, box2):
        x1, y1, z1 = my_closed(box1.interval_x.lower, box1.interval_x.upper), \
                     my_closed(box1.interval_y.lower, box1.interval_y.upper), \
                     my_closed(box1.interval_z.lower, box1.interval_z.upper)
        x2, y2, z2 = my_closed(box2.interval_x.lower, box2.interval_x.upper), \
                     my_closed(box2.interval_y.lower, box2.interval_y.upper), \
                     my_closed(box2.interval_z.lower, box2.interval_z.upper)
        table = [box3D(x1, y1, z1)]
        if z2 - z1 != self.empty:
            table.append(box3D(x1 & x2, y1 & y2, z2 - z1))
        if y2 - y1 != self.empty:
            table.append(box3D(x2, y2 - y1, z2))
        if x2 - x1 != self.empty:
            table.append(box3D(x2 - x1, y2 & y1, z2))
        return table

    def iI_II_iI_II_iI_II(self, box1, box2):
        x2, y2, z2 = my_closed(box2.interval_x.lower, box2.interval_x.upper), \
                     my_closed(box2.interval_y.lower, box2.interval_y.upper), \
                     my_closed(box2.interval_z.lower, box2.interval_z.upper)
        table = [box3D(x2, y2, z2)]
        return table

    def iI_II_iI_II_iII_I(self, box1, box2):
        x1, y1, z1 = my_closed(box1.interval_x.lower, box1.interval_x.upper), \
                     my_closed(box1.interval_y.lower, box1.interval_y.upper), \
                     my_closed(box1.interval_z.lower, box1.interval_z.upper)
        x2, y2, z2 = my_closed(box2.interval_x.lower, box2.interval_x.upper), \
                     my_closed(box2.interval_y.lower, box2.interval_y.upper), \
                     my_closed(box2.interval_z.lower, box2.interval_z.upper)
        table = [box3D(x2, y2, z2)]
        z = [i for i in z1 - z2]
        if len(z) == 2:
            if z[0] != self.empty and z[1] != self.empty:
                table.append(box3D(x1, y1, z[0]))
                table.append(box3D(x1, y1, z[1]))
        if len(z) != 2 or (self.empty in z):
            if z[0] != self.empty:
                table.append(box3D(x1, y1, z[0]))
            if len(z) == 2:
                if z[1] != self.empty:
                    table.append(x1, y1, z[1])
        return table

    def iI_II_iII_I_iII_I(self, box1, box2):
        x1, y1, z1 = my_closed(box1.interval_x.lower, box1.interval_x.upper), \
                     my_closed(box1.interval_y.lower, box1.interval_y.upper), \
                     my_closed(box1.interval_z.lower, box1.interval_z.upper)
        x2, y2, z2 = my_closed(box2.interval_x.lower, box2.interval_x.upper), \
                     my_closed(box2.interval_y.lower, box2.interval_y.upper), \
                     my_closed(box2.interval_z.lower, box2.interval_z.upper)
        table = [box3D(x1, y1, z1)]
        x = [i for i in x2 - x1]
        if x[0] != self.empty:
            table.append(box3D(x[0], y2, z2))
        if len(x) == 2:
            if x[1] != self.empty:
                table.append(box3D(x[1], y2, z2))
        return table

    def iII_I_iII_I_iII_I(self, box1, box2):
        x1, y1, z1 = my_closed(box1.interval_x.lower, box1.interval_x.upper), \
                     my_closed(box1.interval_y.lower, box1.interval_y.upper), \
                     my_closed(box1.interval_z.lower, box1.interval_z.upper)
        table = [box3D(x1, y1, z1)]
        return table

    def iI_II_oI_II_oII_I(self, box1, box2):
        x1, y1, z1 = my_closed(box1.interval_x.lower, box1.interval_x.upper), \
                     my_closed(box1.interval_y.lower, box1.interval_y.upper), \
                     my_closed(box1.interval_z.lower, box1.interval_z.upper)
        x2, y2, z2 = my_closed(box2.interval_x.lower, box2.interval_x.upper), \
                     my_closed(box2.interval_y.lower, box2.interval_y.upper), \
                     my_closed(box2.interval_z.lower, box2.interval_z.upper)
        table = [box3D(x2, y2, z2)]
        if z1 - z2 != self.empty:
            table.append(box3D(x1, y2 & y1, z1 - z2))
        if y1 - y2 != self.empty:
            table.append(box3D(x1, y1 - y2, z1))
        return table

    def iI_II_oI_II_oI_II(self, box1, box2):
        x1, y1, z1 = my_closed(box1.interval_x.lower, box1.interval_x.upper), \
                     my_closed(box1.interval_y.lower, box1.interval_y.upper), \
                     my_closed(box1.interval_z.lower, box1.interval_z.upper)
        x2, y2, z2 = my_closed(box2.interval_x.lower, box2.interval_x.upper), \
                     my_closed(box2.interval_y.lower, box2.interval_y.upper), \
                     my_closed(box2.interval_z.lower, box2.interval_z.upper)
        table = [box3D(x2, y2, z2)]
        if z1 - z2 != self.empty:
            table.append(box3D(x2, y1 & y2, z1 - z2))
        if y1 - y2 != self.empty:
            table.append(box3D(x1, y1 - y2, z1))
        return table

    def iI_II_oII_I_oII_I(self, box1, box2):
        x1, y1, z1 = my_closed(box1.interval_x.lower, box1.interval_x.upper), \
                     my_closed(box1.interval_y.lower, box1.interval_y.upper), \
                     my_closed(box1.interval_z.lower, box1.interval_z.upper)
        x2, y2, z2 = my_closed(box2.interval_x.lower, box2.interval_x.upper), \
                     my_closed(box2.interval_y.lower, box2.interval_y.upper), \
                     my_closed(box2.interval_z.lower, box2.interval_z.upper)
        table = [box3D(x2, y2, z2)]
        if y2 - y1 != self.empty:
            table.append(box3D(x1, y1 - y2, z1))
        if z2 - z1 != self.empty:
            table.append(box3D(x1, y1 & y2, z1 - z2))
        return table

    def iI_II_iI_II_oII_I(self, box1, box2):
        x1, y1, z1 = my_closed(box1.interval_x.lower, box1.interval_x.upper), \
                     my_closed(box1.interval_y.lower, box1.interval_y.upper), \
                     my_closed(box1.interval_z.lower, box1.interval_z.upper)
        x2, y2, z2 = my_closed(box2.interval_x.lower, box2.interval_x.upper), \
                     my_closed(box2.interval_y.lower, box2.interval_y.upper), \
                     my_closed(box2.interval_z.lower, box2.interval_z.upper)
        table = [box3D(x2, y2, z2)]
        if z1 - z2 != self.empty:
            table.append(box3D(x1, y1, z1 - z2))
        return table

    def iII_I_oI_II_oI_II(self, box1, box2):
        x1, y1, z1 = my_closed(box1.interval_x.lower, box1.interval_x.upper), \
                     my_closed(box1.interval_y.lower, box1.interval_y.upper), \
                     my_closed(box1.interval_z.lower, box1.interval_z.upper)
        x2, y2, z2 = my_closed(box2.interval_x.lower, box2.interval_x.upper), \
                     my_closed(box2.interval_y.lower, box2.interval_y.upper), \
                     my_closed(box2.interval_z.lower, box2.interval_z.upper)
        table = [box3D(x1, y1, z1)]
        if y2 - y1 != self.empty:
            table.append(box3D(x2, y2 - y1, z2))
        if z2 - z1 != self.empty:
            table.append(box3D(x2, y2 & y1, z2 - z1))
        return table

    def iII_I_oII_I_oII_I(self, box1, box2):
        x1, y1, z1 = my_closed(box1.interval_x.lower, box1.interval_x.upper), \
                     my_closed(box1.interval_y.lower, box1.interval_y.upper), \
                     my_closed(box1.interval_z.lower, box1.interval_z.upper)
        x2, y2, z2 = my_closed(box2.interval_x.lower, box2.interval_x.upper), \
                     my_closed(box2.interval_y.lower, box2.interval_y.upper), \
                     my_closed(box2.interval_z.lower, box2.interval_z.upper)
        x = [i for i in x2 - x1]
        table = [box3D(x1, y1, z1)]
        if z2 - z1 != self.empty:
            table.append(box3D(x1 & x2, y1 & y2, z2 - z1))
        if y2 - y1 != self.empty:
            table.append(box3D(x2, y2 - y1, z2))
        if x[0] != self.empty:
            box3D(x[0], y1 & y2, z2)
        if len(x) == 2:
            if x[1] != self.empty:
                box3D(x[1], y1 & y2, z2)
        return table

    def iII_I_oI_II_oII_I(self, box1, box2):
        x1, y1, z1 = my_closed(box1.interval_x.lower, box1.interval_x.upper), \
                     my_closed(box1.interval_y.lower, box1.interval_y.upper), \
                     my_closed(box1.interval_z.lower, box1.interval_z.upper)
        x2, y2, z2 = my_closed(box2.interval_x.lower, box2.interval_x.upper), \
                     my_closed(box2.interval_y.lower, box2.interval_y.upper), \
                     my_closed(box2.interval_z.lower, box2.interval_z.upper)
        table = [box3D(x1, y1, z1)]
        if z2 - z1 != self.empty:
            table.append(box3D(x2, y2 & y1, z2 - z1))
        if y2 - y1 != self.empty:
            table.append(box3D(x2, y2 - y1, z2))
        return table

    def iII_I_iII_I_oII_I(self, box1, box2):
        x1, y1, z1 = my_closed(box1.interval_x.lower, box1.interval_x.upper), \
                     my_closed(box1.interval_y.lower, box1.interval_y.upper), \
                     my_closed(box1.interval_z.lower, box1.interval_z.upper)
        x2, y2, z2 = my_closed(box2.interval_x.lower, box2.interval_x.upper), \
                     my_closed(box2.interval_y.lower, box2.interval_y.upper), \
                     my_closed(box2.interval_z.lower, box2.interval_z.upper)
        table = [box3D(x1, y1, z1)]
        if z2 - z1 != self.empty:
            table.append(box3D(x2, y2, z2 - z1))
        return table

    def iI_II_iII_I_oII_I(self, box1, box2):
        x1, y1, z1 = my_closed(box1.interval_x.lower, box1.interval_x.upper), \
                     my_closed(box1.interval_y.lower, box1.interval_y.upper), \
                     my_closed(box1.interval_z.lower, box1.interval_z.upper)
        x2, y2, z2 = my_closed(box2.interval_x.lower, box2.interval_x.upper), \
                     my_closed(box2.interval_y.lower, box2.interval_y.upper), \
                     my_closed(box2.interval_z.lower, box2.interval_z.upper)
        x = [i for i in x2 - x1]
        table = [box3D(x1, y1, z1)]
        if z2 - z1 != self.empty:
            table.append(box3D(x2 & x1, y2 & y1, z2 - z1))
        if not (self.empty in x) and (len(x) == 2):
            table.append(box3D(x[0], y2, z2))
            table.append(box3D(x[1], y2, z2))
        else:
            table.append(box3D(x2 - x1, y2, z2))
        return table

    def iI_II_iI_II_oI_II(self, box1, box2):
        x1, y1, z1 = my_closed(box1.interval_x.lower, box1.interval_x.upper), \
                     my_closed(box1.interval_y.lower, box1.interval_y.upper), \
                     my_closed(box1.interval_z.lower, box1.interval_z.upper)
        x2, y2, z2 = my_closed(box2.interval_x.lower, box2.interval_x.upper), \
                     my_closed(box2.interval_y.lower, box2.interval_y.upper), \
                     my_closed(box2.interval_z.lower, box2.interval_z.upper)
        table = [box3D(x2, y2, z2)]
        if z1 - z2 != self.empty:
            table.append(box3D(x1, y1, z1 - z2))
        return table

    def iII_I_iII_I_oI_II(self, box1, box2):
        x1, y1, z1 = my_closed(box1.interval_x.lower, box1.interval_x.upper), \
                     my_closed(box1.interval_y.lower, box1.interval_y.upper), \
                     my_closed(box1.interval_z.lower, box1.interval_z.upper)
        x2, y2, z2 = my_closed(box2.interval_x.lower, box2.interval_x.upper), \
                     my_closed(box2.interval_y.lower, box2.interval_y.upper), \
                     my_closed(box2.interval_z.lower, box2.interval_z.upper)
        table = [box3D(x1, y1, z1)]
        if z2 - z1 != self.empty:
            table.append(box3D(x2, y2, z2 - z1))
        return table

    def iI_II_iII_I_oI_II(self, box1, box2):
        x1, y1, z1 = my_closed(box1.interval_x.lower, box1.interval_x.upper), \
                     my_closed(box1.interval_y.lower, box1.interval_y.upper), \
                     my_closed(box1.interval_z.lower, box1.interval_z.upper)
        x2, y2, z2 = my_closed(box2.interval_x.lower, box2.interval_x.upper), \
                     my_closed(box2.interval_y.lower, box2.interval_y.upper), \
                     my_closed(box2.interval_z.lower, box2.interval_z.upper)
        x = [x for x in x2 - x1]
        table = [box3D(x1, y1, z1)]
        if z2 - z1 != self.empty:
            table.append(box3D(x2 & x1, y2 & y1, z2 - z1))
        if not (self.empty in x) and (len(x) == 2):
            table.append(box3D(x[0], y2, z2))
            table.append(box3D(x[1], y2, z2))
        else:
            table.append(box3D(x2 - x1, y2, z2))
        return table

    def split(self, idx_sign, tri_sign, tri_sign_i):
        '''Funkcja dobierająca właściwą funkcje rozbijającą na bazie trójki interwałów'''
        box1 = box3D(tri_sign[0], tri_sign[1], tri_sign[2])
        box2 = box3D(tri_sign_i[0], tri_sign_i[1], tri_sign_i[2])
        rozbij_dict = {
                       ('ii21', 'io21', 'io21'): self.iII_I_oII_I_oII_I,
                       ('ii12', 'io12', 'io21'): self.iI_II_oI_II_oII_I,
                       ('ii12', 'ii12', 'ii21'): self.iI_II_iI_II_iII_I,
                       ('ii12', 'ii21', 'ii21'): self.iI_II_iII_I_iII_I,
                       ('ii12', 'io12', 'io12'): self.iI_II_oI_II_oI_II,
                       ('ii12', 'io21', 'io21'): self.iI_II_oII_I_oII_I,
                       ('ii12', 'ii12', 'io21'): self.iI_II_iI_II_oII_I,
                       ('ii21', 'io12', 'io12'): self.iII_I_oI_II_oI_II,
                       ('ii21', 'io12', 'io21'): self.iII_I_oI_II_oII_I,
                       ('ii21', 'ii21', 'io21'): self.iII_I_iII_I_oII_I,
                       ('ii12', 'ii21', 'io21'): self.iI_II_iII_I_oII_I,
                       ('ii12', 'ii12', 'io12'): self.iI_II_iI_II_oI_II,
                       ('ii21', 'ii21', 'io12'): self.iII_I_iII_I_oI_II,
                       ('ii12', 'ii21', 'io12'): self.iI_II_iII_I_oI_II,
                       ('io12', 'io12', 'io12'): self.oI_II_oI_II_oI_II,
                       ('io12', 'io12', 'io21'): self.oI_II_oI_II_oII_I,
                       ('io12', 'io21', 'io21'): self.oI_II_oII_I_oII_I,
                       ('io21', 'io21', 'io21'): self.oII_I_oII_I_oII_I,
                       ('ii12', 'ii12', 'ii12'): self.iI_II_iI_II_iI_II,
                       ('ii21', 'ii21', 'ii21'): self.iII_I_iII_I_iII_I}

        split = rozbij_dict[idx_sign](box1, box2)
        return split
