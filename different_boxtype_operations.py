from split_intervals_2D import *
from cut_box_2D import *

class boxOperations:

    def rotate_and_execute(self, box1, box2, iD):
        '''
        Funkcja obraca pudełka zmieniając kolejność interwałów \n
        :param box1: pudełko ze stosu \n
        :param box2: pudełko z drzewa \n
        :return: lista table, która zawiera pudełka po rozbiciach \n
        :rtype: list
        '''
        sign, spl3D = signatures(), split_3D()
        idx_sign = sign.get_signatures_triple(box1, box2)
        sort, in2sorted, sorted2in = sign.my_sort(idx_sign)
        tri_sign, tri_sign_i = sign.sort_by_signatures(box1, box2, in2sorted)
        split_sign = spl3D.split(tuple(sort), tri_sign, tri_sign_i)
        table, iD = sign.ret_original_order(split_sign, sorted2in, iD)
        return table, iD


    def rotate_and_execute2D(self, wall1, wall2, iD_list):
        wall_cut_obj, sign, walls_res, myint = WallCut(), signatures(), [], myInterval()
        walls_temp = wall_cut_obj.split_walls(wall1, wall2)
        for wall in walls_temp:
            walls_res.append(myint.box_cut([wall[0], wall[1], max(iD_list[0]) + 1]))
            iD_list[1].append(max(iD_list[0]) + 1)
        return walls_res, iD_list

    def execute2D_check(self, box_res, box_temp):
        checksum = 0
        if box_res.interval_x in box_temp.interval_x or box_res.interval_x == box_temp.interval_x:
            checksum += 1
        if box_res.interval_y in box_temp.interval_y or box_res.interval_y == box_temp.interval_y:
            checksum += 1
        if box_res.interval_z in box_temp.interval_z or box_res.interval_z == box_temp.interval_z:
            checksum += 1
        return checksum
