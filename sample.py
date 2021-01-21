#przykładowy program należy wywołać wewnątrz katalogu ./Praktyki
from mainalgo import *
#import głównego modułu
table = []
#deklaracja tablicy zawierającej pudełka na wejściu do algorytmu
table.append(box3D.factory(2, 1, 4, 5, 7, 8))
table.append(box3D.factory(1, 2, 3, 3, 5, 7))
table.append(box3D.factory(2, 3, 2, 4, 7, 7))
#tworzenie pudełek (funkcja factory ma kolejność współrzędnych x_lower y_lower z_lower x_upper, y_upper, z_upper)
#w kolejności x_lower, y_lower, z_lower, x_upper, y_upper, z_upper
print('Pudełka wejściowe:')
for box in table:
    print(box)
#wypisywanie pudełek przed wstawieniem ich do drzewa
pudelka, stos_scian = algorithm.execute(table)
#uruchomienie funkcji execute i rozbicie pudełek
ktore = 0
stos = stos_scian.get_stack_cut()
print('Pudełka wyjściowe: ')
for box in pudelka:
    print('Pudełko wyjściowe {}'.format(ktore + 1))
    print(box)
    print('    ściana xy        ściana yz,      ściana xz')
    print(stos[ktore])
    print()
    #wypisanie pudełek na wyjściu programu
    ktore += 1
