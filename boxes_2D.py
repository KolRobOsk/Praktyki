from boxes_3D import *
from cut_box_2D import *

class tree2D(tree):
    def __init__(self):
        '''Tworzenie drzewa'''
        self.properties = rtree.index.Property()
        self.properties.dimension = 2
        self.tree = rtree.index.Index('2d_index', properties=self.properties)


    def ret_boxes(self, dictionary=None):
        '''
    	Funkcja zwracająca pudełka w drzewie
    	:return: pudełka znajdujące się w drzewie
    	:rtype: list
    	'''

        boxes = [box.object for box in list(self.tree.intersection(self.tree.get_bounds(), True))]
        i, j, w_cut, boxes_res = 0, 0, WallCut(), []
        while len(boxes) > 0:
            for wall in ['wx', 'wy', 'wz']:
                if boxes[i] == dictionary[wall][j].iD:
                    i += 1
                    print(w_cut.wall_uncut(dictionary[wall][j]))
                    boxes.pop(i)
                    boxes_res.append(w_cut.wall_uncut(dictionary[wall][j]))
                    j = 0
            j += 1
        return boxes_res
        