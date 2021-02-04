from signatures_setup import *

class WallCut:

    def wall_uncut(self, wall):
        res = []
        for i in [wall.interval_x, wall.interval_y, wall.interval_z]:
            i = self.wall_uncut_execute(i)
            res.append(i)
        return box3D(res[0], res[1], res[2], wall.iD)

    def wall_uncut_execute(self, inter):
        inter = my_closed(round(inter.lower), round(inter.upper)) if not mylen(inter) == 0 else inter
        return inter

    def wall_cut(self, wall):
        res = []
        for i in [wall.interval_x, wall.interval_y, wall.interval_z]:
            i = self.wall_cut_execute(i)
            res.append(i)
        return box3D(res[0], res[1], res[2], wall.iD)

    def wall_cut_execute(self, inter):
        inter = my_closed(inter.lower_eps, inter.upper_meps) if not mylen(inter) == 0 else inter
        return inter

    def signat_reverse(self, signat):
        new_sign = []
        for sign in signat:
            if sign == 'ii21':
                new_sign.append('ii12')
            elif sign == 'ii12':
                new_sign.append('ii21')
            elif sign == 'io12':
                new_sign.append('io21')
            elif sign == 'io21':
                new_sign.append('io12')
            else:
                new_sign.append('not intersect')
        return new_sign

    def merge_boxes_and_walls(self, list1, list2, third_inter):
        result = []
        if list1:
            result.extend([box3D(wall[0], wall[1], third_inter[0]) for wall in list1])
        if list2:
            result.extend([box3D(wall[0], wall[1], third_inter[1]) for wall in list2])
        return result

    def split_2D_3D(self, signat, third_inter, walls):
        rozbij2D_3D_dict = {
            ('ii12', 'ii12', 'not intersect'): self.iI_II_iI_II_3D,
            ('ii12', 'ii21', 'not intersect'): self.iI_II_iII_I_3D,
            ('ii12', 'io12', 'not intersect'): self.iI_II_oI_II_3D,
            ('ii12', 'io21', 'not intersect'): self.iI_II_oII_I_3D,
            ('ii21', 'ii21', 'not intersect'): self.iII_I_iII_I_3D,
            ('ii21', 'io12', 'not intersect'): self.iII_I_oI_II_3D,
            ('ii21', 'io21', 'not intersect'): self.iII_I_oII_I_3D,
            ('io12', 'io12', 'not intersect'): self.oI_II_oI_II_3D,
            ('io12', 'io21', 'not intersect'): self.oI_II_oII_I_3D,
            ('io21', 'io21', 'not intersect'): self.oII_I_oII_I_3D
        }
        if mylen(third_inter[0]) == 0:
            walls = [[self.wall_uncut_execute(walls[0]), self.wall_uncut_execute(walls[1])],
                     [self.wall_uncut_execute(walls[2]), self.wall_uncut_execute(walls[3])]]
            third_inter_temp = third_inter
        else:
            walls = [[self.wall_uncut_execute(walls[2]), self.wall_uncut_execute(walls[3])],
                     [self.wall_uncut_execute(walls[0]), self.wall_uncut_execute(walls[1])]]
            signat = self.signat_reverse(signat)
            third_inter_temp = [third_inter[1], third_inter[0]]
        walls_temp, boxes_temp = rozbij2D_3D_dict[tuple(signat)]([[walls[0][0], walls[0][1]]], [[walls[1][0], walls[1][1]]])
        walls_and_boxes_res = self.merge_boxes_and_walls(walls_temp, boxes_temp, third_inter_temp)
        return walls_and_boxes_res

    def iI_II_iI_II_3D(self, wall, box):
        return None, [[box[0][0], box[0][1]]]

    def iI_II_iII_I_3D(self, wall, box):
        wall_y_temp = [wall[0][1] - box[0][1]]
        walls_temp = [[wall[0][0], wall_y_temp[0]]]
        if len(wall_y_temp) == 2:
            if wall_y_temp[1]:
                walls_temp.append([wall[0][0], wall_y_temp[1]])
        return walls_temp, [[box[0][0], box[0][1]]]

    def iI_II_oI_II_3D(self, wall, box):
        return [[wall[0][0], wall[0][1] - box[0][1]]], [[box[0][0], box[0][1]]]

    def iI_II_oII_I_3D(self, wall, box):
        return [[wall[0][0], wall[0][1] - box[0][1]]], [[box[0][0], box[0][1]]]

    def iII_I_iII_I_3D(self, wall, box):
        wall_x_temp = [wall[0][0] - box[0][0]]
        wall_y_temp = [wall[0][1] - box[0][1]]
        walls_temp = []
        if wall_x_temp[0]:
            walls_temp.append([wall_x_temp[0], wall[0][1] & box[0][1]])
        if len(wall_x_temp) == 2:
            if wall_x_temp[1]:
                walls_temp.append([wall_x_temp[1], wall[0][1] & box[0][1]])
        if wall_y_temp[0]:
            walls_temp.append([wall[0][0], wall_y_temp[0]])
        if len(wall_y_temp) == 2:
            if wall_y_temp[1]:
                walls_temp.append([wall[0][0], wall_y_temp[1]])
        return walls_temp, [[box[0][0], box[0][1]]]

    def iII_I_oI_II_3D(self, wall, box):
        return [[wall[0][0] - box[0][0], wall[0][1]]], [[box[0][0], box[0][1]]]

    def iII_I_oII_I_3D(self, wall, box):
        wall_x_temp = [wall[0][0] - box[0][0]]
        wall_temp = [[wall_x_temp[0], wall[0][1]], [wall[0][0], wall[0][1] - box[0][1]]]
        if len(wall_x_temp) == 2:
            if wall_x_temp[1]:
                wall_temp.append([wall_x_temp[1], wall[0][1]])
        return wall_temp, [[box[0][0], box[0][1]]]

    def oI_II_oI_II_3D(self, wall, box):
        wall_temp = [[wall[0][0] - box[0][0], box[0][1] & wall[0][1]], [wall[0][0]], wall[0][1] - box[0][1]]
        return wall_temp, [[box[0][0], box[0][1]]]

    def oI_II_oII_I_3D(self, wall, box):
        wall_temp = [[wall[0][0] - box[0][0], box[0][1] & wall[0][1]], [wall[0][0]], wall[0][1] - box[0][1]]
        return wall_temp, [[box[0][0], box[0][1]]]

    def oII_I_oII_I_3D(self, wall, box):
        wall_temp = [[wall[0][0] - box[0][0], box[0][1] & wall[0][1]], [wall[0][0]], wall[0][1] - box[0][1]]
        return wall_temp, [[box[0][0], box[0][1]]]

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
        walls_res = [box3D(wall[0], wall[1], third_inter) for wall in walls_temp[0]]
        return walls_res

    def get_signatures_double(self, wall1, wall2):
        wall1, wall2 = self.wall_uncut(wall1), self.wall_uncut(wall2)
        wall1 = [wall1.interval_x, wall1.interval_y, wall1.interval_z]
        wall2 = [wall2.interval_x, wall2.interval_y, wall2.interval_z]
        sign, signatures_res = signatures(), []
        where_equal = where_in = None
        for i in range(len(wall1)):
            if any([mylen(wall1[i]) == 0, mylen(wall2[i]) == 0]):
                signatures_res.append('not intersect')
            elif i == where_equal and where_in:
                signatures_res.append(sign.get_signature(wall1[where_in], wall2[where_in]))
            else:
                signatures_res.append(sign.get_signature(wall1[i], wall2[i]))
        return signatures_res

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