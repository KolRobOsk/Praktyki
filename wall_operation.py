from signatures_setup import *
from boxes3D import *
from split_intervals import mylen


class WallOperations:

    def split_boxes(self, walllist):
        wall_res, walls = [], []
        box = None
        box = walllist[0] if not walllist[0].is_wall else box
        box = walllist[1] if not walllist[1].is_wall else box
        box_sign = 0 if walllist[0] == box else 1 if walllist[1] == box else None
        stack = boxStack()
        sign = signatures()
        walllist_n = []
        for i in walllist:
            walllist_n.append(self.wall_uncut(i))
        walllist = walllist_n
        if box:
            stack.extend([box])
        '''
        while not len(walllist) == 0:
            wall_inter = walllist.pop()
            if sign.intersection2D(wall_inter, wall_res):
                if box:
                    intersect, not_intersect = sign.intersection2D(wall_inter, [box])
                else:
                    intersect, not_intersect = sign.intersection2D(wall_inter, wall_res)
                if intersect:
                    for i in range(len(intersect)):
                 
            '''
        walls = self.split_walls(walllist[0], walllist[1])
        walllist.extend(walls)
        if box_sign:
            for box1 in walllist:
                stack.extend([self.slice2D(box1, box)])
                #walllist.extend(not_intersect)
        return stack

    '''
            else:
                stack.extend([self.wall_cut(wall_inter)])
    '''

    def slice2D(self, wall, box):
        if box.intersect2D(wall):
            if mylen(wall.interval_x) == 0:
                return box3D(self.wall_cut_execute(box.interval_x), self.wall_cut_execute(wall.interval_y), self.wall_cut_execute(wall.interval_z))
            elif mylen(wall.interval_y) == 0:
                return box3D(self.wall_cut_execute(wall.interval_x), self.wall_cut_execute(box.interval_y), self.wall_cut_execute(wall.interval_z))
            elif mylen(wall.interval_z) == 0:
                return box3D(self.wall_cut_execute(wall.interval_x), self.wall_cut_execute(wall.interval_y), self.wall_cut_execute(box.interval_z))
        else:
            return box3D(self.wall_cut_execute(wall.interval_x), self.wall_cut_execute(wall.interval_y),
                         self.wall_cut_execute(wall.interval_z))

    def wall_uncut(self, wall):
        res = []
        for i in [wall.interval_x, wall.interval_y, wall.interval_z]:
            i = self.wall_uncut_execute(i)
            res.append(i)
        return box3D(res[0], res[1], res[2])

    def wall_uncut_execute(self, inter):
        inter = my_closed(round(inter.lower), round(inter.upper)) if not mylen(inter) == 0 else inter
        return inter

    def wall_cut(self, wall):
        res = []
        for i in [wall.interval_x, wall.interval_y, wall.interval_z]:
            i = self.wall_cut_execute(i)
            res.append(i)
        return box3D(res[0], res[1], res[2])

    def wall_cut_execute(self, inter):
        inter = my_closed(inter.get_lower_eps, inter.get_upper_meps) if not inter.empty else round(inter)
        return inter

    def split_walls(self, wall1, wall2):
        wall1, wall2 = self.wall_uncut(wall1), self.wall_uncut(wall2)
        signature_list, walls, wall_temp = [], [wall1, wall2], []

        signature_list = self.get_signatures_double(wall1, wall2)
        sign = signatures()
        signature_list, in2sorted, sorted2in = sign.my_sort(signature_list)
        for wall in walls:
            temp = sign.permute([wall.interval_x, wall.interval_y, wall.interval_z], in2sorted)
            wall_temp.append(box3D(temp[0], temp[1], temp[2]))
        '''
        if wall:
            for wall in walls:
                temp = sign.permute([wall.interval_x, wall.interval_y, wall.interval_z], sorted2in)
                wall_temp.append(box3D(temp.interval_x, temp.interval_y, temp.interval_z))
        '''
        walls, wall_temp = [self.multi_split_2D(signature_list, wall_temp)], []
        for wall in walls:
            walls_res = sign.permute(wall, sorted2in)
        return walls_res

    def multi_split_2D(self, list, walls):
        list_res = []
        list_res.append(self.single_split_2D(list, [[walls[0].get_interval_x(), walls[0].get_interval_y()], [walls[1].get_interval_x(), walls[1].get_interval_y()]]))
        list_res.append(self.single_split_2D(list, [[walls[0].get_interval_x(), walls[0].get_interval_z()], [walls[1].get_interval_x(), walls[1].get_interval_z()]]))
        list_res.append(self.single_split_2D(list, [[walls[0].get_interval_y(), walls[0].get_interval_z()], [walls[1].get_interval_y(), walls[1].get_interval_z()]]))
        return list_res

    def single_split_2D(self, list, walls):
        if mylen(walls[0][0]) != 0 and mylen(walls[0][1]) != 0:
            return self.split_2D(list, [[walls[0], walls[1]]])
        else:
            return walls[0][0]

    def split_2D(self, signat, walls):
        rozbij2D_dict = {
            ('ii12', 'ii12', 'not intersect'): self.iI_II_iI_II,
            ('ii21', 'ii12', 'not intersect'): self.iII_I_iI_II,
            ('ii12', 'io12', 'not intersect'): self.iI_II_oI_II,
            ('ii12', 'io21', 'not intersect'): self.iI_II_oII_I,
            ('ii21', 'ii21', 'not intersect'): self.iII_I_iII_I,
            ('ii21', 'io12', 'not intersect'): self.iII_I_oI_II,
            ('ii21', 'io21', 'not intersect'): self.iII_I_oII_I,
            ('io12', 'io12', 'not intersect'): self.oI_II_oI_II,
            ('io21', 'io12', 'not intersect'): self.oII_I_oI_II,
            ('io21', 'io21', 'not intersect'): self.oII_I_oII_I
        }
        walls = [[[self.wall_uncut_execute(walls[0][0][0]), self.wall_uncut_execute(walls[0][0][1])], [self.wall_uncut_execute(walls[0][1][0]), self.wall_uncut_execute(walls[0][1][1])]]]
        walls = rozbij2D_dict[tuple(signat)]([walls[0][0]], [walls[0][1]])
        return walls


    def get_signatures_double(self, wall1, wall2):
        wall1 = [wall1.interval_x, wall1.interval_y, wall1.interval_z]
        wall2 = [wall2.interval_x, wall2.interval_y, wall2.interval_z]
        signatures_res = []
        for i in range(len(wall1)):
            if mylen(wall1[i]) == 0 or mylen(wall2[i]) == 0:
                signatures_res.append('not intersect')
            else:
                signatures_res.append(signatures().get_signature(wall1[i], wall2[i]))
        return signatures_res

    def iI_II_iI_II(self, wall1, wall2):
        res = [[[wall1[0][0] | wall2[0][0], wall1[0][1] | wall2[0][1]]]]
        for wall in res[0]:
            wall[0], wall[1] = my_closed(wall[0].lower, wall[0].upper), my_closed(wall[1].lower, wall[1].upper)
        return res

    def iII_I_iI_II(self, wall1, wall2):
        res = [[wall1[0]]]
        temp = [i for i in wall2[0][1] - wall1[0][1]]
        if len(temp) == 2:
            if temp[1]:
                res[0].append([wall2[0][0], temp[1]])
        if temp:
            res[0].append([wall2[0][0], temp[0]])
        for wall in res[0]:
            wall[0], wall[1] = my_closed(wall[0].lower, wall[0].upper), my_closed(wall[1].lower, wall[1].upper)
        return res

    def iI_II_oI_II(self, wall1, wall2):
        res = [[wall2[0], [wall1[0][0], wall1[0][1] - wall2[0][1]]]]
        for wall in res[0]:
            wall[0], wall[1] = my_closed(wall[0].lower, wall[0].upper), my_closed(wall[1].lower, wall[1].upper)
        return res

    def iII_I_iII_I(self, wall1, wall2):
        res = [[[wall1[0][0] | wall2[0][0], wall1[0][1] | wall2[0][1]]]]
        for wall in res[0]:
            wall[0], wall[1] = my_closed(wall[0].lower, wall[0].upper), my_closed(wall[1].lower, wall[1].upper)
        return res

    def iI_II_oII_I(self, wall1, wall2):
        res = [[[wall2[0][0], wall2[0][1]], [wall1[0][0], wall1[0][1] - wall2[0][1]]]]
        for wall in res[0]:
            wall[0], wall[1] = my_closed(wall[0].lower, wall[0].upper), my_closed(wall[1].lower, wall[1].upper)
        return res

    def iII_I_oI_II(self, wall1, wall2):
        res = [[[wall1[0][0], wall1[0][1]], [wall2[0][0], wall2[0][1] - wall1[0][1]]]]
        for wall in res[0]:
            wall[0], wall[1] = my_closed(wall[0].lower, wall[0].upper), my_closed(wall[1].lower, wall[1].upper)
        return res

    def iII_I_oII_I(self, wall1, wall2):
        res = [[[wall1[0][0], wall1[0][1]], [wall2[0][0], wall2[0][1] - wall1[0][1]]]]
        for wall in res[0]:
            wall[0], wall[1] = my_closed(wall[0].lower, wall[0].upper), my_closed(wall[1].lower, wall[1].upper)
        return res

    def oI_II_oI_II(self, wall1, wall2):
        res = [[[wall2[0][0], wall2[0][1]],
        [wall1[0][0] - wall2[0][0], wall1[0][1] - wall2[0][1]],
        [wall1[0][0] & wall2[0][0], wall1[0][1] - wall2[0][1]],
        [wall1[0][0] - wall2[0][0], wall1[0][1] & wall2[0][1]]]]
        for wall in res[0]:
            wall[0], wall[1] = my_closed(wall[0].lower, wall[0].upper), my_closed(wall[1].lower, wall[1].upper)
        return res

    def oII_I_oI_II(self, wall1, wall2):
        res = [[[wall1[0][0], wall1[0][1]],
               [wall2[0][0] - wall1[0][0], wall2[0][1] & wall1[0][1]],
                [wall2[0][0], wall2[0][1] - wall1[0][1]]]]
        for wall in res[0]:
            wall[0], wall[1] = my_closed(wall[0].lower, wall[0].upper), my_closed(wall[1].lower, wall[1].upper)
        return res

    def oII_I_oII_I(self, wall1, wall2):
        res = [[[wall1[0][0], wall1[0][1]],
                [wall2[0][0], wall2[0][1] - wall1[0][1]],
                [wall2[0][0] - wall1[0][0], wall2[0][1] & wall1[0][1]]]]
        for wall in res[0]:
            wall[0], wall[1] = my_closed(wall[0].lower, wall[0].upper), my_closed(wall[1].lower, wall[1].upper)
        return res

