import rtree

'''
klasa przechowująca dane 
stosu pudełek z wejścia programu
'''
class boxStack:

    def __init__(self):
        #stos pudełek
        self.stack = []

    #funkcje get oraz set stosu
    def get_stack(self):
        return self.stack

    def set_stack(self, new_stack):
        self.stack = new_stack

    #funkcje append, extend oraz pop stosu
    def append(self, added):
        self.stack.append(added)

    def extend(self, added):
        self.stack.extend(added)

    def pop(self):
        return self.stack.pop()

#klasa przechowująca instrukcje drzewa
class tree:

    def __init__(self):
        # tworzenie drzewa
        self.properties = rtree.index.Property()
        # ustawienia drzewa
        self.properties.dimension = 3
        self.tree = rtree.index.Index('3d_index', properties=self.properties)

    #funkcje get oraz set drzewa
    def get_tree(self):
        return self.tree

    def set_tree(self, new_tree):
        self.tree = new_tree
