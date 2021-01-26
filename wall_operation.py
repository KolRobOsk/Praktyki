from signatures_setup import *
from boxes3D import *
import os
from split_intervals import mylen

class WallOperations:

    def split_boxes(self, walllist):
        wall_res = []
        stack = boxStack()
        sign = signatures()
        walllist_n = []
        for i in walllist:
            walllist_n.append(self.wall_uncut(i))
        walllist = walllist_n
        while not len(walllist) == 0:
            wall_inter = walllist.pop()
            if sign.intersection2D(wall_inter, wall_res):
                intersect = sign.intersection2D(wall_inter, wall_res)[0]
                walls = self.split_walls(wall_inter, intersect)
                for wall in walls:
                     walllist.extend([box3D(wall[0], wall[1], wall[2])])
            else:
                #self.wall_cut(wall_inter)
                stack.extend([wall_inter])
        return stack

    def wall_uncut(self, wall):
        res = []
        for i in [wall.interval_x, wall.interval_y, wall.interval_z]:
            i = self.wall_cut_execute(i)
            res.append(i)
        return box3D(res[0], res[1], res[2])

    def wall_uncut_execute(self, inter):
        inter = my_closed(round(inter.get_lower_eps), round(inter.get_upper_meps)) if mylen(inter)>0 else inter
        return inter

    def wall_cut(self, wall):
        res = []
        for i in [wall.interval_x, wall.interval_y, wall.interval_z]:
            i = self.wall_cut_execute(i)
            res.append(i)
        return box3D(res[0], res[1], res[2])

    def wall_cut_execute(self, inter):
        inter = my_closed(inter.get_lower_eps, inter.get_upper_meps) if mylen(inter)>0 else inter
        return inter

    def split_walls(self, wall1, wall2):
        signature_list, walls = [], [wall1, wall2]
        signature_list = self.get_signatures_double(wall1, wall2)
        signature_list, in2sorted, sorted2in = signatures().my_sort(signature_list)
        print(signature_list)
        walls = [self.multi_split_2D(signature_list, walls)]
        return walls

    def multi_split_2D(self, list, walls):
        list_res = []
        list_res.append(self.single_split_2D(list, [[walls[0].get_interval_x(), walls[0].get_interval_y()], [walls[1].get_interval_x(), walls[1].get_interval_y()]]))
        list_res.append(self.single_split_2D(list, [[walls[0].get_interval_x(), walls[0].get_interval_z()], [walls[1].get_interval_x(), walls[1].get_interval_z()]]))
        list_res.append(self.single_split_2D(list, [[walls[0].get_interval_y(), walls[0].get_interval_z()], [walls[1].get_interval_y(), walls[1].get_interval_z()]]))
        return list_res

    def single_split_2D(self, list, walls):
        if mylen(walls[0][0]) != 0 or mylen(walls[0][1]):
            return self.split_2D(list, [walls[0], walls[1]])
        else:
            return walls[0][0]

    def split_2D(self, signat, walls):
        rozbij2D_dict = {
            ('ii12', 'ii12', 'not inter'): self.iI_II_iI_II,
            ('ii12', 'ii21', 'not inter'): self.iI_II_iII_I,
            ('ii12', 'io12', 'not inter'): self.iI_II_oI_II,
            ('ii12', 'io21', 'not inter'): self.iI_II_oII_I,
            ('ii21', 'ii21', 'not inter'): self.iII_I_iII_I,
            ('ii21', 'io12', 'not inter'): self.iII_I_oI_II,
            ('ii21', 'io21', 'not inter'): self.iII_I_oII_I,
            ('io12', 'io12', 'not inter'): self.oI_II_oI_II,
            ('io12', 'io21', 'not inter'): self.oI_II_oII_I,
            ('io21', 'io21', 'not inter'): self.oII_I_oII_I
        }
        print(signat)
        walls = rozbij2D_dict[tuple(signat)]([walls[0]], [walls[1]])
        return walls


    def get_signatures_double(self, wall1, wall2):
        wall1 = [wall1.interval_x, wall1.interval_y, wall1.interval_z]
        wall2 = [wall2.interval_x, wall2.interval_y, wall2.interval_z]
        signatures_res = []
        for i in range(len(wall1)):
            if wall1[i] != my_closed(math.inf, -math.inf) & wall2[i] != my_closed(math.inf, -math.inf):
                signatures_res.append("not inter")
            else:
                signatures_res.append(signatures().get_signature(wall1[i], wall2[i]))
        return signatures_res

    def iI_II_iI_II(self, wall1, wall2):
        return [wall1[0][0] & wall2[0][0], wall1[0][1] & wall2[0][1]]

    def iI_II_iII_I(self, wall1, wall2):

        wall1_split_int1 = [j for j in (wall1[0][1] - wall2[0][1])]
        walls = [wall2[0],
                [wall1[0][0], wall1_split_int1[0][0]],
                 [wall1[0][0], wall1_split_int1[0][1]]]
        return walls

    def iI_II_oI_II(self, wall1, wall2):
        return [wall1[0], [wall2[0][0], wall2[0][1] - wall1[0][1]]]

    def iII_I_iII_I(self, wall1, wall2):
        return [[wall1[0][0] & wall2[0][0], wall1[0][1] & wall2[0][1]]]

    def iI_II_oII_I(self, wall1, wall2):
        return [wall1[0], [wall2[0][1], wall2[0][1] - wall1[0][1]]]

    def iII_I_oI_II(self, wall1, wall2):
        return [wall2[0], [wall1[0][0], wall1[0][0] - wall2[0][0]]]

    def iII_I_oII_I(self, wall1, wall2):
        return [wall2[0],
                [wall1[0][0], wall1[0][1] - wall2[0][1]]]

    def oI_II_oI_II(self, wall1, wall2):
        return [[wall1[0][0] & wall2[0][0], wall1[0][1] & wall2[0][1]],
                [wall1[0][0] - wall2[0][0], wall1[0][1] & wall2[0][1]],
                [wall2[0][0] - wall1[0][0], wall1[0][1] & wall2[0][1]],
                [wall1[0][0], wall1[0][1] - wall2[0][1]],
                [wall2[0][0], wall2[0][1] - wall1[0][1]]]

    def oI_II_oII_I(self, wall1, wall2):
        return [[wall1[0][0] & wall2[0][0], wall1[0][1] & wall2[0][1]],
                [wall1[0][0] - wall2[0][0], wall1[0][1] & wall2[0][1]],
                [wall2[0][0] - wall1[0][0], wall1[0][1] & wall2[0][1]],
                [wall1[0][0], wall1[0][1] - wall2[0][1]],
                [wall2[0][0], wall2[0][1] - wall1[0][1]]]

    def oII_I_oII_I(self, wall1, wall2):
        return [[wall1[0][0] & wall2[0][0], wall1[0][1] & wall2[0][1]],
                [wall1[0][0] - wall2[0][0], wall1[0][1] & wall2[0][1]],
                [wall2[0][0] - wall1[0][0], wall1[0][1] & wall2[0][1]],
                [wall1[0][0], wall1[0][1] - wall2[0][1]],
                [wall2[0][0], wall2[0][1] - wall1[0][1]]]

