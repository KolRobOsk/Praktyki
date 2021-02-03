#przykładowy program należy wywołać wewnątrz katalogu ./Praktyki
from mainalgo import *
#import głównego modułu
table = boxStack()
try:
    os.remove('3d_index.idx')
    os.remove('3d_index.dat')
    os.remove('2d_index.idx')
    os.remove('2d_index.dat')
except:
    pass

#deklaracja tablicy zawierającej pudełka na wejściu do algorytmu
table.extend([box3D.factory(1, 1, 3, 7, 9, 3)])
table.extend([box3D.factory(1, 1, 3, 7, 8, 3)])

#tworzenie pudełek (funkcja factory ma kolejność współrzędnych x_lower y_lower z_lower x_upper, y_upper, z_upper)
#w kolejności x_lower, y_lower, z_lower, x_upper, y_upper, z_upper
print('Pudełka wejściowe:')
for box in table.get_stack():
    print(box.interval_x, box.interval_y, box.interval_z)
drzewo3D,  drzewo2D_xy,  drzewo2D_yz,  drzewo2D_xz = tree(), tree2D_xy(), tree2D_yz(), tree2D_xz()
#wypisywanie pudełek przed wstawieniem ich do drzewa
algorithm.algorytm(table, drzewo3D, drzewo2D_xy,  drzewo2D_yz,  drzewo2D_xz)
#uruchomienie funkcji execute i rozbicie pudełek
ktore = 0

'''
for box in drzewo3D.ret_boxes():
    print('Pudełko wyjściowe {}'.format(ktore + 1))
    print(box.interval_x, box.interval_y, box.interval_z)
    ktore += 1
'''

for box in drzewo2D_xy.ret_boxes():
    print('Ścianka wyjściowa {}'.format(ktore + 1))
    print(box.interval_x, box.interval_y, box.interval_z)
    ktore += 1

'''
for box in drzewo2D_yz.ret_boxes2D():
    print('Ścianka wyjściowa {}'.format(ktore + 1))
    print(box)
    ktore += 1

for box in drzewo2D_xz.ret_boxes2D():
    print('Ścianka wyjściowa {}'.format(ktore + 1))
    print(box)
    ktore += 1

'''
