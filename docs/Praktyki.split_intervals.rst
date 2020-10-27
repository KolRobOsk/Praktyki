.. _Praktyki.split_intervals:



Praktyki.split_intervals
===============

rola w programie
----------------
Split intervals ma 1 klasę - split, która służy to rozbijania pudełek, poprzez tworzenie nowych o wymaganych cechach oraz funkcję mylen.
W klasie znajduje się 20 funkcji rozbijających, o takiej samej anatomii.

funkcje 
------------------
nazwa(typy argumentów:argumenty)

* my_len(myInterval:interval) - funkcja, która zwraca długość interwału
* [funkcje rozbijające, nazwa:stosunek1_stosunek2_stosunek3, argumenty: box3D:box1, box3D:box2] - funkcja na początku re-deklaruje wszystkie interwały z obu pudełek, następnie tworzy pudełka i wstawia na zwracaną listę. UWAGA - niektóre pudełka zostają pominięte, gdyż interwały w stosunku half out czasem powodują, że interwał jedno lub więcej pudełek wyjściowych nie powinno istnieć według współrzędnych i program przestaje działać.	  
* split.split(list:idx_sign, list:tri_sign, list:tri_sign_i) - w tej funkcji znajduje się słownik, w którym mieszczą się odniesienia do wszystkich funkcji rozbijających, a na podstawie sygnatur funkcja wybiera, z której funkcji rozbijającej skorzystać.
