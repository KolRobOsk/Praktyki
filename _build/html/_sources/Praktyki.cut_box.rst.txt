.. _Praktyki.cut_box:



Praktyki.cut_box
================

rola w programie
----------------
Moduł składa się z 2 klas: Box3D oraz myInterval oraz funkcji my_closed.
Przy pomocy klasy Box3D tworzone są pudełka. Klasa myInterval dziedziczy
z klasy Portion.Interval. Jej zadaniem jest przycinanie (odejmowanie bardzo 
małych liczb, czyli epsilonów od granicy interwałów) pudełek, aby program nie rozpoznawał
pudełek jako przecinające się gdy tylko stykają się ze sobą.
my_closed to funkcja tworząca interwał, który potem będzie można przyciąć.

funkcje 
------------------
nazwa(typy argumentów:argumenty)

* my_closed(lower, upper) - funkcja tworząca interwał z atrybutami lower - dolna granica, upper - górna granica

* box3D.get_interval_x() - funkcja zwracająca interwał pudełka na płaszczyźnie x
* box3D.get_interval_y() - funkcja zwracająca interwał pudełka na płaszczyźnie y
* box3D.get_interval_z() - funkcja zwracająca interwał pudełka na płaszczyźnie z
* box3D.__contains__(list:num) - funkcja, która sprawdza czy punkt jest wewnątrz pudełka
* box3D.__ror__(list:num) - funkcja, która sprawdza czy punkt jest na granicy pudełek
* box3D.factory(complex:x1, complex:y1, complex:z1, complex:x2, complex:y2, complex:z2) - tworzy pudełko na bazie podanych wartości granicznych poszczególnych interwałów (x1 to dolna granica interwału x, zaś y2 to górna granica interwału y)

* myInterval.upper_eps() - atrybut o wartości górnej interwału przypisanego do obiektu + eps (epsilon, bardzo mała liczba) 
* myInterval.upper_meps() - atrybut o wartości górnej interwału przypisanego do obiektu - eps (epsilon, bardzo mała liczba)
* myInterval.lower_eps() - atrybut o wartości dolnej interwału przypisanego do obiektu + eps (epsilon, bardzo mała liczba)	
* myInterval.lower_meps() - atrybut o wartości dolnej interwału przypisanego do obiektu - eps (epsilon, bardzo mała liczba)
* myInterval.get_upper_eps() - funkcja zwracająca atrybut upper_eps
* myInterval.get_upper_meps() -funkcja zwracająca atrybut upper_meps
* myInterval.get_lower_eps() - funkcja zwracająca atrybut lower_eps
* myInterval.get_lower_meps() - funkcja zwracająca atrybut lower_eps
* myInterval.upper_eps() - funkcja ustawiająca atrybut upper_eps na podstawie atrybutu upper + eps
* myInterval.upper_meps() - funkcja ustawiająca atrybut upper_eps na podstawie atrybutu upper + eps
* myInterval.lower_eps() -  funkcja ustawiająca atrybut upper_eps na podstawie atrybutu lower + meps
* myInterval.lower_meps() -funkcja ustawiająca atrybut upper_eps na podstawie atrybutu lower + meps
* myInterval.box_cut(box3D: box1) - funkcja przycina pudełko tj. uruchamia dla każdego interwału (x, y, z) funkcję box_cut_execute
* myInterval.box_uncut(box3D: box2) - funkcja cofa działanie funkcji box_cut dla każdego interwału (x, y, z) przy pomocy funkcji box_uncut_execute
* myInterval.box_cut_execute(myInterval:interval) - funkcja zwraca dla podanego interwału interwał o wartościach granicznych lower + eps, upper - eps
* myInterval.box_uncut_execute(myInterval:interval) - funkcja zwraca dla podanego interwału interwał o wartościach granicznych lower - eps, upper + eps
