import os, sys
sys.path.insert(0, os.path.abspath('.'))
from different_boxtype_operations import *
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

    def add_to_tree(self, q, drzewo2D):
        if q.is_empty_z:
            drzewo2D.tree.insert(q.iD, (q.interval_x.lower, q.interval_y.lower, q.interval_x.upper, q.interval_y.upper), q)
        elif q.is_empty_y:
            drzewo2D.tree.insert(q.iD, (q.interval_x.lower, q.interval_z.lower, q.interval_x.upper, q.interval_z.upper), q)
        elif q.is_empty_x:
            drzewo2D.tree.insert(q.iD, (q.interval_y.lower, q.interval_z.lower, q.interval_y.upper, q.interval_z.upper), q)
        return drzewo2D

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
                for wall in list_sign:
                    while len(Q[wall]) != 0:
                        q = Q[wall].pop()
                        if algo.check_if_intersect_2D_single(q, drzewo2D.ret_boxes(Q_res)):
                            j = algo.check_if_intersect_2D_single(q, drzewo2D.ret_boxes(Q_res))
                            Q, drzewo2D, id_list = algo.sub_algo_2D(j, drzewo2D, q, Q, id_list)
                            Q_res = algo.cut_out_dictionary_elem(Q_res, j)
                        else:
                            Q_res[algo.check_which_wall(q)].append(q)
                            drzewo2D = algo.add_to_tree(q, drzewo2D)
                are_walls_split = True
        return Q_res

    @staticmethod
    def sub_algo_2D(j, drzewo2D, q, Q, iD_list):
        algo, j_iD = algorithm(), j.iD
        drzewo2D = algo.delete_from_tree(drzewo2D, j)
        q, third_int_1, where_third = algorithm.get_new_intervals_2D(q)
        j, third_int_2, where_third = algorithm.get_new_intervals_2D(j)
        j_list, iD_list = boxOperations().rotate_and_execute2D(q, j, iD_list, [third_int_1, third_int_2])
        for iter in j_list:
            wall = algo.check_which_wall(iter)
            Q[wall].append(iter)
        return Q, drzewo2D, iD_list

    def delete_from_tree(self, drzewo2D, j):
        if j.is_empty_x:
            drzewo2D.tree.delete(j.iD, (j.interval_y.lower, j.interval_z.lower, j.interval_y.upper, j.interval_z.upper))
        elif j.is_empty_y:
            drzewo2D.tree.delete(j.iD, (j.interval_x.lower, j.interval_z.lower, j.interval_x.upper, j.interval_z.upper))
        elif j.is_empty_z:
            drzewo2D.tree.delete(j.iD, (j.interval_x.lower, j.interval_y.lower, j.interval_x.upper, j.interval_y.upper))
        return drzewo2D

    def cut_out_dictionary_elem(self, Q_res, j):
        if j.is_empty_x:
            wall = 'wx'
        elif j.is_empty_y:
            wall = 'wy'
        elif j.is_empty_z:
            wall = 'wz'
        iterator = 0
        for box in Q_res[wall]:
            if sum([box.interval_x == j.interval_x, box.interval_y == j.interval_y, box.interval_z == j.interval_z]) == 3:
                Q_res[wall].pop(iterator)
                return Q_res
            iterator += 1

    def check_which_wall(self, j):
        if j.is_empty_x:
            return "wx"
        if j.is_empty_y:
            return "wy"
        if j.is_empty_z:
            return "wz"

    def check_if_intersect_2D_single(self, q, j):
        wall_cut = WallCut()
        for box in j:
            if wall_cut.check_if_walls_intersect(q, box):
                return box
            else:
                continue
        return False

    def return_full_box(self, j, Q_res):
        ret, i = [], 0
        for wall in ['wx', 'wy', 'wz']:
            for box in Q_res[wall]:
                if box.iD == j.iD:
                    return box
        return None


    @staticmethod
    def get_new_intervals_2D(box):
        if box.is_empty_x:
            return [box.interval_y, box.interval_z], box.interval_x, 0
        elif box.is_empty_y:
            return [box.interval_x, box.interval_z], box.interval_y, 1
        elif box.is_empty_z:
            return [box.interval_x, box.interval_y], box.interval_z, 2
