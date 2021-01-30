import os, sys
from UnitTEST.functions_test import *
sys.path.insert(0, os.path.abspath('..'))
sys.path.insert(0, os.path.abspath('.'))
from mainalgo import *
import unittest
from functions_test import *
from random import randint
from cut_box import *
import copy

class algorithm_test(unittest.TestCase):
    def copy_box_list(self, list):
        copy_list = []
        for i in list:
            copy_list.extend([i])
        return copy_list

    def test_funkcji_algorytm(self):
        try:
            os.remove('3d_index.idx')
            os.remove('3d_index.dat')
        except:
            pass
        table = []
        ile_pudelek = randint(2, 10)
        for j in range(ile_pudelek):
            table.append(box3D.random())
        table_copy = self.copy_box_list(table)
        old_stack = boxStack()
        old_stack.extend(table)
        drzewo = tree()
        stos = algorithm().algorytm(old_stack, drzewo)
        self.assertEqual(True, algorithm_check().evaluate(table_copy, stos.get_stack(), 10))

    def test_funkcji_2D_rozbijanie_mixed(self):
        try:
            os.remove('3d_index.idx')
            os.remove('3d_index.dat')
        except:
            pass
        W, Walls = boxStack(), boxStack()
        ile_pudelek = randint(8, 10)
        new_w = []
        drzewo3 = tree()
        new_walls = boxStack()
        for j in range(ile_pudelek):
            W.extend([box3D.random()])
        Walls.extend(self.copy_box_list(W.get_stack()))
        for i in range(len(W.get_stack())):
            new_walls.extend([W.get_stack()[i].get_wall_yz(3)])
            new_w.append(Walls.get_stack()[i].get_wall_yz(3))
        ile_pudelek = randint(8, 10)
        for j in range(ile_pudelek):
            W.extend([box3D.random()])
        for i in range(len(W.get_stack())):
            new_walls.extend([W.get_stack()[i]])
            new_w.append(W.get_stack()[i])
        stos = algorithm().algorytm(new_walls, drzewo3)
        self.assertEqual(True, algorithm_check().evaluate2D(new_w, stos.get_stack(), 1000))

if __name__ == '__main__':
    unittest.main()