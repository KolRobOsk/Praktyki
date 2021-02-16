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
        if sum([len(dictionary['wx']) == 0, len(dictionary['wy']) == 0, len(dictionary['wz']) == 0]) < 3:
            boxes = self.tree.intersection(self.tree.bounds, True)
            boxes = [item.object for item in boxes]
            j, w_cut, boxes_res = 0, WallCut(), []
            while len(boxes) > 0:
                for wall in ['wx', 'wy', 'wz']:
                    if len(dictionary[wall]) > j:
                        if boxes[0].iD == dictionary[wall][j].iD:
                            boxes_res.append(w_cut.wall_uncut(dictionary[wall][j]))
                            boxes.pop(0)
                            j = 0
                    else:
                        continue
                j += 1
            return boxes_res
        else:
            return []