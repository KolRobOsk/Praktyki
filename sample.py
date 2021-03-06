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
table.extend([box3D.factory(1, 1, 3, 10, 5, 9)])
table.extend([box3D.factory(1, 1, 3, 10, 5, 9)])
#table.extend([box3D.factory(1, 1, 5, 11, 5, 6)])

#tworzenie pudełek (funkcja factory ma kolejność współrzędnych x_lower y_lower z_lower x_upper, y_upper, z_upper)
#w kolejności x_lower, y_lower, z_lower, x_upper, y_upper, z_upper
print('Pudełka wejściowe:')
for box in table.get_stack():
    print(box.interval_x, box.interval_y, box.interval_z)
print('--------------------------------')
drzewo3D, drzewo2D = tree(), tree2D()
#wypisywanie pudełek przed wstawieniem ich do drzewa
dictionary = algorithm.algorytm(table, drzewo3D, drzewo2D)
#uruchomienie funkcji execute i rozbicie pudełek
ktore = 0

for box in dictionary['b']:
    print('Obiekt {ktore}: Pudełko wyjściowe'.format(ktore=ktore + 1))
    print(box.interval_x, box.interval_y, box.interval_z)
    ktore += 1
print()

ktore = 0
for box in dictionary['wx']:
    print('Ścianka wyjściowa yz {ktore}'.format(ktore=ktore + 1))
    print(box)
    ktore += 1
print()

ktore = 0
for box in dictionary['wy']:
    print('Ścianka wyjściowa xz {ktore}'.format(ktore=ktore + 1))
    print(box)
    ktore += 1
print()

ktore = 0
for box in dictionary['wz']:
    print('Ścianka wyjściowa xy {ktore}'.format(ktore=ktore + 1))
    print(box)
    ktore += 1