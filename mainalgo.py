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
    def rotate_and_execute(self, box1, box2):
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

    def rotate_and_execute2D(self, wall, box):
        spl = WallOperations()
        box_temp = self.check_if_wall(wall, box)
        stack = spl.split_boxes([wall, box_temp])
        stack = stack.get_stack()
        sign = signatures()
        walls_inter, walls_not_inter = sign.intersection2D(box, stack)
        while not len(walls_inter) == 0:
            wall = walls_inter.pop()
            cond, cond_2 = sign.intersection2D(box, stack)
            if cond:
                if wall.interval_x.empty:
                    temp = self.cut_pieces2D([wall.interval_y, wall.interval_z], [box.interval_y, box.interval_z])
                    temp = box3D(temp.interval_x, wall.interval_y, wall.interval_z) if temp else None
                elif wall.interval_y.empty():
                    temp = self.cut_pieces2D([wall.interval_x, wall.interval_z], [box.interval_x, box.interval_z])
                    temp = box3D(wall.interval_x, temp.interval_y, wall.interval_z) if temp else None
                elif wall.interval_z.empty():
                    temp = self.cut_pieces2D([wall.interval_x, wall.interval_y], [box.interval_x, box.interval_y])
                    temp = box3D(wall.interval_x, wall.interval_y, temp.interval_z) if temp else None
                
                walls_inter.append(temp)
            else:
                walls_not_inter.append(wall)
        return walls_not_inter
        '''
        return stack

        stack_res = []
        for box_res in stack:
            checksum = self.execute2D_check(box_res, box_temp)
            if checksum == 3:
                if mylen(box.interval_y) == 0:
                    box_temp_2 = self.cut_pieces2D([box_res.interval_x, box_res.interval_z],
                                               [box.interval_x, box.interval_z])
                    if box_temp_2:
                        if box_temp_2[0] and box_temp_2[1]:
                            stack_res.append(box3D(box_temp_2[0], box.interval_y, box_temp_2[1]))
                        elif box_temp_2[1]:
                            stack_res.append(box3D(box_temp_2[0], box.interval_y, box_temp_2[1]))
                        elif box_temp_2[0]:
                            stack_res.append(box3D(box.interval_x, box.interval_y, box_temp_2[1]))

                elif mylen(box.interval_x) == 0:
                    box_temp_2 = self.cut_pieces2D([box_res.interval_y, box_res.interval_z],
                                                   [box.interval_y, box.interval_z])
                    if box_temp_2:
                        if box_temp_2[0] and box_temp_2[1]:
                            stack_res.append(box3D(box.interval_x, box_temp_2[0], box_temp_2[1]))
                        elif box_temp_2[1]:
                            stack_res.append(box3D(box.interval_x, box_temp_2[1], box.interval_z))
                        elif box_temp_2[0]:
                            stack_res.append(box3D(box.interval_x, box.interval_y, box_temp_2[1]))

                elif mylen(box.interval_z) == 0:
                    box_temp_2 = self.cut_pieces2D([box_res.interval_x, box_res.interval_y],
                                                   [box.interval_x, box.interval_y])
                    if box_temp_2:
                        if box_temp_2[0] and box_temp_2[1]:
                            stack_res.append(box3D(box_temp_2[0], box_temp_2[1], box.interval_z))
                        elif box_temp_2[1]:
                            stack_res.append(box3D(box.interval_x, box_temp_2[0], box.interval_z))
                        elif box_temp_2[0]:
                            stack_res.append(box3D(box_temp_2[0], box.interval_y, box.interval_z))
                else:
                    continue
        return stack_res
        '''

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
        box_temp = box3D(wall.interval_x, wall.interval_y, wall.interval_z)
        if not box.is_wall:
            if mylen(wall.interval_x) == 0:
                box_temp = box3D(wall.get_interval_x(), box.get_interval_y(), box.get_interval_z())
            elif mylen(wall.interval_y) == 0:
                box_temp = box3D(box.get_interval_x(), wall.get_interval_y(), box.get_interval_z())
            elif mylen(wall.interval_z) == 0:
                box_temp = box3D(box.get_interval_x(), box.get_interval_y(), wall.get_interval_z())
        return box_temp if not box.is_wall else box


    @staticmethod
    def execute(box_list):
        '''
        Funkcja statyczna, która przyjmuje listę pudełek i zwraca listę rozbitych pudełek\n
        :param box_list: lista pudełek do rozbicia\n
        :return: lista pudełek po rozbiciu\n
        :rtype: list
        '''
        Q, drzewo = boxStack(), tree()
        Q.extend(box_list)
        stos = algorithm().algorytm(Q, drzewo)
        return stos

        #return drzewo

		
    @staticmethod
    def algorytm(Q, tree):
        '''
        Funkcja statyczna, w wyniku której wszystkie przecinające się
        pudełka ze stosu zostają rozbite i wstawione do drzewa
        :param Q: stos pudełek \n
        :param tree: puste drzewo z indeksowaniem w trzech wymiarach\n
        :return: drzewo rtree zawierające pudełka\n
        :rtype: tree.tree
        '''
        #obiekt klasy myInterval
        my_int = myInterval()
        #zmienna potrzebna do wprowadzania pudełka w unikalne miejsce do drzewa
        iD = 0
        stack_res = boxStack()
        #pętla działa dopóki stos nie zostanie pusty
        while not Q.empty():
            #zdjęcie ostatniego pudełka ze stosu i przycięcie go
            q = Q.pop()
            q = my_int.box_cut(q)
            if not len([i.intersection(q) for i in stack_res.get_stack()]) == 0:
                '''
                Sprawdzenie czy pudełko q przecina się z którymkolwiek elementem z drzewa.
                Jeśli tak, pudełko przecinające się zostaje pobrane z drzewa i usunięte,
                zaś wynik rozbicia zostaje wstawiony ponownie na stos pudełek
                '''
                i = stack_res.pop(list.index([i.intersection(q) for i in stack_res.get_stack()][0]))#wycięte intersection drzewa
                inter = [i.object.interval_x, i.object.interval_y, i.object.interval_z]
                j = box3D(inter[0], inter[1], inter[2])
                q = my_int.box_uncut(q)
                j = my_int.box_uncut(j)
                #cofnięcie przycięcia dla pudełek które mają być rozbite
                if q.is_wall or j.is_wall:
                    if q.is_wall and j.is_wall:
                        Q.extend(algorithm().rotate_and_execute2D(q, j))
                    elif q.is_wall:
                        Q.extend(algorithm().rotate_and_execute2D(q, j))
                    elif j.is_wall:
                        Q.extend(algorithm().rotate_and_execute2D(j, q))
                else:
                    Q.extend(algorithm().rotate_and_execute(q, j))
                #wprowadzenie wyniku rozbicia na stos
                #tree.tree.delete(i.id, (i.bbox[0], i.bbox[1], i.bbox[2], i.bbox[3], i.bbox[4], i.bbox[5]))
                #usunięcie starego pudełka z drzewa
            else:
                #tree.tree.add(iD, (q.interval_x.lower, q.interval_y.lower, q.interval_z.lower, q.interval_x.upper, q.interval_y.upper, q.interval_z.upper), q)
                stack_res.extend([q])
                #dodanie nowego pudełka do drzewa i zwiększenie zmiennej iD o 1
                #iD += 1
            return stack_res