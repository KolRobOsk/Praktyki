from signatures_setup import *
from boxes3D import *
from split_intervals import mylen
from walls_cut import *


class WallOperations:

    def split_boxes(self, wall, box, iD_list, iD, iD2):
        wall_cut_obj, sign, walls_res, myint = WallCut(), signatures(), [], myInterval()
        wall1 = box3D.factory(wall[0], wall[1], wall[4].lower, wall[2], wall[3], wall[4].upper, wall[5])
        wall2 = box3D.factory(box[0], box[1], box[4].lower, box[2], box[3], box[4].upper, box[5])
        walls_temp = self.split_walls([wall1, wall2])
        for wall in walls_temp:
            if not wall.is_wall:
                walls_res.append(myint.box_cut(box3D(wall.interval_x, wall.interval_y, wall.interval_z, max(iD_list[0]) + 1)))
                iD_list[0].append(max(iD_list[0]) + 1)
                iD = max(iD_list[1]) + 1
            else:
                walls_res.append(box3D(wall.interval_x, wall.interval_y, wall.interval_z, max(iD_list[1]) + 1))
                iD_list[1].append(iD2)
                iD2 = max(iD_list[1]) + 1
        return walls_res, iD_list, iD, iD2

    def split_walls(self, walls):
        walls_temp_2, sign, walls_res, signature_list = [], signatures(), [], WallCut().get_signatures_double(walls[0], walls[1])
        sorted_sign, in2sorted, sorted2in = sign.my_sort(signature_list)
        temp_1 = sign.permute([walls[0].interval_x, walls[0].interval_y, walls[0].interval_z], in2sorted)
        temp_2 = sign.permute([walls[1].interval_x, walls[1].interval_y, walls[1].interval_z], in2sorted)
        walls_temp = self.multi_split_2D(sorted_sign, [temp_1, temp_2])
        for wall in walls_temp[0]:
            walls_temp_2.append(sign.permute([wall.interval_x, wall.interval_y, wall.interval_z], sorted2in))
        for wall in walls_temp_2:
            walls_res.append(box3D(wall[0], wall[1], wall[2]))
        return walls_res

    def into_wall(self, box1, box2):
        if box1.is_wall and box2.is_wall:
            return None, None
        elif box1.is_wall:
            return self.into_wall_execute(box1, box2), 2
        else:
            return self.into_wall_execute(box2, box1), 1

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

    def check_into_box_execute(self, wall, box, num):
        wall_cut_obj = WallCut()
        if num == 0:
            return box3D(wall_cut_obj.wall_cut_execute(box.interval_x), wall_cut_obj.wall_cut_execute(wall.interval_y),
              wall_cut_obj.wall_cut_execute(wall.interval_z), wall.iD)
        elif num == 1:
            return box3D(wall_cut_obj.wall_cut_execute(wall.interval_x), wall_cut_obj.wall_cut_execute(box.interval_y),
                  wall_cut_obj.wall_cut_execute(wall.interval_z), wall.iD)
        elif num == 2:
            return box3D(wall_cut_obj.wall_cut_execute(wall.interval_x), wall_cut_obj.wall_cut_execute(wall.interval_y),
                  wall_cut_obj.wall_cut_execute(box.interval_z), wall.iD)


    def multi_split_2D(self, sign_list, walls):
        list_res = []
        both_walls = True if self.are_both_walls(walls) else False
        list_res.extend(self.single_split_2D(2, sign_list, [walls[0][2], walls[1][2]], [walls[0][0], walls[0][1], walls[1][0], walls[1][1]], both_walls))
        list_res.extend(self.single_split_2D(1, sign_list, [walls[0][1], walls[1][1]], [walls[0][0], walls[0][2], walls[1][0], walls[1][2]], both_walls))
        list_res.extend(self.single_split_2D(0, sign_list, [walls[0][0], walls[1][0]], [walls[0][1], walls[0][2], walls[1][1], walls[1][2]], both_walls))
        return list_res

    def are_both_walls(self, walls):
        return True if box3D(walls[0][0], walls[0][1], walls[0][2]).is_wall and box3D(walls[1][0], walls[1][1], walls[1][2]).is_wall else False

    def single_split_2D(self, i, sign_list, third_inter, walls, both_walls):
        wall_obj = WallCut()
        if any([mylen(third_inter[0]) == 0, mylen(third_inter[1]) == 0]) and both_walls:
            return [wall_obj.split_2D(sign_list, third_inter[0], [walls[0], walls[1], walls[2], walls[3]])]
        elif any([mylen(third_inter[0]) == 0, mylen(third_inter[1]) == 0]) and not both_walls:
            return [wall_obj.split_2D_3D(sign_list, third_inter, [walls[0], walls[1], walls[2], walls[3]])]
        else:
            return []