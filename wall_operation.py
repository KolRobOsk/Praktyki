from signatures_setup import *
from boxes3D import *
from split_intervals import mylen


class WallOperations:

    def split_boxes(self, walllist, iD_list, iD, iD2):
        sign, walls_res, myint = signatures(), [], myInterval()
        box = self.into_wall(walllist[0], walllist[1])
        wall1, wall2 = self.wall_uncut(walllist[0]), self.wall_uncut(walllist[1])
        walls_temp = self.split_walls([wall1, wall2])
        for wall in walls_temp:
            wall_temp = self.check_into_box(wall, box) if box else None
            if wall_temp:
                if wall_temp.is_wall:
                    walls_res.append(self.wall_cut(box3D(wall[0], wall[1], wall[2], max(iD_list[0]) + 1)))
                else:
                    walls_res.append(myint.box_cut(box3D(wall[0], wall[1], wall[2], max(iD_list[0]) + 1)))
                iD_list[0].append(max(iD_list[0]) + 1)
                iD = max(iD_list[1]) + 1
            else:
                walls_res.append(box3D(wall.interval_x, wall.interval_y, wall.interval_z, max(iD_list[1]) + 1))
                iD_list[1].append(iD2)
                iD2 = max(iD_list[1]) + 1
        return walls_res, iD_list, iD, iD2

    def split_walls(self, walls):
        signature_list = self.get_signatures_double(walls[0], walls[1])
        walls_res = []
        sign = signatures()
        signature_list, in2sorted, sorted2in = sign.my_sort(signature_list)
        temp_1 = sign.permute([walls[0].interval_x, walls[0].interval_y, walls[0].interval_z], in2sorted)
        temp_2 = sign.permute([walls[1].interval_x, walls[1].interval_y, walls[1].interval_z], in2sorted)
        walls_temp = self.multi_split_2D(signature_list, [temp_1, temp_2])
        walls_temp_2 = [sign.permute([wall.interval_x, wall.interval_y, wall.interval_z], sorted2in) for wall in walls_temp[0]]
        for wall in walls_temp_2:
            walls_res.append(box3D(wall[0], wall[1], wall[2]))
        return walls_res

    def into_wall(self, box1, box2):
        if box1.is_wall and box2.is_wall:
            return None
        elif box1.is_wall:
            return self.into_wall_execute(box1, box2)
        else:
            return self.into_wall_execute(box2, box1)

    def into_wall_execute(self, wall, box):
        if mylen(wall.interval_x) == 0:
            return box3D(wall.interval_x, box.interval_y, box.interval_z)
        elif mylen(wall.interval_y) == 0:
            return box3D(box.interval_x, wall.interval_y, box.interval_z)
        elif mylen(wall.interval_z) == 0:
            return box3D(box.interval_x, box.interval_y, wall.interval_z)

    def check_if_wall(self, box):
        if mylen(box.interval_x) == 0:
            return box.interval_x
        elif mylen(box.interval_y) == 0:
            return box.interval_y
        elif mylen(box.interval_z) == 0:
            return box.interval_z
        else:
            return None

    def check_into_box(self, wall, box):
        if len(signatures.intersection2D(box, [wall])) > 0:
            if mylen(wall.interval_x) == 0:
                return self.check_into_box_execute(wall, box, 0)
            elif mylen(wall.interval_y) == 0:
                return self.check_into_box_execute(wall, box, 1)
            elif mylen(wall.interval_z) == 0:
                return self.check_into_box_execute(wall, box, 2)
        else:
            return box3D(self.wall_cut_execute(wall.interval_x), self.wall_cut_execute(wall.interval_y),
                         self.wall_cut_execute(wall.interval_z), wall.iD)

    def check_into_box_execute(self, wall, box, num):
        if num == 0:
            return box3D(self.wall_cut_execute(box.interval_x), self.wall_cut_execute(wall.interval_y),
              self.wall_cut_execute(wall.interval_z), wall.iD)
        elif num == 1:
            return box3D(self.wall_cut_execute(wall.interval_x), self.wall_cut_execute(box.interval_y),
                  self.wall_cut_execute(wall.interval_z), wall.iD)
        elif num == 2:
            return box3D(self.wall_cut_execute(wall.interval_x), self.wall_cut_execute(wall.interval_y),
                  self.wall_cut_execute(box.interval_z), wall.iD)

    def wall_uncut(self, wall):
        res = []
        for i in [wall.interval_x, wall.interval_y, wall.interval_z]:
            i = self.wall_uncut_execute(i)
            res.append(i)
        return box3D(res[0], res[1], res[2], wall.iD)

    def wall_uncut_execute(self, inter):
        inter = my_closed(round(inter.lower), round(inter.upper)) if not mylen(inter) == 0 else my_closed(inter.lower, inter.lower)
        return inter

    def wall_cut(self, wall):
        res = []
        for i in [wall.interval_x, wall.interval_y, wall.interval_z]:
            i = self.wall_cut_execute(i)
            res.append(i)
        return box3D(res[0], res[1], res[2], wall.iD)

    def wall_cut_execute(self, inter):
        inter = my_closed(inter.get_lower_eps, inter.get_upper_meps) if not inter.empty else round(inter)
        return inter

    def multi_split_2D(self, sign_list, walls):
        list_res = []
        list_res.append(self.single_split_2D(2, sign_list, walls[0][2], [walls[0][0], walls[0][1], walls[1][0], walls[1][1]]))
        list_res.append(self.single_split_2D(1, sign_list, walls[0][1], [walls[0][0], walls[0][2], walls[1][0], walls[1][2]]))
        list_res.append(self.single_split_2D(0, sign_list, walls[0][0], [walls[0][1], walls[0][2], walls[1][1], walls[1][2]]))
        return list_res

    def single_split_2D(self, i, sign_list, third_inter, walls):
        if sign_list[i] != 'not inter':
            return self.split_2D(sign_list, third_inter, [walls[0], walls[1], walls[2], walls[3]])
        else:
            return walls

    def split_2D(self, signat, third_inter, walls):
        rozbij2D_dict = {
            ('ii12', 'ii12', 'not intersect'): self.iI_II_iI_II,
            ('ii12', 'ii21', 'not intersect'): self.iII_I_iI_II,
            ('ii12', 'io12', 'not intersect'): self.iI_II_oI_II,
            ('ii12', 'io21', 'not intersect'): self.iI_II_oII_I,
            ('ii21', 'ii21', 'not intersect'): self.iII_I_iII_I,
            ('ii21', 'io12', 'not intersect'): self.iII_I_oI_II,
            ('ii21', 'io21', 'not intersect'): self.iII_I_oII_I,
            ('io12', 'io12', 'not intersect'): self.oI_II_oI_II,
            ('io12', 'io21', 'not intersect'): self.oII_I_oI_II,
            ('io21', 'io21', 'not intersect'): self.oII_I_oII_I
        }
        walls = [[self.wall_uncut_execute(walls[0]), self.wall_uncut_execute(walls[1])], [self.wall_uncut_execute(walls[2]), self.wall_uncut_execute(walls[3])]]
        walls_temp = rozbij2D_dict[tuple(signat)]([[walls[0][0], walls[0][1]]], [[walls[1][0], walls[1][1]]])
        walls_res = [box3D(wall[0][0], wall[0][1], third_inter) for wall in walls_temp]
        return walls_res


    def get_signatures_double(self, wall1, wall2):
        wall1 = [wall1.interval_x, wall1.interval_y, wall1.interval_z]
        wall2 = [wall2.interval_x, wall2.interval_y, wall2.interval_z]
        sign, signatures_res = signatures(), []
        for i in range(len(wall1)):
            if mylen(wall1[i]) == 0 or mylen(wall2[i]) == 0:
                signatures_res.append('not intersect')
            else:
                signatures_res.append(sign.get_signature(wall1[i], wall2[i]))
        return signatures_res

    def iI_II_iI_II(self, wall1, wall2):
        res = [[[wall1[0][0] | wall2[0][0], wall1[0][1] | wall2[0][1]]]]
        return res

    def iII_I_iI_II(self, wall1, wall2):
        res = [[wall1[0]]]
        temp = [i for i in wall2[0][1] - wall1[0][1]]
        if len(temp) == 2:
            if temp[1]:
                res[0].append([wall2[0][0], temp[1]])
        if temp:
            res[0].append([wall2[0][0], temp[0]])
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

    def oII_I_oI_II(self, wall1, wall2):
        res = [[[wall1[0][0], wall1[0][1]],
               [wall2[0][0] - wall1[0][0], wall2[0][1] & wall1[0][1]],
                [wall2[0][0], wall2[0][1] - wall1[0][1]]]]
        return res

    def oII_I_oII_I(self, wall1, wall2):
        res = [[[wall1[0][0], wall1[0][1]],
                [wall2[0][0], wall2[0][1] - wall1[0][1]],
                [wall2[0][0] - wall1[0][0], wall2[0][1] & wall1[0][1]]]]
        return res
