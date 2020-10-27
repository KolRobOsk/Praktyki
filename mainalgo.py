import os
sys.path.insert(0, os.path.abspath('.'))
from signatures_setup import *
from split_intervals import *
from cut_box import *

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

    def begin(self, box1, box2):
    '''
    :param box1: Pudełko zdjęte z stosu funkcją pop	      
    :type box2: box3D()
    :param box2: Pudełko zdjęte z drzewa funkcją pop
    :type box2: box3D()
    :return: Zwraca listę posortowanych interwałów      
    :rtype: list of complex     
    '''
        sign = signatures()
        spl = split()
        idx_sign = sign.get_signatures_triple(box1, box2)
        sort, in2sorted, sorted2in = sign.my_sort(idx_sign)
        tri_sign, tri_sign_i = sign.sort_signatures(box1, box2, in2sorted)
        split_sign = spl.split(tuple(sort), tri_sign, tri_sign_i)
        table = sign.ret_original_order(split_sign, sorted2in)
        return table

    @staticmethod
    def algorytm(Q, tree):
        '''
        Funkcja statyczna, w wyniku której wszystkie przecinające się
        pudełka ze stosu zostają rozbite i wstawione do drzewa 
        '''

        #obiekt klasy myInterval
        my_int = myInterval()
        #zmienna potrzebna do wprowadzania pudełka w unikalne miejsce do drzewa
        iD = 0
        #pętla działa dopóki stos nie zostanie pusty
        while not len(Q.get_stack()) == 0:
            #zdjęcie ostatniego pudełka ze stosu i przycięcie go
            q = Q.pop()
            q = my_int.box_cut(q)
            if tree.tree.count((q.interval_x.lower,  q.interval_y.lower, q.interval_z.lower, q.interval_x.upper, q.interval_y.upper,  q.interval_z.upper)) > 0:
                '''
                Sprawdzenie czy pudełko q przecina się z którymkolwiek elementem z drzewa.
                Jeśli tak, pudełko przecinające się zostaje pobrane z drzewa i usunięte,
                zaś wynik rozbicia zostaje wstawiony ponownie na stos pudełek
                '''
                i = list(tree.tree.intersection((q.interval_x.lower,  q.interval_y.lower, q.interval_z.lower, q.interval_x.upper, q.interval_y.upper,  q.interval_z.upper), objects=True))[0]
                inter = [i.object.interval_x, i.object.interval_y, i.object.interval_z]
                j = box3D(inter[0], inter[1], inter[2])
                q = my_int.box_uncut(q)
                j = my_int.box_uncut(j)
                #cofnięcie przycięcia dla pudełek które mają być rozbite
                Q.extend(algorithm().begin(q, j))
                #wprowadzenie wyniku rozbicia na stos
                tree.tree.delete(i.id, (i.bbox[0], i.bbox[1], i.bbox[2], i.bbox[3], i.bbox[4], i.bbox[5]))
                #usunięcie starego pudełka z drzewa
            else:
                tree.tree.add(iD, (q.interval_x.lower, q.interval_y.lower, q.interval_z.lower, q.interval_x.upper, q.interval_y.upper, q.interval_z.upper), q)
                #dodanie nowego pudełka do drzewa i zwiększenie zmiennej iD o 1
                iD += 1
        #kilka instrukcji wypisujących efekt działania całego programu
        lista = tree.tree.intersection(tree.tree.get_bounds(), True)
        lista = [item.bbox for item in lista]
        print('\n')
        for i in lista:
            print([i[0], i[3]], end = '') if i[0] != i[3] else print([i[0]], end = '')
            print(' x ', end = '')
            print([i[1], i[4]], end = '') if i[1] != i[4] else print([i[1]], end = '')
            print(' x ', end = '')
            print([i[2], i[5]], end = '\n') if i[2] != i[5] else print([i[2]], end = '\n')
        return tree.tree
        '''zwrócenie drzewa'''

