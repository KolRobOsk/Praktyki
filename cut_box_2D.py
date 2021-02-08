from cut_box_3D import *
from split_intervals_3D import mylen
from boxes_3D import *
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
            res.append(self.wall_cut_execute(i))
        return box3D(res[0], res[1], res[2], wall.iD)

    def wall_cut_execute(self, inter):
        inter = my_closed(inter.lower_eps, inter.upper_meps) if not mylen(inter) == 0 else inter
        return inter

    def check_if_wall(self, box):
        if mylen(box.interval_x) == 0:
            return box.interval_x
        elif mylen(box.interval_y) == 0:
            return box.interval_y
        elif mylen(box.interval_z) == 0:
            return box.interval_z
        else:
            return None

    def split_2D(self, sign_list, third_inter, walls):
        return [self.split_2D(sign_list, third_inter, [walls[0], walls[1], walls[2], walls[3]])]


    def split_walls(self, wall1, wall2):
        walls_temp_2, sign, walls_res, signature_list = [], signatures(), [], WallCut().get_signatures_double(wall1, wall2)
        sorted_sign, in2sorted, sorted2in = sign.my_sort(signature_list)
        print(wall1)
        walls_temp = self.split_2D(sorted_sign, [wall1[0], wall1[1], wall2[0], wall2[1]], both_walls)
        for wall in walls_temp:
            temp = sign.permute([wall[0], wall[1]], sorted2in)
            walls_res.append([temp[0], temp[1]])
        return walls_res
