.. _Praktyki.mainalgo:

Praktyki.mainalgo
=================

rola w programie
----------------
Moduł służy do uruchomienia całego algorytmu. 
Usuwa pliki pozostawione po ostatnim drzewie.
Posiada jedną klasę, algorithm.

funkcje 
------------------
nazwa(typy argumentów:argumenty)

* algorithm.algorytm(BoxStack:Q, rtree:tree) - statyczna funkcja, inicjuje główną pętlę programu, sprawdza czy pudełko rozpatrywane przecina się z którymkolwiek zawartym w drzewie. Jeśli tak, usuwa jedno z przecinających się z drzewa i rozbija je z pudełkiem ze stosu i wstawia na stos.  Jeśli nie, wstawia na pudełko na drzewo i usuwa ze stosu.
* algorithm.begin(Box3D:box1, Box3D:box2) - zmienia tworzy tablicę sygnatur dla dwóch pudełek, sortuje je, według ich kolejności permutuje interwały w pudełkach. Następnie pudełka zostają rozbite, a ich interwały permutowane do pierwotnej kolejności. 


