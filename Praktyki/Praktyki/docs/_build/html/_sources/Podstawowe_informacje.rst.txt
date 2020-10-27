.. _Podstawowe_informacje:

Podstawowe informacje
=====================

Licencja
--------
Program jest udostępniany na licencji GNU General Public License
https://www.gnu.org/licenses/licenses.pl.html 

Założenia działania programu
----------------------------
Program bierze dowolną liczbę pudełek które mogą się przecinać i zwraca pudełka nie przecinające się mające jako unię unię pudełek na wejściu

Przecinanie - pudełka przecinają się jeżeli tworzące je interwały mają niepustą cześć wspólną dla osi x, y i z.

Rozbicie - jeśli dwa pudełka się przecinają, zostaje zwrócona niekoniecznie
taka sama ilość pudełek, które unię mają równą pudełkom przecinającym się,
lecz się nie przecinają. 

Układ współrzędnych kartezjańskich
----------------------------------
Jest to układ współrzędnych oparty na trzech płaszczyznach: x, y oraz z.
Więcej informacji 
https://en.wikipedia.org/wiki/Cartesian_coordinate_system

interwały
---------
Interwał to odcinek o dwóch atrybutach granicznych.

pudełka
-------
Pudełka to obiekty przedstawione przez 3 interwały, 
po jednym na każdą z płaszczyzn. Można je sobie wyobrazić
jako zwykłe prostopadłościany.

drzewo
------
Drzewo korzystające z 3-wymiarowych węzłów.

