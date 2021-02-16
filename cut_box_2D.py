from signatures_setup import *
from split_intervals_2D import *

class WallCut:

    def check_if_walls_intersect(self, wall1, wall2):
        sign, x1, y1, z1, x2, y2, z2 = signatures(), wall1.interval_x, wall1.interval_y, wall1.interval_z, wall2.interval_x, wall2.interval_y, wall2.interval_z
        return True if sum([sign.is_separate(x1, x2), sign.is_separate(y1, y2), sign.is_separate(z1, z2)]) == 0 else False

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

    def split_walls(self, wall1, wall2, third_inter):
        walls_temp_2, sign, walls_res, signature_list = [], signatures(), [], signatures().get_signatures_double(wall1, wall2)
        sorted_sign, in2sorted, sorted2in = sign.my_sort(signature_list)
        walls = [self.wall_uncut_execute(wall1[0]), self.wall_uncut_execute(wall1[1]),
                 self.wall_uncut_execute(wall2[0]), self.wall_uncut_execute(wall2[1]),
                 self.wall_uncut_execute(third_inter[0]), self.wall_uncut_execute(third_inter[1])]
        walls_temp = split_2D().split_2D(sorted_sign, walls)
        for wall in [walls_temp]:
            temp = sign.permute([wall[0], wall[1]], sorted2in)
            walls_res.append([temp[0], temp[1], wall[2]])
        return walls_res