from boxes_3D import *

class tree2D(tree):
    def __init__(self):
        '''Tworzenie drzewa'''
        self.properties = rtree.index.Property()
        self.properties.dimension = 2
        self.tree = rtree.index.Index('2d_index_yz', properties=self.properties)


    def ret_boxes(self, dictionary=None):
        '''
    	Funkcja zwracająca pudełka w drzewie
    	:return: pudełka znajdujące się w drzewie
    	:rtype: list
    	'''
        try:
            boxes = self.tree.intersection(self.tree.get_bounds(), True)
            boxes = [item.object for item in boxes]
            if mylen(boxes[0].interval_z) == 0:
                boxes = [[box.interval_x, box.interval_y] for box in boxes]
            elif mylen(boxes[0].interval_x) == 0:
                boxes = [[box.interval_y, box.interval_y] for box in boxes]
            elif mylen(boxes[0].interval_y) == 0:
                boxes = [[box.interval_x, box.interval_z] for box in boxes]
            return boxes
        except:
            return []
