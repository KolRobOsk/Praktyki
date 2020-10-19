import rtree

class boxStack:
    '''
    Klasa przechowująca dane
    stosu pudełek z wejścia programu
    '''

    def __init__(self):
        '''Stos pudełek'''
        self.stack = []

    def get_stack(self):
        '''Funkcja get stosu'''
        return self.stack

    def set_stack(self, new_stack):
        '''Funkcja set stosu'''
        self.stack = new_stack

    def append(self, added):
        '''Funkcja append stosu'''
        self.stack.append(added)

    def extend(self, added):
        '''Funkcje extend stosu'''
        self.stack.extend(added)

    def pop(self):
        '''Funkcje pop stosu'''
        return self.stack.pop()

class tree:
    '''Klasa przechowująca instrukcje drzewa'''

    def __init__(self):
        '''Tworzenie drzewa'''
        self.properties = rtree.index.Property()
        self.properties.dimension = 3
        self.tree = rtree.index.Index('3d_index', properties=self.properties)

    def get_tree(self):
        '''Funkcje get drzewa'''
        return self.tree

    def set_tree(self, new_tree):
        '''Funkcje set drzewa'''
        self.tree = new_tree
