import os, sys
sys.path.insert(0, os.path.abspath('.'))
from signatures_setup import *
from split_intervals_3D import *
from split_intervals_2D import *
from cut_box import *
from wall_operation import *
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
            try:
                i = list(tree_temp.tree.intersection((q.interval_x.lower, q.interval_y.lower, q.interval_z.lower, q.interval_x.upper,
                                             q.interval_y.upper, q.interval_z.upper), objects=True))[0]
                return i.object
            except:
                return None
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

    def quicksort_boxes_walls(self, q):
        if q.is_empty_x:
            q = ['wx', q.interval_x, [q.interval_y, q.interval_z]]
        elif q.is_empty_y:
            q = ['wy', q.interval_y, [q.interval_x, q.interval_z]]
        elif q.is_empty_z:
            q = ['wz', q.interval_z, [q.interval_x, q.interval_y]]
        return q

    def quicksort_boxes(self, Q):
        Q_temp, Q_res = [], {'b': [], 'wx': [], 'wy': [], 'wz': [],}
        for q in Q.get_stack():
            if not q.is_wall:
                Q_res['b'].append(q)
            elif q.is_wall:
                Q_temp = self.quicksort_boxes_walls(q)
                Q_res[Q_temp[0]].append([Q_temp[1], Q_temp[2]])
        return Q_res

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
        #obiekt klasy myInterval
        my_int = myInterval()
        tree2D_where_interval = {}
        #zmienna potrzebna do wprowadzania pudełka w unikalne miejsce do drzewa
        id_list = [[0], [0]]
        algo, oper, stack_res = algorithm(), WallOperations(), boxStack()
        Q, Q_res = algo.quicksort_boxes(Q), {}
        #pętla działa dopóki stos nie zostanie pusty
        are_walls_split = False if sum([len(Q['wx']) > 0, len(Q['wy']) > 0, len(Q['wz']) > 0]) > 0 else True
        are_boxes_split = False if len(Q['b']) > 0 else True
        while not (are_walls_split and are_boxes_split):
            #zdjęcie ostatniego pudełka ze stosu i przycięcie go
            if not are_boxes_split:
                '''
                Sprawdzenie czy pudełko q przecina się z którymkolwiek elementem z drzewa.
                Jeśli tak, pudełko przecinające się zostaje pobrane z drzewa i usunięte,
                zaś wynik rozbicia zostaje wstawiony ponownie na stos pudełek
                '''
                q = Q['b'].pop()
                if drzewo3D.tree.count((q.interval_x.lower,  q.interval_y.lower, q.interval_z.lower,
                                        q.interval_x.upper, q.interval_y.upper,  q.interval_z.upper)) > 0:
                    inter = algo.get_first_tree_object(q, drzewo3D, 3)
                    j = box3D(inter.interval_x, inter.interval_y, inter.interval_z, inter.iD)
                    drzewo3D.tree.delete(q.iD, (j.interval_x.lower, j.interval_y.lower, j.interval_z.lower, j.interval_x.upper, j.interval_y.upper, j.interval_z.upper))
                    j = WallCut().wall_uncut(j)
                    q, j = my_int.box_uncut(q), my_int.box_uncut(j)
                    boxes = [my_int.box_uncut(box) for box in
                             algorithm().rotate_and_execute(q, j, id_list)]
                    Q['b'].extend(boxes)
                else:
                    drzewo3D.tree.add(q.iD, (q.interval_x.lower, q.interval_y.lower, q.interval_z.lower, q.interval_x.upper, q.interval_y.upper, q.interval_z.upper), q)
                if len(Q['b']) == 0:
                    are_boxes_split = True
                    Q['b'] = drzewo3D.tree.ret_boxes()
            elif are_walls_split:
                x, y, z = [], [], []
                for wall in ['wx', 'wy', 'wz']:
                    q = Q[wall].pop()
                    while not len(Q[wall]) == 0:
                        if wall == 'wx':
                            if drzewo2D.tree.count(q.interval_y.lower, q.interval_z.lower, q.interval_y.upper, q.interval_z.upper):
                                inter = algo.get_first_tree_object(q, drzewo2D, 3)
                                j, j_iD = [inter.interval_y, inter.interval_z], inter.iD
                                drzewo2D[wall].extend(algo.rotate_and_execute2D(q, j, drzewo2D))
                                drzewo2D.tree.delete(j_iD, (q.interval_y.lower, q.interval_z.lower, q.interval_y.upper, q.interval_z.upper))
                            else:
                                drzewo2D.tree.add(q.iD, (
                                q.interval_y.lower, q.interval_z.lower, q.interval_y.upper, q.interval_z.upper))
                            if len(Q[wall]) == 0:
                                x = drzewo2D.ret_boxes()
                                drzewo2D = tree2D()
                        elif wall == 'wy':
                            if drzewo2D.tree.count(q.interval_x.lower, q.interval_z.lower, q.interval_x.upper,
                                                           q.interval_z.upper):
                                inter = algo.get_first_tree_object(q, drzewo2D, 3)
                                j, j_iD = [inter.interval_x, inter.interval_z], inter.iD
                                tree2D[wall].extend(algo.rotate_and_execute2D(q, j, drzewo2D))
                                drzewo2D.tree.delete(j_iD, (q.interval_x.lower, q.interval_z.lower, q.interval_x.upper, q.interval_z.upper))
                            else:
                                tree2D.tree.add(q.iD, (
                                q.interval_x.lower, q.interval_z.lower, q.interval_x.upper, q.interval_z.upper))
                            if Q[wall].empty:
                                y = drzewo2D.ret_boxes()
                                drzewo2D = tree2D()

                        elif wall == 'wz':
                            if drzewo2D.tree.count(q.interval_x.lower, q.interval_y.lower, q.interval_x.upper,
                                                           q.interval_y.upper):
                                inter = algo.get_first_tree_object(q, drzewo2D, 3)
                                j, j_iD = [inter.interval_x, inter.interval_y], inter.iD
                                tree2D[wall].extend(algo.rotate_and_execute2D(q, j, drzewo2D))
                                drzewo2D.tree.delete(j_iD, (q.interval_x.lower, q.interval_y.lower, q.interval_y.upper, q.interval_z.upper))
                            else:
                                tree2D.tree.add(q.iD, (q.interval_x.lower, q.interval_y.lower, q.interval_x.upper, q.interval_y.upper))
                            if Q[wall].empty:

                                z = drzewo2D.ret_boxes()
                                drzewo2D = tree2D()
        Q['wx'].extend(x)
        Q['wy'].extend(y)
        Q['wz'].extend(z)

        return Q

