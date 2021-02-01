import os, sys
sys.path.insert(0, os.path.abspath('.'))
from signatures_setup import *
from split_intervals import *
from cut_box import *
from wall_operation import *
from boxes3D import *

try:
    os.remove('3d_index.idx')
    os.remove('3d_index.dat')
    os.remove('2d_index_xy.idx')
    os.remove('2d_index_xy.dat')
    os.remove('2d_index_yz.idx')
    os.remove('2d_index_yz.dat')
    os.remove('2d_index_xz.idx')
    os.remove('2d_index_xz.dat')
except:
    pass
'''
Usuwanie poprzednich plików drzewa,
inaczej błąd kompilacji, bo python
próbuje zapisać coś co już jest
'''

#główna klasa całego programu
class algorithm:




    '''
    Główna klasa programu.
    '''
    def rotate_and_execute(self, box1, box2, iD_list):
        '''
        Funkcja obraca pudełka zmieniając kolejność interwałów \n
        :param box1: pudełko ze stosu \n
        :param box2: pudełko z drzewa \n
        :return: lista table, która zawiera pudełka po rozbiciach \n
        :rtype: list
        '''
        sign = signatures()
        spl = split()
        idx_sign = sign.get_signatures_triple(box1, box2)
        sort, in2sorted, sorted2in = sign.my_sort(idx_sign)
        tri_sign, tri_sign_i = sign.sort_signatures(box1, box2, in2sorted)
        split_sign = spl.split(tuple(sort), tri_sign, tri_sign_i)
        table = sign.ret_original_order(split_sign, sorted2in)
        return table

    def rotate_and_execute2D(self, wall, box, iD_list, iD, iD2):
        walls_res, iD_list, iD, iD2 = WallOperations().split_boxes([wall, box], iD_list, iD, iD2)
        return walls_res, iD_list, iD, iD2

    def execute2D_check(self, box_res, box_temp):
        checksum = 0
        if box_res.interval_x in box_temp.interval_x or box_res.interval_x == box_temp.interval_x:
            checksum += 1
        if box_res.interval_y in box_temp.interval_y or box_res.interval_y == box_temp.interval_y:
            checksum += 1
        if box_res.interval_z in box_temp.interval_z or box_res.interval_z == box_temp.interval_z:
            checksum += 1
        return checksum

    def check_if_wall(self, wall, box):
        box_temp = box3D(wall.interval_x, wall.interval_y, wall.interval_z, wall.iD)
        if not box.is_wall:
            if mylen(wall.interval_x) == 0:
                box_temp = box3D(wall.get_interval_x(), box.get_interval_y(), box.get_interval_z(), wall.iD)
            elif mylen(wall.interval_y) == 0:
                box_temp = box3D(box.get_interval_x(), wall.get_interval_y(), box.get_interval_z(), wall.iD)
            elif mylen(wall.interval_z) == 0:
                box_temp = box3D(box.get_interval_x(), box.get_interval_y(), wall.get_interval_z(), wall.iD)
        return box_temp if not box.is_wall else box

    def sub_condition_2D(self, q, tree, third_inter):
        if q.is_empty_z:
            return tree.tree.count((q.interval_x.lower,  q.interval_y.lower, third_inter.lower,
                                        q.interval_x.upper, q.interval_y.upper,  third_inter.lower)) > 0
        elif q.is_empty_y:
            return tree.tree.count((q.interval_x.lower, third_inter.lower, q.interval_y.lower,
                                    q.interval_x.upper, third_inter.lower, q.interval_z.upper)) > 0
        elif q.is_empty_x:
            return tree.tree.count((third_inter.lower, q.interval_y.lower, q.interval_z.lower,
                                    third_inter.lower, q.interval_y.upper, q.interval_z.upper)) > 0

    def sub_condition_3D(self, q, tree3D):
        return tree3D.tree.count((q.interval_x.lower, q.interval_y.lower, q.interval_z.lower, q.interval_x.upper, q.interval_y.upper, q.interval_z.upper)) > 0

    def condition3D(self, q, tree3D, third_inter):
        if q.is_wall:
            if self.sub_condition_2D(q, tree3D, third_inter):
                return True
            else:
                return False
        else:
            if self.sub_condition_3D(q, tree3D):
                return True
            else:
                return False

    def condition2D_xy(self, q, tree2D):
        if tree2D.tree.count((q.interval_x.lower, q.interval_y.lower, q.interval_x.upper, q.interval_y.upper)) > 0:
             j = list(tree2D.tree.intersection((q.interval_x.lower, q.interval_y.lower, q.interval_x.upper, q.interval_y.upper), objects=True))[0]
             if j.object[2] == q.interval_z or j.object[2] in q.interval_z:
                 return True
             else:
                 return False
        else:
            return False

    def condition2D_xz(self, q, tree2D):
        if tree2D.tree.count((q.interval_x.lower, q.interval_z.lower, q.interval_x.upper, q.interval_z.upper)) > 0:
            j = list(tree2D.tree.intersection(
                (q.interval_x.lower, q.interval_y.lower, q.interval_x.upper, q.interval_y.upper), objects=True))[0]
            if j.object[1] == q.interval_y or j.object[1] in q.interval_y:
                return True
            else:
                return False
        else:
            return False

    def condition2D_yz(self, q, tree2D):
        if tree2D.tree.count((q.interval_y.lower, q.interval_z.lower, q.interval_y.upper, q.interval_z.upper)) > 0:
            j = list(tree2D.tree.intersection(
                (q.interval_x.lower, q.interval_y.lower, q.interval_x.upper, q.interval_y.upper), objects=True))[0]
            if j.object[0] == q.interval_x or j.object[0] in q.interval_x:
                return True
            else:
                return False
        else:
            return False

    def get_first_tree_object(self, q, tree_temp, dimensions):
        if dimensions == 3:
            i = list(tree_temp.tree.intersection((q.interval_x.lower, q.interval_y.lower, q.interval_z.lower, q.interval_x.upper,
                                             q.interval_y.upper, q.interval_z.upper), objects=True))[0]
            return [i.object.interval_x, i.object.interval_y, i.object.interval_z], i.object.iD
        elif dimensions == 2:
            temp = list(tree_temp.tree.intersection((q[0].lower, q[1].lower, q[0].upper, q[1].upper), objects=True))[0]
            return temp.object

    def wall_into_tree(self, box):
        if mylen(box.interval_x) == 0:
            return [box.interval_y.lower, box.interval_z.lower, box.interval_y.upper, box.interval_z.upper, box.interval_x, box.iD]
        elif mylen(box.interval_y) == 0:
            return [box.interval_x.lower, box.interval_y.lower, box.interval_x.upper, box.interval_z.upper, box.interval_y, box.iD]
        elif mylen(box.interval_z) == 0:
            return [box.interval_x.lower, box.interval_y.lower, box.interval_x.upper, box.interval_y.upper, box.interval_z, box.iD]

    def add_to_tree(self, iD2, q, tree2D_xy, tree2D_yz, tree2D_xz):
        q = self.wall_into_tree(q)
        if mylen(q[2]) == 0:
            tree2D_xy.tree.add(q[5], (q[0], q[1], q[2], q[3]), q)
        if mylen(q[1]) == 0:
            tree2D_xz.tree.add(q[5], (q[0], q[1], q[2], q[3]), q)
        if mylen(q[0]) == 0:
            tree2D_yz.tree.add(q[5], (q[0], q[1], q[2], q[3]), q)
        return q, tree2D_xy, tree2D_yz, tree2D_xz


    def sub_algo_2D(self, q, j, Q, tree, inter, iD, iD2, id_list, tree2D_where_interval):
        res, id_list, iD, iD2 = self.rotate_and_execute2D(q, j, id_list, iD, iD2)
        #wprowadzenie wyniku rozbicia na stos
        j = [j.interval_x, j.interval_y, j.interval_z]
        j = self.wall_into_tree(box3D(j[0], j[1], j[2]))
        Q.extend(res)
        #tree.tree.delete(i.id, (i.bbox[0], id.bbox[1], i.bbox[2], i.bbox[3], i.bbox[4], i.bbox[5]))
        #usunięcie starego pudełka z drzewa
        if any([i == q.iD for i in id_list[1]]):
            j = tree2D_where_interval[str(inter[5])]
            j = box3D(j[0], j[1], j[2], j[3])
        else:
            j = inter
        return j, q, Q, tree, inter, iD, iD2, id_list

    @staticmethod
    def execute(box_list):
        '''
        Funkcja statyczna, która przyjmuje listę pudełek i zwraca listę rozbitych pudełek\n
        :param box_list: lista pudełek do rozbicia\n
        :return: lista pudełek po rozbiciu\n
        :rtype: list
        '''
        Q, drzewo, drzewo2D_xy, drzewo2D_yz, drzewo2D_xz = boxStack(), tree(), tree2D_xy(), tree2D_yz(), tree2D_xz()
        Q.extend(box_list)
        return algorithm().algorytm(Q, tree,  drzewo2D_xy,  drzewo2D_yz,  drzewo2D_xz)
        #return drzewo

    @staticmethod
    def algorytm(Q, tree3D, tree2D_xy, tree2D_yz, tree2D_xz):
        '''
        Funkcja statyczna, w wyniku której wszystkie przecinające się
        pudełka ze stosu zostają rozbite i wstawione do drzewa
        :param Q: stos pudełek \n
        :param tree3D: puste drzewo z indeksowaniem w trzech wymiarach\n
        :return: drzewo rtree zawierające pudełka\n
        :rtype: tree.tree
        '''
        #obiekt klasy myInterval
        my_int = myInterval()
        tree2D_where_interval = {}
        #zmienna potrzebna do wprowadzania pudełka w unikalne miejsce do drzewa
        iD, iD2 = 1, 1
        id_list = [[0], [0]]
        algo, oper, stack_res = algorithm(), WallOperations(), boxStack()
        #pętla działa dopóki stos nie zostanie pusty
        while not Q.empty():
            #zdjęcie ostatniego pudełka ze stosu i przycięcie go
            q = Q.pop()
            q = my_int.box_cut(q)
            q_third = oper.check_if_wall(q)
            if algo.condition3D(q, tree3D, q_third):
                '''
                Sprawdzenie czy pudełko q przecina się z którymkolwiek elementem z drzewa.
                Jeśli tak, pudełko przecinające się zostaje pobrane z drzewa i usunięte,
                zaś wynik rozbicia zostaje wstawiony ponownie na stos pudełek
                '''
                inter, q_iD = algo.get_first_tree_object(q, tree3D, 3)
                j = box3D(inter[0], inter[1], inter[2], q_iD)
                tree3D.tree.delete(j.iD, (j.interval_x.lower, j.interval_y.lower, j.interval_z.lower, j.interval_x.upper, j.interval_y.upper, j.interval_z.upper))
                q = my_int.box_uncut(q)
                j = my_int.box_uncut(j)
                #cofnięcie przycięcia dla pudełek które mają być rozbite
                Q.extend(algorithm().rotate_and_execute(q, j, id_list))

            elif algo.condition2D_xy(q, tree2D_xy):
                inter = algo.get_first_tree_object([q.interval_y, q.interval_z], tree2D_yz, 2)
                j = box3D(my_closed(inter[0], inter[2]), my_closed(inter[1], inter[3]), inter[4],  inter[5])
                tree2D_xy.tree.delete(iD2, (j.interval_x.lower, j.interval_y.lower, j.interval_x.upper, j.interval_y.upper))
                j, q, Q, tree, inter, iD, iD2, id_list = algo.sub_algo_2D(q, j, Q, tree2D_xy, inter, iD, iD2, id_list, tree2D_where_interval)

            elif algo.condition2D_yz(q, tree2D_yz):
                inter = algo.get_first_tree_object([q.interval_y, q.interval_z], tree2D_yz, 2)
                j = box3D(my_closed(inter[0], inter[2]), my_closed(inter[1], inter[3]), inter[4],  inter[5])
                tree2D_xy.tree.delete(iD2, (j.interval_y.lower, j.interval_z.lower, j.interval_y.upper, j.interval_z.upper))
                j, q, Q, tree, inter, iD, iD2, id_list = algo.sub_algo_2D(q, j, Q, tree2D_yz, inter, iD, iD2, id_list, tree2D_where_interval)

            elif algo.condition2D_xz(q, tree2D_xz):
                inter = algo.get_first_tree_object([q.interval_x, q.interval_z], tree2D_xz, 2)
                j = box3D(my_closed(inter[0], inter[2]), my_closed(inter[1], inter[3]), inter[4],  inter[5])
                tree2D_xy.tree.delete(iD2, (j.interval_x.lower, j.interval_z.lower, j.interval_x.upper, j.interval_z.upper))
                j, q, Q, tree, inter, iD, iD2, id_list = algo.sub_algo_2D(q, j, Q, tree2D_xz, inter, iD, iD2, id_list, tree2D_where_interval)

            else:
                if not q.is_wall:
                    q = box3D(q.interval_x, q.interval_y, q.interval_z, max(id_list[0]) + 1)
                    id_list[0].append(max(id_list[0]) + 1)
                    tree3D.tree.add(q.iD, (q.interval_x.lower, q.interval_y.lower, q.interval_z.lower, q.interval_x.upper, q.interval_y.upper, q.interval_z.upper), q)
                    iD = max(id_list[0]) + 1
                else:
                    q = box3D(q.interval_x, q.interval_y, q.interval_z, max(id_list[1]) + 1)
                    id_list[1].append(max(id_list[1]) + 1)
                    val = {str(iD) : (q.interval_x, q.interval_y, q.interval_z, q.iD)}
                    iD2 = max(id_list[1]) + 1
                    print(val)
                    tree2D_where_interval.update(val)
                    q, tree2D_xy, tree2D_yz, tree2D_xz  = algo.add_to_tree(iD2, q, tree2D_xy, tree2D_yz, tree2D_xz)
                    id_list[1].append(q[5])
        return tree3D, tree2D_xy, tree2D_yz, tree2D_xz

