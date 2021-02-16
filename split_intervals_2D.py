from signatures_setup import *

class split_2D:

    #####DODAĆ DO IN IN ROZBIJANIE DLA MNIEJSZEGO PUDEŁKA O WIĘKSZYM 3cim interwale

    def iI_II_iI_II(self, wall1, wall2):
        res = [[[wall1[0][0] | wall2[0][0], wall1[0][1] | wall2[0][1], wall1[0][2] | wall2[0][2]]]]
        return res

    def iI_II_iII_I(self, wall1, wall2):
        if signatures().is_equal(wall1[0][1], wall2[0][1]) or signatures().is_equal(wall2[0][0], wall1[0][0]):
            return self.iI_II_iI_II(wall1, wall2)
        else:
            y1, x2 = [i for i in wall1[0][1] - wall2[0][1]], [i for i in wall2[0][0] - wall1[0][0]]
            my_int = myInterval()
            res = [[[my_int.cut_right(x2[0]), wall2[0][1], wall2[0][2]], [my_int.cut_left(x2[1]), wall2[0][1], wall2[0][2]],
                    [wall1[0][0], my_int.cut_right(y1[0]), wall1[0][2]], [wall1[0][0], my_int.cut_left(y1[1]), wall1[0][2]],
                    [wall1[0][0] & wall2[0][0], wall1[0][1] & wall2[0][1], wall1[0][2] | wall2[0][2]]]]
            return res

    def iI_II_oI_II(self, wall1, wall2):
        my_int = myInterval
        if signatures().is_half_out(wall1[0][1], wall2[0][1]):
            res = self.iI_II_iI_II(wall1, wall2)
        elif mylen(wall1[0][2]) > mylen(wall2[0][2]):
            x1 = [i for i in wall1[0][0] - wall2[0][0]]
            res = [[[wall1[0][0], my_int.cut_right(wall1[0][1]), wall1[0][2]],
                    [wall2[0][0], wall2[0][1] - wall1[0][1], wall2[0][2]],
                    [x1[0], wall1[0][1] & wall2[0][1], wall1[0][0]],
                    [x1[1], wall1[0][1] & wall2[0][1], wall1[0][0]]]]
        else:
            res = [[wall2[0], [wall1[0], my_int.cut_right(wall1[0][1] - wall2[0][1]), wall1[0][2]]]]
        return res

    def iII_I_iII_I(self, wall1, wall2):
        res = [[[wall1[0][0] | wall2[0][0], wall1[0][1] | wall2[0][1], wall1[0][2] | wall2[1][2]]]]
        return res

    def iI_II_oII_I(self, wall1, wall2):
        if signatures().is_half_out(wall1[0][1], wall2[0][1]):
            res = self.iI_II_iI_II(wall1, wall2)
        else:
            my_int = myInterval()
            if mylen(wall2[0][2]) > mylen(wall1[0][2]):
                res = [[[wall1[0][0], my_int.cut_left(wall1[0][1] - wall2[0][1]), wall1[0][2]],
                        [wall2[0][0], wall2[0][1], wall2[0][2]]]]
            else:
                x2 = [box for box in wall2[0][1] - wall1[0][1]]
                res = [[wall1[0], [wall2[0][0], my_int.cut_right(wall2[0][1] - wall1[0][1]), wall2[0][2]],
                        [x2[0], wall2[0][1], wall2[0][2]], [x2[1], wall2[0][1], wall2[0][2]]]]
        return res

    def iII_I_oI_II(self, wall1, wall2):
        if signatures().is_half_out(wall1[0][1], wall2[0][1]):
            res = self.iI_II_iI_II(wall1, wall2)
        else:
            my_int = myInterval()
            if mylen(wall1[0][2]) > mylen(wall2[0][2]):
                res = [[[wall2[0][0], my_int.cut_left(wall2[0][1] - wall1[0][1]), wall2[0][2]],
                        [wall1[0][0], wall1[0][1], wall1[0][2]]]]
            else:
                x1 = [box for box in wall1[0][1] - wall2[0][1]]
                res = [[wall2[0], [wall1[0][0], my_int.cut_right(wall1[0][1] - wall2[0][1]), wall1[0][2]],
                        [x1[0], wall1[0][1], wall1[0][2]], [x1[1], wall1[0][1], wall1[0][2]]]]
        return res

    def iII_I_oII_I(self, wall1, wall2):
        res = self.iI_II_oI_II(wall2, wall1)
        return res

    def oI_II_oI_II(self, wall1, wall2):
        res = self.oII_I_oII_I(wall2, wall1)
        return res

    def oI_II_oII_I(self, wall1, wall2):
        sign, my_int = signatures(), myInterval()
        if sign.is_half_out(wall1[0][0], wall1[0][0]) and sign.is_half_out(wall1[0][1], wall2[0][1]):
            res = self.iI_II_iI_II(wall1, wall2)
        elif sign.is_half_out(wall1[0][0], wall1[0][0]):
            res = self.oI_II_oI_II(wall1, wall2)
        elif sign.is_half_out(wall1[0][1], wall2[0][1]):
            if mylen(wall1[0][2]) < mylen(wall2[0][2]):
                y1 = wall1[0][1] - wall2[0][1]
                res = [[[wall1[0][0] - wall2[0][0], wall1[0][1], wall1[0][2]],
                        [wall1[0][0], y1[0], wall2[0][2]], [wall1[0][0], y1[1], wall1[0][2]],
                        my_int.cut_left(wall2[0][0] - wall1[0][0]), wall2[0][1], wall2[0][2]]]
            else:
                res = [[[my_int.cut_left(wall2[0][0] - wall1[0][0]), wall2[0][1], wall2[0][2]],
                        wall1[0][0], wall1[0][1], wall2[0][2]]]
        else:
            res = self.oII_I_oII_I(wall2, wall1)
        return res

    def oII_I_oII_I(self, wall1, wall2):
        res = self.oI_II_oI_II(wall2, wall1)
        return res

    def split_2D(self, signat, walls):
        rozbij2D_dict = {
            ('ii12', 'ii12', 'not intersect'): self.iI_II_iI_II,
            ('ii12', 'ii21', 'not intersect'): self.iI_II_iII_I,
            ('ii12', 'io12', 'not intersect'): self.iI_II_oI_II,
            ('ii12', 'io21', 'not intersect'): self.iI_II_oII_I,
            ('ii21', 'ii21', 'not intersect'): self.iII_I_iII_I,
            ('ii21', 'io12', 'not intersect'): self.iII_I_oI_II,
            ('ii21', 'io21', 'not intersect'): self.iII_I_oII_I,
            ('io12', 'io12', 'not intersect'): self.oI_II_oI_II,
            ('io12', 'io21', 'not intersect'): self.oI_II_oII_I,
            ('io21', 'io21', 'not intersect'): self.oII_I_oII_I
        }
        signat.append('not intersect')
        walls_temp = rozbij2D_dict[tuple(signat)]([[walls[0], walls[2], walls[4]]], [[walls[1], walls[3], walls[5]]])
        walls_res = [[wall[0], wall[1], wall[2]] for wall in walls_temp[0]][0]
        return walls_res

