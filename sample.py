#przykładowy program należy wywołać wewnątrz katalogu ./Praktyki
from mainalgo import *
#import głównego modułu
table = []
#deklaracja tablicy zawierającej pudełka na wejściu do algorytmu
table.append(box3D.factory(2, 1, 8, 5, 7, 8))
table.append(box3D.factory(1, 2, 8, 3, 5, 8))
#table.append(box3D.factory(2, 3, 2, 4, 7, 7))
#tworzenie pudełek (funkcja factory ma kolejność współrzędnych x_lower y_lower z_lower x_upper, y_upper, z_upper)
#w kolejności x_lower, y_lower, z_lower, x_upper, y_upper, z_upper
print('Pudełka wejściowe:')
for box in table:
    print(box)
#wypisywanie pudełek przed wstawieniem ich do drzewa
pudelka = algorithm.execute(table)
#uruchomienie funkcji execute i rozbicie pudełek
ktore = 0
print('Pudełka wyjściowe: ')
for box in pudelka.ret_boxes():
    print('Pudełko wyjściowe {}'.format(ktore + 1))
    print(box)
    ktore += 1
