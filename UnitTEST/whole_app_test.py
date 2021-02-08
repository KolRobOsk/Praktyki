import os, sys
from UnitTEST.functions_test import *
sys.path.insert(0, os.path.abspath('..'))
sys.path.insert(0, os.path.abspath('.'))
from mainalgo import *
import unittest
from functions_test import *
from random import randint
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
        drzewo3D, drzewo2D = tree(), tree2D()
        diction = algorithm().algorytm(old_stack, drzewo3D, drzewo2D)
        self.assertEqual(True, algorithm_check().evaluate(table_copy, diction['b'], 10))

if __name__ == '__main__':
    unittest.main()