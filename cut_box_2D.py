from cut_box_3D import *

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

