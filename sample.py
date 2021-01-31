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
table.extend([box3D.factory(2, 1, 8, 5, 7, 8, 6)])
table.extend([box3D.factory(1, 1, 8, 4, 6, 8, 3)])
table.extend([box3D.factory(6, 1, 7, 9, 7, 7, 8)])
table.extend([box3D.factory(6, 1, 5, 9, 7, 7, 8)])
#tworzenie pudełek (funkcja factory ma kolejność współrzędnych x_lower y_lower z_lower x_upper, y_upper, z_upper)
#w kolejności x_lower, y_lower, z_lower, x_upper, y_upper, z_upper
print('Pudełka wejściowe:')
for box in table.get_stack():
    print(box)
drzewo3D, drzewo2D = tree(), tree2D()
#wypisywanie pudełek przed wstawieniem ich do drzewa
algorithm.algorytm(table, drzewo3D, drzewo2D)
#uruchomienie funkcji execute i rozbicie pudełek
ktore = 0

for box in drzewo3D.ret_boxes():
    print('Pudełka wyjściowe {}'.format(ktore + 1))
    print(box)
    ktore += 1

for box in drzewo2D.ret_boxes():
    print('Ścianki wyjściowe {}'.format(ktore + 1))
    print(box)
    ktore += 1

