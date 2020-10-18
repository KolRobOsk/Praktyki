from split import *
class signatures:

    #funkcje sprawdzające, jaką sygnaturę nadać danej parze interwałów
    def io12(self, interval1, interval2):
        len1, len2 = (mylen(interval1), mylen(interval2))
        difference = len2 - len1 if len1 > 0 else len1 + len2
        if ((interval1.upper < interval2.upper) & (self.is_out(interval1, interval2)))| (self.is_half_out(interval1, interval2) & (difference > 0)):
            return True
        else:
            return False

    def ii12(self, interval1, interval2):
        return True if (self.is_in(interval1, interval2) & (interval1.upper < interval2.upper)) else False

    def io21(self, interval1, interval2):
        len1, len2 = (mylen(interval1), mylen(interval2))
        difference = len1 - len2 if len2 > 0 else len1 + len2
        if (interval2.upper < interval1.upper) & (self.is_out(interval1, interval2)) | (self.is_half_out(interval1, interval2) & (difference > 0)):
            return True
        else:
            return False

    def ii21(self, interval1, interval2):
        return True if (self.is_in(interval1, interval2) & (interval1.upper > interval2.upper)) else False

    #funkcja zwracająca tablicę z trzema sygnaturami interwałów
    def get_signatures_triple(self, box1, box2):
        x1, y1, z1, x2, y2, z2 = box1.interval_x, box1.interval_y, box1.interval_z, box2.interval_x, box2.interval_y, box2.interval_z
        signatures = [self.get_signature(x1, x2), self.get_signature(y1, y2), self.get_signature(z1, z2)]
        return signatures

    #funkcja przygotowująca pudełka do posortowania interwałów
    def sort_signatures(self, box1, box2, in2sorted):
        box_tab1 = [box1.interval_x, box1.interval_y, box1.interval_z]
        box_tab2 = [box2.interval_x, box2.interval_y, box2.interval_z]
        tri_sign, tri_sign_i = self.permute_signatures(box_tab1, in2sorted), self.permute_signatures(box_tab2, in2sorted)
        return tri_sign, tri_sign_i

    #funkcja permutująca interwały z tablicy
    def permute_signatures(self, box_tab, sort_order):
        box_tab = self.permute(box_tab, sort_order)
        return box_tab

    #funkcja przeprowadzająca operację permutacji
    def permute(self, sortin, permutation):
        assert len(sortin) == len(permutation)
        return [sortin[i] for i in permutation]

    #funkcja sortująca sygnatury interwałów
    def my_sort(self, inputlist):
        inputlist = zip(inputlist, range(len(inputlist)))
        aux = sorted(inputlist, key=lambda x: x[0])
        sorted2in = [aux[i][1] for i in range(len(aux))]
        list2 = zip(sorted2in, range(len(sorted2in)))
        aux1 = sorted(list2, key=lambda x: x[0])
        in2sorted = [aux1[i][1] for i in range(len(aux1))]
        sort = [aux[i][0] for i in range(len(aux))]
        return sort, in2sorted, sorted2in

    '''
    funkcje sprawdzające czy interwały 
    są w danym stosunku do siebie
    '''
    def is_in(self, interval1, interval2):
        union = interval1 & interval2
        return True if ((union.lower == interval1.lower and union.upper == interval1.upper) ^ (union.lower == interval2.lower and union.upper == interval2.upper)) else False


    def is_equal(self, interval1, interval2):
        return True if interval1 == interval2 else False


    def is_out(self, interval1, interval2):
        return True if (interval1.lower != interval2.lower) and (interval2.upper != interval1.upper) and (interval1 & interval2) else False


    def is_separate(self, int1, int2):
        intersect = int1 & int2
        return True if mylen(intersect) == 0 else False

    def is_half_out(self, int1, int2):
        return True if (int1.lower == int2.lower) ^ (int2.upper == int1.upper) else False

    def ie(self, interval1, interval2):
        return True if self.is_equal(interval1, interval2) else False

    #funkcja nadająca sygnatury parom interwałów
    def get_signature(self, interval1, interval2):
        if self.ii12(interval1, interval2):
            return 'ii12'
        if self.ii21(interval1, interval2):
            return 'ii21'
        if self.io12(interval1, interval2):
            return 'io12'
        if self.io21(interval1, interval2):
            return 'io21'
        if self.ie(interval1, interval2):
            return 'ii12'

    #funkcja przywracająca oryginalny porządek interwałów
    def ret_original_order(self, split, sorted2in):
        table = []
        for i in split:
            j = [i.interval_x, i.interval_y, i.interval_z]
            perm = self.permute_signatures(j, sorted2in)
            table.append(box3D(perm[0], perm[1], perm[2]))
        return table
