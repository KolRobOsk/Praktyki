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
table.extend([box3D.factory(2, 1, 3, 9, 5, 9)])
table.extend([box3D.factory(1, 0, 4, 9, 2, 7)])
table.extend([box3D.factory(9, 1, 5, 14, 5, 6)])

#tworzenie pudełek (funkcja factory ma kolejność współrzędnych x_lower y_lower z_lower x_upper, y_upper, z_upper)
#w kolejności x_lower, y_lower, z_lower, x_upper, y_upper, z_upper
print('Pudełka wejściowe:')
for box in table.get_stack():
    print(box.interval_x, box.interval_y, box.interval_z)
print('--------------------------------')
drzewo3D,  drzewo2D = tree(), tree2D()
#wypisywanie pudełek przed wstawieniem ich do drzewa
dictionary = algorithm.algorytm(table, drzewo3D, drzewo2D)
#uruchomienie funkcji execute i rozbicie pudełek
ktore = 0

for box in drzewo3D.ret_boxes():
    print('Obiekt {ktore}: Pudełko wyjściowe'.format(ktore=ktore + 1))
    print(box.interval_x, box.interval_y, box.interval_z)
    ktore += 1

for box in drzewo2D.ret_boxes(dictionary):
    print('Obiekt {ktore}: Ścianka wyjściowa'.format(ktore=ktore + 1))
    print(box)
    ktore += 1

