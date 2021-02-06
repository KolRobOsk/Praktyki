from split_intervals_2D import *

class boxOperations:

    def rotate_and_execute(self, box1, box2):
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
        tri_sign, tri_sign_i = sign.sort_signatures(box1, box2, in2sorted)
        split_sign = spl3D.split(tuple(sort), tri_sign, tri_sign_i)
        table = sign.ret_original_order(split_sign, sorted2in)
        return table


    def rotate_and_execute2D(self, wall1, wall2, iD_list):
        walls_res, iD_list, iD, iD2 = split_2D().split_boxes(wall1, wall2, iD_list)
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
