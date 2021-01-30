import math
import os, sys
sys.path.append('..')
from cut_box import *
from split_intervals import split as TEST, mylen
from portion import closed, closedopen, openclosed
#unit testy
import random as rnd
import unittest
from wall_operation import *

class algorithm_check(unittest.TestCase):

    out_interval_bigger = my_closed(2, 7)
    interval_smaller = my_closed(3, 4)
    in_interval_bigger = my_closed(2, 5)
    tst = TEST()

    def random_point_from_a_box(self, box):
        num_x = box.interval_x if mylen(box.interval_x) == 0 else rnd.randint(box.interval_x.lower, box.interval_x.upper)
        num_y = box.interval_y if mylen(box.interval_y) == 0 else rnd.randint(box.interval_y.lower, box.interval_y.upper)
        num_z = box.interval_z if mylen(box.interval_z) == 0 else rnd.randint(box.interval_z.lower, box.interval_z.upper)
        return [num_x, num_y, num_z]

    def loop_test(self, boxes_in, boxes_out):
        b = rnd.choice(boxes_in)
        x = self.random_point_from_a_box(b)
        num_in = []
        num_boundary = []
        for b in boxes_out:
            if b:
                num_in.append(b.__contains__(x))
                num_boundary.append(b.__ror__(x))
        num_in = sum(num_in)
        num_boundary = sum(num_boundary)
        if (num_in == 1) or ((num_in == num_boundary) and (num_in != 0)):
            return True
        else:
            if num_in != 1 & num_in != num_boundary:
                print('\ncontains error')
            else:
                print('\n__ror__ error')
            print('\n', b.interval_x, b.interval_y, b.interval_z, '\n', x)
            return False

    def evaluate(self, boxes_in, boxes_out, checks_num=1000):
        for i in range(checks_num):
            if self.loop_test(boxes_in, boxes_out):
                continue
            else:
                return False
        return True

    def loop_test2D(self, boxes_in, boxes_out):
        b = rnd.choice(boxes_in)
        x = self.random_point_from_a_box(b)
        num_in = []
        num_boundary = []
        for b in boxes_out:
            if b:
                num_in.append(b.__contains__(x))
                num_boundary.append(b.__ror__(x))
        num_in = sum(num_in)
        num_boundary = sum(num_boundary)
        if (num_in == 1) or ((num_in == num_boundary) and (num_in != 0)):
            return True
        else:
            if num_in != 1 & num_in != num_boundary:
                print('\ncontains error')
            else:
                print('\n__ror__ error')
            print('\n', b.interval_x, b.interval_y, b.interval_z, '\n', x)
            return False

    def evaluate2D(self, boxes_in, boxes_out, checks_num=1000):
        for i in range(checks_num):
            if self.loop_test2D(boxes_in, boxes_out):
                continue
            else:
                return False
        return True

    def test_oI_II_oI_II_oI_II(self):
        box0 = box3D(self.interval_smaller, self.interval_smaller, self.interval_smaller)
        box1 = box3D(self.out_interval_bigger, self.out_interval_bigger, self.out_interval_bigger)
        self.assertEqual(True ,self.evaluate([box0, box1], TEST().oI_II_oI_II_oI_II(box0, box1)))

    def test_oI_II_oI_II_oII_I(self):
        box0 = box3D(self.interval_smaller, self.interval_smaller, self.out_interval_bigger)
        box1 = box3D(self.out_interval_bigger, self.out_interval_bigger, self.interval_smaller)
        self.assertEqual(True , self.evaluate([box0, box1], TEST().oI_II_oI_II_oII_I(box0, box1)))
        
    def test_oI_II_oII_I_oII_I(self):
        box0 = box3D(self.interval_smaller, self.out_interval_bigger, self.out_interval_bigger)
        box1 = box3D(self.out_interval_bigger, self.interval_smaller, self.interval_smaller)
        self.assertEqual(True ,self.evaluate([box0, box1], TEST().oI_II_oII_I_oII_I(box0, box1)))
        
    def test_oII_I_oII_I_oII_I(self):
        box0 = box3D(self.out_interval_bigger, self.out_interval_bigger, self.out_interval_bigger)
        box1 = box3D(self.interval_smaller, self.interval_smaller, self.interval_smaller)
        self.assertEqual(True ,self.evaluate([box0, box1], TEST().oII_I_oII_I_oII_I(box0, box1)))
        
    def test_iI_II_iI_II_iI_II(self):
        box0 = box3D(self.interval_smaller, self.interval_smaller, self.interval_smaller)
        box1 = box3D(self.in_interval_bigger, self.in_interval_bigger, self.in_interval_bigger)
        self.assertEqual(True ,self.evaluate([box0, box1], TEST().iI_II_iI_II_iI_II(box0, box1)))

    def test_iI_II_iI_II_iII_I(self):
        box0 = box3D(self.interval_smaller, self.interval_smaller, self.in_interval_bigger)
        box1 = box3D(self.in_interval_bigger, self.in_interval_bigger, self.interval_smaller)
        self.assertEqual(True ,self.evaluate([box0, box1], TEST().iI_II_iI_II_iII_I(box0, box1)))

    def test_iI_II_iII_I_iII_I(self):
        box0 = box3D(self.interval_smaller, self.in_interval_bigger, self.in_interval_bigger)
        box1 = box3D(self.in_interval_bigger, self.interval_smaller, self.interval_smaller)
        self.assertEqual(True ,self.evaluate([box0, box1], TEST().iI_II_iII_I_iII_I(box0, box1)))

    def test_iII_I_iII_I_iII_I(self):
        box0 = box3D(self.in_interval_bigger, self.in_interval_bigger, self.in_interval_bigger)
        box1 = box3D(self.interval_smaller, self.interval_smaller, self.interval_smaller)
        self.assertEqual(True ,self.evaluate([box0, box1], TEST().iII_I_iII_I_iII_I(box0, box1)))

    def test_iI_II_iI_II_oII_I(self):
        box0 = box3D(self.interval_smaller, self.interval_smaller, self.out_interval_bigger)
        box1 = box3D(self.in_interval_bigger, self.in_interval_bigger, self.interval_smaller)
        self.assertEqual(True ,self.evaluate([box0, box1], TEST().iI_II_iI_II_oII_I(box0, box1)))
 
    def test_iII_I_oI_II_oI_II(self):
        box0 = box3D(self.in_interval_bigger, self.interval_smaller, self.interval_smaller)
        box1 = box3D(self.interval_smaller, self.out_interval_bigger, self.out_interval_bigger)
        self.assertEqual(True ,self.evaluate([box0, box1], TEST().iII_I_oI_II_oI_II(box0, box1)))

    def test_iI_II_oI_II_oI_II(self):
        box0 = box3D(self.interval_smaller, self.interval_smaller, self.interval_smaller)
        box1 = box3D(self.in_interval_bigger, self.out_interval_bigger, self.out_interval_bigger)
        self.assertEqual(True ,self.evaluate([box0, box1], TEST().iI_II_oI_II_oI_II(box0, box1)))

    def test_iI_II_oI_II_oII_I(self):
        box0 = box3D(self.interval_smaller, self.interval_smaller, self.out_interval_bigger)
        box1 = box3D(self.in_interval_bigger, self.out_interval_bigger, self.interval_smaller)
        self.assertEqual(True ,self.evaluate([box0, box1], TEST().iI_II_oI_II_oII_I(box0, box1)))


    def test_iII_I_oI_II_oII_I(self):
        box0 = box3D(self.in_interval_bigger, self.interval_smaller, self.out_interval_bigger)
        box1 = box3D(self.interval_smaller, self.out_interval_bigger, self.interval_smaller)
        self.assertEqual(True ,self.evaluate([box0, box1], TEST().iII_I_oI_II_oII_I(box0, box1)))


    def test_iII_I_oII_I_oII_I(self):
        box0 = box3D(self.in_interval_bigger, self.out_interval_bigger, self.out_interval_bigger)
        box1 = box3D(self.interval_smaller, self.interval_smaller, self.interval_smaller)
        self.assertEqual(True ,self.evaluate([box0, box1], TEST().iII_I_oII_I_oII_I(box0, box1)))

    def test_iI_II_oII_I_oII_I(self):
        box0 = box3D(self.interval_smaller, self.out_interval_bigger, self.out_interval_bigger)
        box1 = box3D(self.in_interval_bigger, self.interval_smaller, self.interval_smaller)
        self.assertEqual(True ,self.evaluate([box0, box1], TEST().iI_II_oII_I_oII_I(box0, box1)))

    def test_iI_II_iII_I_oII_I(self):
        box0 = box3D(self.interval_smaller, self.in_interval_bigger, self.interval_smaller)
        box1 = box3D(self.in_interval_bigger, self.interval_smaller, self.out_interval_bigger)
        self.assertEqual(True ,self.evaluate([box0, box1], TEST().iI_II_iII_I_oII_I(box0, box1)))
        
    def test_iI_II_iI_II_oI_II(self):
        box0 = box3D(self.interval_smaller, self.interval_smaller, self.interval_smaller)
        box1 = box3D(self.in_interval_bigger, self.in_interval_bigger, self.out_interval_bigger)
        self.assertEqual(True ,self.evaluate([box0, box1], TEST().iI_II_iI_II_oI_II(box0, box1)))

    def test_iI_II_iII_I_oI_II(self):
        box0 = box3D(self.interval_smaller, self.in_interval_bigger, self.interval_smaller)
        box1 = box3D(self.in_interval_bigger, self.interval_smaller, self.out_interval_bigger)
        self.assertEqual(True ,self.evaluate([box0, box1], TEST().iI_II_iII_I_oI_II(box0, box1)))
        
    def test_iII_I_iII_I_oI_II(self):
        box0 = box3D(self.in_interval_bigger, self.in_interval_bigger, self.interval_smaller)
        box1 = box3D(self.interval_smaller, self.interval_smaller, self.out_interval_bigger)
        self.assertEqual(True ,self.evaluate([box0, box1], TEST().iII_I_iII_I_oI_II(box0, box1)))
        
    def test_iII_I_iII_I_oII_I(self):
        box0 = box3D(self.in_interval_bigger, self.in_interval_bigger, self.out_interval_bigger)
        box1 = box3D(self.interval_smaller, self.interval_smaller, self.interval_smaller)
        self.assertEqual(True ,self.evaluate([box0, box1], TEST().iII_I_iII_I_oII_I(box0, box1)))

    #testy ścianek
    def test_iI_II_iI_II(self):
        box1 = box3D(self.interval_smaller, self.interval_smaller, 3)
        box0 = box3D(self.in_interval_bigger, self.in_interval_bigger, 3)
        res = WallOperations().iI_II_iI_II([[box0.interval_x, box0.interval_y]], [[box1.interval_x, box1.interval_y]])
        res = [box3D(r[0], r[1], 3) for r in res[0]]
        self.assertEqual(True, self.evaluate2D([box0, box1], res))

    def test_iII_I_iI_II(self):
        box1 = box3D(self.interval_smaller, self.in_interval_bigger, 3)
        box0 = box3D(self.in_interval_bigger, self.interval_smaller, 3)
        res = WallOperations().iII_I_iI_II([[box0.interval_x, box0.interval_y]], [[box1.interval_x, box1.interval_y]])
        res = [box3D(r[0], r[1], 3) for r in res[0]]
        self.assertEqual(True, self.evaluate2D([box0, box1], res))

    def test_iI_II_oI_II(self):
        box1 = box3D(self.interval_smaller, self.interval_smaller, 3)
        box0 = box3D(self.in_interval_bigger, self.out_interval_bigger, 3)
        res = WallOperations().iI_II_oI_II([[box0.interval_x, box0.interval_y]], [[box1.interval_x, box1.interval_y]])
        res = [box3D(r[0], r[1], 3) for r in res[0]]
        self.assertEqual(True, self.evaluate2D([box0, box1], res))


    def test_iI_II_oI_II(self):
        box0 = box3D(self.interval_smaller, self.interval_smaller, 3)
        box1 = box3D(self.in_interval_bigger, self.out_interval_bigger, 3)
        res = WallOperations().iI_II_oI_II([[box0.interval_x, box0.interval_y]], [[box1.interval_x, box1.interval_y]])
        res = [box3D(r[0], r[1], 3) for r in res[0]]
        self.assertEqual(True, self.evaluate2D([box0, box1], res))

    def test_iI_II_oII_I(self):
        box0 = box3D(self.interval_smaller, self.out_interval_bigger, 3)
        box1 = box3D(self.in_interval_bigger, self.interval_smaller, 3)
        res = WallOperations().iI_II_oII_I([[box0.interval_x, box0.interval_y]], [[box1.interval_x, box1.interval_y]])
        res = [box3D(r[0], r[1], 3) for r in res[0]]
        self.assertEqual(True, self.evaluate2D([box0, box1], res))

    def test_iII_I_oI_II(self):
        box0 = box3D(self.in_interval_bigger, self.interval_smaller, 3)
        box1 = box3D(self.interval_smaller, self.out_interval_bigger, 3)
        res = WallOperations().iII_I_oI_II([[box0.interval_x, box0.interval_y]], [[box1.interval_x, box1.interval_y]])
        res = [box3D(r[0], r[1], 3) for r in res[0]]
        self.assertEqual(True, self.evaluate2D([box0, box1], res))

    def test_iII_I_oII_I(self):
        box0 = box3D(self.in_interval_bigger, self.out_interval_bigger, 3)
        box1 = box3D(self.interval_smaller, self.interval_smaller, 3)
        res = WallOperations().iII_I_oII_I([[box0.interval_x, box0.interval_y]], [[box1.interval_x, box1.interval_y]])
        res = [box3D(r[0], r[1], 3) for r in res[0]]
        self.assertEqual(True, self.evaluate2D([box0, box1], res))

    def test_oI_II_oI_II(self):
        box1 = box3D(self.out_interval_bigger, self.out_interval_bigger, 3)
        box0 = box3D(self.interval_smaller, self.interval_smaller, 3)
        res = WallOperations().oI_II_oI_II([[box0.interval_x, box0.interval_y]], [[box1.interval_x, box1.interval_y]])
        res = [box3D(r[0], r[1], 3) for r in res[0]]
        self.assertEqual(True, self.evaluate2D([box0, box1], res))

    def test_oII_I_oI_II(self):
        box0 = box3D(self.out_interval_bigger, self.interval_smaller, 3)
        box1 = box3D(self.interval_smaller, self.out_interval_bigger, 3)
        res = WallOperations().oII_I_oI_II([[box0.interval_x, box0.interval_y]], [[box1.interval_x, box1.interval_y]])
        res = [box3D(r[0], r[1], 3) for r in res[0]]
        self.assertEqual(True, self.evaluate2D([box0, box1], res))


    def test_oII_I_oII_I(self):
        box1 = box3D(self.interval_smaller, self.interval_smaller, 3)
        box0 = box3D(self.out_interval_bigger, self.out_interval_bigger, 3)
        res = WallOperations().oII_I_oII_I([[box0.interval_x, box0.interval_y]], [[box1.interval_x, box1.interval_y]])
        res = [box3D(r[0], r[1], 3) for r in res[0]]
        self.assertEqual(True, self.evaluate2D([box0, box1], res))


if __name__ == '__main__':
    unittest.main()
