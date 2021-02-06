from signatures_setup import *

class split_2D:

    def iI_II_iI_II(self, wall1, wall2):
        res = [[[wall1[0][0] | wall2[0][0], wall1[0][1] | wall2[0][1]]]]
        return res


    def iI_II_iII_I(self, wall1, wall2):
        if signatures().is_equal(wall1[0][1], wall2[0][1]) or signatures().is_equal(wall2[0][0], wall1[0][0]):
            return self.iI_II_iI_II(wall1, wall2)
        else:
            res = [[wall2[0]]]
            temp = [i for i in wall1[0][1] - wall2[0][1]]
            if len(temp) == 2:
                if temp[1]:
                    res[0].append([wall1[0][0], temp[1]])
            if temp:
                res[0].append([wall1[0][0], temp[0]])
            return res


    def iI_II_oI_II(self, wall1, wall2):
        res = [[wall2[0], [wall1[0][0], wall1[0][1] - wall2[0][1]]]]
        return res


    def iII_I_iII_I(self, wall1, wall2):
        res = [[[wall1[0][0] | wall2[0][0], wall1[0][1] | wall2[0][1]]]]
        return res


    def iI_II_oII_I(self, wall1, wall2):
        res = [[[wall2[0][0], wall2[0][1]], [wall1[0][0], wall1[0][1] - wall2[0][1]]]]
        return res


    def iII_I_oI_II(self, wall1, wall2):
        res = [[[wall1[0][0], wall1[0][1]], [wall2[0][0], wall2[0][1] - wall1[0][1]]]]
        return res


    def iII_I_oII_I(self, wall1, wall2):
        res = [[[wall1[0][0], wall1[0][1]], [wall2[0][0], wall2[0][1] - wall1[0][1]]]]
        return res


    def oI_II_oI_II(self, wall1, wall2):
        res = [[[wall2[0][0], wall2[0][1]],
                [wall1[0][0] - wall2[0][0], wall1[0][1] - wall2[0][1]],
                [wall1[0][0] & wall2[0][0], wall1[0][1] - wall2[0][1]],
                [wall1[0][0] - wall2[0][0], wall1[0][1] & wall2[0][1]]]]
        return res


    def oI_II_oII_I(self, wall1, wall2):
        res = [[[wall2[0][0], wall2[0][1]],
                [wall1[0][0] - wall2[0][0], wall1[0][1] & wall2[0][1]],
                [wall1[0][0], wall1[0][1] - wall2[0][1]]]]
        return res


    def oII_I_oII_I(self, wall1, wall2):
        res = [[[wall1[0][0], wall1[0][1]],
                [wall2[0][0], wall2[0][1] - wall1[0][1]],
                [wall2[0][0] - wall1[0][0], wall2[0][1] & wall1[0][1]]]]
        return res

    def split_2D(self, signat, third_inter, walls):
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
        walls = [[self.wall_uncut_execute(walls[0]), self.wall_uncut_execute(walls[1])],
                 [self.wall_uncut_execute(walls[2]), self.wall_uncut_execute(walls[3])]]
        walls_temp = rozbij2D_dict[tuple(signat)]([[walls[0][0], walls[0][1]]], [[walls[1][0], walls[1][1]]])
        walls_res = [[wall[0], wall[1]] for wall in walls_temp[0]][0]
        return walls_res

