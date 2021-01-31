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
    os.remove('2d_index.idx')
    os.remove('2d_index.dat')
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


    def cut_pieces2D(self, wall_res, box):
        if mylen(wall_res[0]) < mylen(box[0]) and mylen(wall_res[1]) < mylen(box[1]):
            return None
        else:
            if mylen(wall_res[0]) > mylen(box[0]):
                wall_res[0] = wall_res[0] - box[0]
            elif mylen(wall_res[0]) < mylen(box[0]):
                wall_res[0] = box[0]
            if mylen(wall_res[1]) > mylen(box[1]):
                wall_res[1] = wall_res[1] - box[1]
            elif mylen(wall_res[1]) < mylen(box[1]):
                wall_res[1] = box[0]
            return wall_res if wall_res[0] and wall_res[1] else None

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

    def condition3D(self, q, tree, third_inter):
        if tree.tree.count((q.interval_x.lower,  q.interval_y.lower, q.interval_z.lower,
                                        q.interval_x.upper, q.interval_y.upper,  q.interval_z.upper)) > 0:
            return True
        else:
            return False


    def condition2D(self, q, tree2D):
        if tree2D.tree.count((q.interval_x.lower, q.interval_y.lower, q.interval_x.upper, q.interval_y.upper)) > 0:
            return True
        else:
            return False

    def update_dict_where(self, q, iD, update_dict):
        update_dict.update({iD : q})
        return update_dict

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
            return [box.interval_y.lower, box.interval_z.lower, box.interval_y.upper, box.interval_z.upper, box.interval_x.lower, box.iD]
        elif mylen(box.interval_y) == 0:
            return [box.interval_x.lower, box.interval_y.lower, box.interval_x.upper, box.interval_z.upper, box.interval_y.lower, box.iD]
        elif mylen(box.interval_z) == 0:
            return [box.interval_x.lower, box.interval_y.lower, box.interval_x.upper, box.interval_y.upper, box.interval_z.lower, box.iD]

    @staticmethod
    def execute(box_list):
        '''
        Funkcja statyczna, która przyjmuje listę pudełek i zwraca listę rozbitych pudełek\n
        :param box_list: lista pudełek do rozbicia\n
        :return: lista pudełek po rozbiciu\n
        :rtype: list
        '''
        Q, drzewo, drzewo2D = boxStack(), tree(), tree2D()
        Q.extend(box_list)
        algorithm().algorytm(Q, drzewo, drzewo2D)
        return drzewo, drzewo2D
        #return drzewo

    @staticmethod
    def algorytm(Q, tree, tree2D):
        '''
        Funkcja statyczna, w wyniku której wszystkie przecinające się
        pudełka ze stosu zostają rozbite i wstawione do drzewa
        :param Q: stos pudełek \n
        :param tree: puste drzewo z indeksowaniem w trzech wymiarach\n
        :return: drzewo rtree zawierające pudełka\n
        :rtype: tree.tree
        '''
        #obiekt klasy myInterval
        my_int, tree2D_where_interval = myInterval(), {}
        #zmienna potrzebna do wprowadzania pudełka w unikalne miejsce do drzewa
        iD, iD2 = 0, 0
        id_list = [[], []]
        algo, oper, stack_res = algorithm(), WallOperations(), boxStack()
        #pętla działa dopóki stos nie zostanie pusty
        while not Q.empty():
            #zdjęcie ostatniego pudełka ze stosu i przycięcie go
            q = Q.pop()
            q = my_int.box_cut(q)
            q_third = oper.check_if_wall(q)
            if algo.condition3D(q, tree, q_third):
                '''
                Sprawdzenie czy pudełko q przecina się z którymkolwiek elementem z drzewa.
                Jeśli tak, pudełko przecinające się zostaje pobrane z drzewa i usunięte,
                zaś wynik rozbicia zostaje wstawiony ponownie na stos pudełek
                '''
                inter, obj_id = algo.get_first_tree_object(q, tree, 3)
                j = box3D(inter[0], inter[1], inter[2], obj_id)
                q = my_int.box_uncut(q)
                j = my_int.box_uncut(j)
                #cofnięcie przycięcia dla pudełek które mają być rozbite
                Q.extend(algorithm().rotate_and_execute(q, j, id_list))
                tree.tree.delete(j.iD, (j.interval_x.lower, j.interval_y.lower, j.interval_z.lower, j.interval_x.upper, j.interval_y.upper, j.interval_z.upper))

            elif algo.condition2D(q, tree2D):
                if q.is_empty_x:
                    q_temp = [q.interval_y, q.interval_z]
                elif q.is_empty_y:
                    q_temp = [q.interval_x, q.interval_z]
                else:
                    q_temp = [q.interval_x, q.interval_y]
                inter = algo.get_first_tree_object(q_temp, tree2D, 2)
                inter = tree2D_where_interval[inter[5]]
                j = inter
                if q.is_wall:
                    res, id_list, iD, iD2 = algorithm().rotate_and_execute2D(q, j, id_list, iD, iD2)
                else:
                    res, id_list, iD, iD2 = algorithm().rotate_and_execute2D(j, q, id_list, iD, iD2)
                #wprowadzenie wyniku rozbicia na stos
                Q.extend(res)
                j_iD = j.iD
                j = algo.wall_into_tree(j)
                #tree.tree.delete(i.id, (i.bbox[0], id.bbox[1], i.bbox[2], i.bbox[3], i.bbox[4], i.bbox[5]))
                #usunięcie starego pudełka z drzewa
                tree2D.tree.delete(j_iD, (j[0], j[1], j[2], j[3]))
            else:
                #tree.tree.add(iD, (q.interval_x.lower, q.interval_y.lower, q.interval_z.lower, q.interval_x.upper, q.interval_y.upper, q.interval_z.upper), q)
                stack_res.extend([q])
                #dodanie nowego pudełka do drzewa i zwiększenie zmiennej iD o 1
                if not q.is_wall:
                    id_list[0].append(q.iD)
                    tree.tree.add(iD, (q.interval_x.lower, q.interval_y.lower, q.interval_z.lower, q.interval_x.upper, q.interval_y.upper, q.interval_z.upper), q)
                    iD = max(id_list[0]) + 1
                else:
                    q = box3D(q.interval_x, q.interval_y, q.interval_z, iD2)
                    tree2D_where_interval = algo.update_dict_where(q, q.iD, tree2D_where_interval)
                    q = algo.wall_into_tree(q)
                    tree2D.tree.add(iD2, (q[0], q[1], q[2], q[3]), q)
                    id_list[1].append(q[5])
                    iD2 = max(id_list[1]) + 1
        return tree, tree2D

