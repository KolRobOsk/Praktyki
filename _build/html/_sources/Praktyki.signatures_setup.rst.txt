.. _Praktyki.signatures_setup:



Praktyki.signatures_setup
=================================

rola w programie
----------------
Moduł posiada klasę signatures, dzięki której możliwe jest przeprowadzanie operacji, takich jak permutacja czy sortowanie na sygnaturach. 

funkcje 
------------------
nazwa(typy argumentów:argumenty)

* signatures.io12(myInterval:interval1, myInterval:interval2) - funkcja zwraca True jeśli interwały są w stosunku out oraz drugi interwał ma wyższą wartość górną lub są w stosunku half out i drugi interwał ma większy przedział niż unia interwałów w innym przypadku zwraca False
* signatures.io21(myInterval:interval1, myInterval:interval2) - funkcja zwraca True jeśli interwały są w stosunku out oraz pierwszy interwał ma wyższą wartość górną lub są w stosunku half out i pierwszy interwał ma większy przedział niż unia interwałów, w innym przypadku zwraca False
* signatures.ii12(myInterval:interval1, myInterval:interval2) - funkcja zwraca True jeśli interwały są w stosunki in oraz drugi interwał ma większy przedział od pierwszego, w innym przypadku zwraca False
* signatures.ii21(myInterval:interval1, myInterval:interval2) - funkcja zwraca True jeśli interwały są w stosunki in oraz pierwszy interwał ma większy przedział od drugiego, w innym przypadku zwraca False
* signatures.get_signatures_triple(box3D:box1, box3D:box2) - funkcja zwraca listę sygnatur dla dwóch pudełek na wejściu, korzystając z funkcji get_signature dla każdej pary interwałów
* signatures.sort_signatures(box3D: box1, box3D: box2, list:in2sorted) - funkcja zwraca spermutowane według wzoru liste interwałów dwóch pudełek wejściowych
* signatures.permute_signatures(box_tab, sort_order) - funkcja permutuje interwały z listy
* signatures.permute(list:sortin, list:permutation) - funkcja permutuje listę (sortin) podaną na wejściu według ustalonego wzoru
* signatures.my_sort(list:inputlist) - funkcja zwraca 3 listy: listę posortowanych elementów, wzór permutacji aby dojść do kolejneści posortowanych elementów, oraz wzór permutacji aby cofnąć sortowanie
* signatures.is_in(myInterval:interval1, myInterval:interval2) - funkcja zwraca True jeśli między interwałami występuje stosunek in, w innym przypadku zwraca False
* signatures.is_out(myInterval:interval1, myInterval:interval2) - funkcja zwraca True jeśli między interwałami występuje stosunek out, w innym przypadku zwraca False
* signatures.is_equal(myInterval:interval1, myInterval:interval2) -  funkcja zwraca True jeśli między interwałami występuje stosunek equal, w innym przypadku zwraca False
* signatures.is_separate(myInterval:interval1, myInterval:interval2) - funkcja zwraca True jeśli między interwałami występuje stosunek separate, w innym przypadku zwraca False
* signatures.is_half_out(myInterval:interval1, myInterval:interval2) -  funkcja zwraca True jeśli między interwałami występuje stosunek half out, w innym przypadku zwraca False
* signatures.ie(myInterval:interval1, myInterval:interval2) - funkcja zwraca True gdy interwały mają równy przedział, w innym przypadku zwraca False
* signatures.get_signature(myInterval:interval1, myInterval:interval2) - funkcja zwraca konkretną sygnaturę dla danej pary interwałów: io12, io21, ii12, ii21, w przypadku stosunku ie zwraca ii12
* signatures.ret_original_order(list:split, list:sorted2in) - funkcja zwraca listę pudełek spermutowanych według wzoru permutacji sorted2in
