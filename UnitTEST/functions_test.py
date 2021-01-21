import math
import os, sys
sys.path.append('..')
from split_intervals import split 
import portion
from cut_box import *
from signatures_setup import split as TEST
from portion import closed, closedopen, openclosed
#unit testy
import random as rnd
import unittest

class algorithm_check(unittest.TestCase):

    out_interval_bigger = closed(3, 6)
    interval_smaller = closed(2, 5)
    in_interval_bigger = closed(1, 6)
    tst = TEST()

    def random_point_from_a_box(self, box):
        num_x = rnd.randint(box.interval_x.lower, box.interval_x.upper)
        num_y = rnd.randint(box.interval_y.lower, box.interval_y.upper)
        num_z = rnd.randint(box.interval_z.lower, box.interval_z.upper)
        return [num_x, num_y, num_z]

    def loop_test(self, boxes_in, boxes_out):
        b = rnd.choice(boxes_in)
        x = self.random_point_from_a_box(b)
        num_in = sum([b.__contains__(x) for b in boxes_out])
        num_boundary = sum([b.__ror__(x) for b in boxes_out])
        if (num_in == 1) or ((num_in == num_boundary) and (num_in != 0)):
            return True
        else:
            if num_in != 1 & num_in != num_boundary:
                print('\ncontains error')
            else:
                print('\n__ror__ error')
            print('\n', b.interval_x, b.interval_y, b.interval_z, '\n', x)
            return False

    def evaluate(self, boxes_in, boxes_out, checks_num = 1000):
        for i in range(checks_num):
            if self.loop_test(boxes_in, boxes_out):
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



if __name__ == '__main__':
    unittest.main()
