import os, sys
sys.path.insert(0, os.path.abspath('.'))
from signatures_setup import *
from split_intervals_3D import *
from split_intervals_2D import *
from cut_box_3D import *
from cut_box_2D import *
from different_boxtype_operations import *
from boxes_3D import *
from boxes_2D import *

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

    def get_first_tree_object(self, q, tree_temp, dimensions):
        if dimensions == 3:
            i = list(tree_temp.tree.intersection((q.interval_x.lower, q.interval_y.lower, q.interval_z.lower, q.interval_x.upper,
                                         q.interval_y.upper, q.interval_z.upper), objects=True))[0]
            return i.object
        elif dimensions == 2:
            temp = list(tree_temp.tree.intersection((q[0].lower, q[1].lower, q[0].upper, q[1].upper), objects=True))[0]
            return temp.object

    def add_to_tree(self, iD2, q, tree2D):
        if q.is_wall and q.is_empty_z:
            tree2D.tree.add(q.iD, (q.interval_x.lower, q.interval_y.lower, q.interval_x.upper, q.interval_y.upper), q)
        elif q.is_wall and q.is_empty_y:
            tree2D.tree.add(q.iD, (q.interval_x.lower, q.interval_z.lower, q.interval_x.upper, q.interval_z.upper), q)
        elif q.is_wall and q.is_empty_x:
            tree2D.tree.add(q.iD, (q.interval_y.lower, q.interval_z.lower, q.interval_y.upper, q.interval_z.upper), q)
        return q, tree2D

    def dictionary_update_val(self, q):
        if q.is_empty_x:
            val = {str(q.iD): (q.interval_x)}
        elif q.is_empty_y:
            val = {str(q.iD): (q.interval_y)}
        elif q.is_empty_z:
            val = {str(q.iD): (q.interval_z)}
        return val

    @staticmethod
    def convert_closed_to_my_closed(closed_b):
        my_closed_box = box3D(my_closed(closed_b.interval_x.lower, closed_b.interval_x.upper), my_closed(closed_b.interval_y.lower, closed_b.interval_y.upper), my_closed(closed_b.interval_z.lower, closed_b.interval_z.upper), closed_b.iD)
        return my_closed_box

    def quicksort_boxes_walls(self, Q_res, q, iD):
        Q_res['wx'].append([q.interval_x.lower, q.interval_y, q.interval_z])
        Q_res['wx'].append([q.interval_x.upper, q.interval_y, q.interval_z])
        Q_res['wy'].append([q.interval_x, q.interval_y.lower, q.interval_z])
        Q_res['wy'].append([q.interval_x, q.interval_y.upper, q.interval_z])
        Q_res['wz'].append([q.interval_x, q.interval_y, q.interval_z.lower])
        Q_res['wz'].append([q.interval_x, q.interval_y, q.interval_z.upper])
        return Q_res

    def quicksort_boxes(self, Q):
        Q_temp, Q_res, iD = [], {'b': [], 'wx': [], 'wy': [], 'wz': []}, 0
        for q in Q.get_stack():
            if not q.is_wall:
                q = box3D(q.interval_x, q.interval_y, q.interval_z, iD)
                iD += 1
                Q_res['b'].append(q)
                Q_res = self.quicksort_boxes_walls(Q_res, q, iD)
        return Q_res, iD

    @staticmethod
    def execute(box_list):
        '''
        Funkcja statyczna, która przyjmuje listę pudełek i zwraca listę rozbitych pudełek\n
        :param box_list: lista pudełek do rozbicia\n
        :return: lista pudełek po rozbiciu\n
        :rtype: list
        '''
        Q, drzewo, drzewo2D= boxStack(), tree(), tree2D()
        Q.extend(box_list)
        return algorithm().algorytm(Q, tree,  drzewo2D)
        #return drzewo



    @staticmethod
    def algorytm(Q, drzewo3D, drzewo2D):
        '''
        Funkcja statyczna, w wyniku której wszystkie przecinające się
        pudełka ze stosu zostają rozbite i wstawione do drzewa
        :param Q: stos pudełek \n
        :param tree3D: puste drzewo z indeksowaniem w trzech wymiarach\n
        :return: drzewo rtree zawierające pudełka\n
        :rtype: tree.tree
        '''
        #zmienna potrzebna do wprowadzania pudełka w unikalne miejsce do drzewa
        my_int, algo, oper, stack_res = myInterval(), algorithm(), boxOperations(), boxStack()
        Q, iD = algo.quicksort_boxes(Q)
        id_list, Q_res, x, y, z = [[0], [0]], {}, [], [], []
        #pętla działa dopóki stos nie zostanie pusty
        are_boxes_split = False if len(Q['b']) > 0 else True
        are_walls_split = False if are_boxes_split else True
        Q_res_wall, list_sign = {'wx': [], 'wy': [], 'wz': []}, ['wx', 'wy', 'wz']
        while not (are_walls_split and are_boxes_split):
            #zdjęcie ostatniego pudełka ze stosu i przycięcie go
            if not are_boxes_split:
                '''
                Sprawdzenie czy pudełko q przecina się z którymkolwiek elementem z drzewa.
                Jeśli tak, pudełko przecinające się zostaje pobrane z drzewa i usunięte,
                zaś wynik rozbicia zostaje wstawiony ponownie na stos pudełek
                '''
                q = Q['b'].pop()
                q = my_int.box_cut(q)
                if drzewo3D.tree.count((q.interval_x.lower,  q.interval_y.lower, q.interval_z.lower,
                                        q.interval_x.upper, q.interval_y.upper,  q.interval_z.upper)) > 0:
                    j = algo.get_first_tree_object(q, drzewo3D, 3)
                    j = box3D(j.interval_x, j.interval_y, j.interval_z, j.iD)
                    drzewo3D.tree.delete(j.iD, (j.interval_x.lower, j.interval_y.lower, j.interval_z.lower, j.interval_x.upper, j.interval_y.upper, j.interval_z.upper))
                    q, j = my_int.box_uncut(q), my_int.box_uncut(j)
                    temp, iD = oper.rotate_and_execute(q, j, iD)
                    Q['b'].extend(temp)
                else:
                    drzewo3D.tree.insert(q.iD, (q.interval_x.lower, q.interval_y.lower, q.interval_z.lower, q.interval_x.upper, q.interval_y.upper, q.interval_z.upper), q)
                if len(Q['b']) == 0:
                    are_boxes_split = True
                    Q_res['b'] = drzewo3D.ret_boxes()
            elif not are_walls_split:
                for wall in list_sign:
                    q = Q[wall].pop()
                    while not len(Q[wall]) == 0:
                        if algo.check_if_intersect_2D_single(q, drzewo2D, Q, Q_res, False):
                            Q, Q_res_wall = algorithm.sub_algo_2D(wall, drzewo2D, q, Q, Q_res_wall)
                        else:
                            Q_res_wall[wall].append(q)
                            drzewo2D.tree.insert(q.iD, (q.interval_y.lower, q.interval_z.lower, q.interval_y.upper, q.interval_z.upper))
                        if len(Q[wall]) == 0:
                            list_sign.pop(0)
                        if len(wall) == 0:
                            are_walls_split = True
        Q['b'].extend(Q_res['b'])
        for wall in ['wx', 'wy', 'wz']:
            Q[wall].extend(Q_res_wall[wall])
        return Q

    @staticmethod
    def sub_algo_2D(wall, drzewo2D, q, Q, Q_res_wall):
        j, Q_res = algorithm().check_if_intersect_2D(q, drzewo2D, Q, True)
        j, j_iD = algorithm.get_new_intervals_2D(j), j.iD
        j_list = [WallCut.wall_cut(wall) for wall in boxOperations().rotate_and_execute2D(q, j, drzewo2D)]
        drzewo2D[wall].extend(j_list)
        drzewo2D.tree.delete(j_iD, (q.interval_y.lower, q.interval_z.lower, q.interval_y.upper, q.interval_z.upper))
        return Q, Q_res_wall

    def cut_out_dictionary_elem(self, Q_res, j):
        if j.is_empty_x:
            Q_res['wx'].remove(j)
        elif j.is_empty_y:
            Q_res['wy'].remove(j)
        elif j.is_empty_z:
            Q_res['wz'].remove(j)
        return Q_res

    def check_if_intersect_2D_single(self, q, drzewo2D, Q_res, ret = False, j = None):
        if ret:
            if j:
                Q_res = self.cut_out_dictionary_elem(Q_res, j.object)
                return j.object, Q_res
            else:
                return True
        else:
            return False

    def return_full_boxes(self, box_list, Q_res):
        ret, i = [], 0
        for box in box_list:
            for wall in ['wx', 'wy', 'wz']:
                if Q_res[wall][i].iD == box.iD:
                    ret.append(box3D(box.interval_x, box.interval_y, box.interval_z, box.iD))
                    Q_res[wall].pop(i)
                    i = 0
                    break
            i += 1
        return ret

    def check_if_intersect_2D(self, q, drzewo2D, Q,  Q_res, ret):
        j = self.return_full_boxes(drzewo2D.ret_boxes(), Q_res)
        temp, Q_res = self.check_if_intersect_2D_single(q, drzewo2D, Q_res, True, j)
        return temp, Q_res

    @staticmethod
    def get_new_intervals_2D(self, box):
        if box.is_empty_x:
            return [box.interval_y, box.interval_z]
        elif box.is_empty_y:
            return [box.interval_x, box.interval_z]
        elif box.is_empty_z:
            return [box.interval_x, box.interval_y]
