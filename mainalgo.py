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

    def add_to_tree(self, q, tree2D):
        if q.is_empty_z:
            tree2D.tree.insert(q.iD, (q.interval_x.lower, q.interval_y.lower, q.interval_x.upper, q.interval_y.upper), q.iD)
        elif q.is_empty_y:
            tree2D.tree.insert(q.iD, (q.interval_x.lower, q.interval_z.lower, q.interval_x.upper, q.interval_z.upper), q.iD)
        elif q.is_empty_x:
            tree2D.tree.insert(q.iD, (q.interval_y.lower, q.interval_z.lower, q.interval_y.upper, q.interval_z.upper), q.iD)
        return q, tree2D

    @staticmethod
    def convert_closed_to_my_closed(closed_b):
        my_closed_box = box3D(my_closed(closed_b.interval_x.lower, closed_b.interval_x.upper), my_closed(closed_b.interval_y.lower, closed_b.interval_y.upper), my_closed(closed_b.interval_z.lower, closed_b.interval_z.upper), closed_b.iD)
        return my_closed_box

    def quicksort_boxes_walls(self, Q_res, q, iD):
        Q_res['wx'].append(box3D(my_closed(q.interval_x.lower, q.interval_x.lower), q.interval_y, q.interval_z, iD))
        iD += 1
        Q_res['wx'].append(box3D(my_closed(q.interval_x.upper, q.interval_x.upper), q.interval_y, q.interval_z, iD))
        iD += 1
        Q_res['wy'].append(box3D(q.interval_x, my_closed(q.interval_y.lower, q.interval_y.lower), q.interval_z, iD))
        iD += 1
        Q_res['wy'].append(box3D(q.interval_x, my_closed(q.interval_y.upper, q.interval_y.upper), q.interval_z, iD))
        iD += 1
        Q_res['wz'].append(box3D(q.interval_x, q.interval_y, my_closed(q.interval_z.lower, q.interval_z.lower), iD))
        iD += 1
        Q_res['wz'].append(box3D(q.interval_x, q.interval_y, my_closed(q.interval_z.upper, q.interval_z.upper), iD))
        iD += 1
        return Q_res, iD

    def quicksort_boxes(self, Q):
        Q_temp, Q_res, iD, iD2 = [], {'b': [], 'wx': [], 'wy': [], 'wz': []}, 0, 0
        for q in Q.get_stack():
            q = box3D(q.interval_x, q.interval_y, q.interval_z, iD)
            Q_res['b'].append(q)
            Q_res, iD2 = self.quicksort_boxes_walls(Q_res, q, iD2)
            iD += 1
        return Q_res, iD

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
        list_sign, id_list, Q_res, x, y, z = ['wx', 'wy', 'wz'], [[0], [0]], {'b':[], 'wx':[], 'wy':[], 'wz':[]}, [], [], []
        #pętla działa dopóki stos nie zostanie pusty
        are_boxes_split = False if len(Q['b']) > 0 else True
        are_walls_split = False if not are_boxes_split else True
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
                    j = list(drzewo3D.tree.intersection((q.interval_x.lower,  q.interval_y.lower, q.interval_z.lower,
                                        q.interval_x.upper, q.interval_y.upper,  q.interval_z.upper), objects=True))[0].object
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
                i = 0
                for wall in list_sign:
                    while len(Q[wall]) != 0:
                        q = Q[wall].pop()
                        q = algo.convert_closed_to_my_closed(q)
                        q = WallCut().wall_cut(q)
                        if algo.check_if_intersect_2D_single(q, drzewo2D, Q_res, False, drzewo2D.ret_boxes()):
                            Q = algorithm.sub_algo_2D(wall, drzewo2D, q, Q, Q_res)
                        else:
                            Q_res[wall].append(q)
                            algo.add_to_tree(q, drzewo2D)
                are_walls_split = True
        return Q_res

    @staticmethod
    def sub_algo_2D(wall, drzewo2D, q, Q, Q_res_wall):
        j, Q_res_wall = algorithm().check_if_intersect_2D(q, drzewo2D, Q, Q_res_wall, True)
        j, j_iD = algorithm.get_new_intervals_2D(j), j.iD
        j_list = [WallCut.wall_uncut(wall) for wall in boxOperations().rotate_and_execute2D(q, j, drzewo2D)]
        drzewo2D[wall].extend(j_list)
        drzewo2D.tree.delete(j_iD, (q.interval_y.lower, q.interval_z.lower, q.interval_y.upper, q.interval_z.upper))
        return Q_res_wall

    def cut_out_dictionary_elem(self, Q_res, j):
        if j.is_empty_x:
            Q_res['wx'].remove(j)
        elif j.is_empty_y:
            Q_res['wy'].remove(j)
        elif j.is_empty_z:
            Q_res['wz'].remove(j)
        return Q_res

    def check_if_intersect_2D_single(self, q, drzewo2D, Q_res, ret=False, j=None):
        if j == None:
            j = drzewo2D.ret_boxes(Q_res)
        j = [self.return_full_boxes(wall, Q_res) for wall in j]
        wall_cut = WallCut()
        for box in j:
            if ret:
                if wall_cut.check_if_walls_intersect(q, box):
                    Q_res = self.cut_out_dictionary_elem(Q_res, box)
                    return box, Q_res
                else:
                    continue
            else:
                if wall_cut.check_if_walls_intersect(q, box):
                    return True
                else:
                    continue
        return False

    def return_full_boxes(self, j, Q_res):
        ret, i = [], 0
        for wall in ['wx', 'wy', 'wz']:
            for box in Q_res[wall]:
                if box == j.iD:
                    ret.append(box3D(Q_res[wall][i].interval_x, Q_res[wall][i].interval_y, Q_res[wall][i].interval_z, Q_res[wall][i].iD))
                    break
        return ret

    def check_if_intersect_2D(self, q, drzewo2D, Q,  Q_res, ret):
        j = drzewo2D.ret_boxes(Q_res)
        temp, Q_res = self.check_if_intersect_2D_single(q, drzewo2D, Q, ret, j)
        return temp, Q

    @staticmethod
    def get_new_intervals_2D(box):
        if box.is_empty_x:
            return [box.interval_y, box.interval_z]
        elif box.is_empty_y:
            return [box.interval_x, box.interval_z]
        elif box.is_empty_z:
            return [box.interval_x, box.interval_y]
