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
        table = []
        ile_pudelek = randint(2, 10)
        for j in range(ile_pudelek):
            table.append(box3D.random())
        table_copy = self.copy_box_list(table)
        old_stack = boxStack()
        old_stack.extend(table)
        drzewo = tree()
        algorithm().algorytm(old_stack, drzewo)
        self.assertEqual(True, algorithm_check().evaluate(table_copy, drzewo.ret_boxes(), 10))

    def test_funkcji_2D_rozbijanie_xy(self):
        W, Walls = boxStack(), boxStack()
        ile_pudelek = randint(8, 10)
        new_w = []
        new_walls = []
        for j in range(ile_pudelek):
            W.extend([box3D.random()])
        Walls.extend(self.copy_box_list(W.get_stack()))
        operations = WallOperations()
        for i in range(len(W.get_stack())):
            new_walls.append(W.get_stack()[i].get_wall_xy())
            new_w.append(Walls.get_stack()[i].get_wall_xy())
        walls_p = operations.split_boxes(new_walls)
        self.assertEqual(True, algorithm_check().evaluate2D(new_w, walls_p.get_stack(), 1000))



if __name__ == '__main__':
    unittest.main()



