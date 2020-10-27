.. _Praktyki.boxes3D:

Praktyki.boxes3D
=============

rola w programie 
----------------
Moduł posiada 2 klasy:
* Tree - drzewo przechowujące pudełka po zakończeniu działania programu.
* BoxStack - stos pudełek przechowujący pudełka nie wprowadzone jeszcze do drzewa.

funkcje
-------
nazwa(typy argumentów:argumenty)

* Tree.get_tree() - funkcja zwracająca drzewo dla obiektu rtree
* Tree.set_tree(rtree:new_tree) - funkcja ustawiająca nową postać drzewa

* BoxStack.get_stack() - zwraca stos dla obiektu BoxStack
* BoxStack.set_stack(BoxStack:new_stack) - ustawia nową postać stosu
* BoxStack.append(Box3D:added) - dodaje element do stosu pudełek (wstawiając cały obiekt added na koniec)
* BoxStack.extend(list:added) - rozszerza stos pudełek (wstawiając wszystkie elementy Box3D z listy na koniec stosu)
* BoxStack.pop() - usuwa ostatni element stosu pudełek


