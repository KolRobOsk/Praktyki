from cut_box import my_closed
from boxes3D import boxStack

class wallStack(boxStack):
    '''
    Klasa przechowująca dane\n
    stosu ścian z wejścia programu
    '''

    def __init__(self):
        '''Stos ścian'''
        self.stack = []
        '''Stos "przyciętych" ścian'''
        self.stack_cut = []

    def empty(self):
        '''
        Czy pusty stos?\n
        :return: informację czy stos jest pusty\n
        :rtype: bool
        '''
        return not bool(self.get_stack())

    def get_stack(self):
        '''
        Funkcja get stosu\n
        :return: Obecny stos\n
        :rtype: boxStack
        '''
        return self.stack

    def set_stack(self, new_stack):
        '''
        Funkcja set stosu \n
        :param new_stack: aktualizowanie stanu stosu
        '''
        self.stack = new_stack

    def append(self, added):
        '''
        Funkcje append stosu\n
        :param added: element, który posłuży do rozszerzenia stosu o nowe elementy
        '''
        for box in added:

            interval_1, interval_2 = box[0], box[1]
            interval_3, interval_4 = box[1], box[2]
            interval_5, interval_6 = box[0], box[2]

            interval_1_cut, interval_2_cut = my_closed(round(box[0].lower), round(box[0].upper)), \
                                     my_closed(round(box[1].lower), round(box[1].upper))
            interval_3_cut, interval_4_cut = my_closed(round(box[1].lower), round(box[1].upper)), \
                                     my_closed(round(box[2].lower), round(box[2].upper))
            interval_5_cut, interval_6_cut = my_closed(round(box[0].lower), round(box[0].upper)), \
                                     my_closed(round(box[2].lower), round(box[2].upper))

            self.stack.append([[interval_1, interval_2], [interval_3, interval_4], [interval_5, interval_6]])
            self.stack_cut.extend([[[interval_1_cut, interval_2_cut], [interval_3_cut, interval_4_cut], [interval_5_cut, interval_6_cut]]])

    def get_stack_cut(self):
        return self.stack_cut

class Wall:
    '''
    Klasa tworząca "dwuwymiarowe" pudełka\n
    :return: ściana na podstawie podanych interwałów\n
    :rtype: Wall
    '''
    def __init__(self, interval_1, interval_2):
        self.interval_1 = interval_1
        self.interval_2 = interval_2

    def wall_from_numbers(self, x1, x2, y1, y2):
        '''
        tworzenie ściany na podstawie współrzędnych\n
        :return: ścianę pudełka na podstawie podanych granic\n
        :rtype: Wall
        '''
        if x1>=x2:
            x1, x2 = x2, x1
        if y1>=y2:
            y1, y2 = y2, y1
        Wall(my_closed(x1, x2), my_closed(y1, y2))


    def get_interval_1(self):
        '''
        Funkcje get dla jednego z interwałów\n
        :return: interwał pudełka wskazujący położenie na osi x\n
        :rtype: portion.Interval
        '''
        return self.interval_1

    def get_interval_2(self):
        '''
        Funkcje get dla jednego z interwałów\n
        :return: interwał pudełka wskazujący położenie na osi y\n
        :rtype: portion.Interval
        '''
        return self.interval_2

    def __contains__(self, num):
        '''
        Funkcja sprawdzająca czy punkt jest w pudełku\n
        :param num: tablica zawierająca 2 wartości punktu sprawdzanego - x, y\n
        :rtype: bool
        '''
        return True if (num[0] in self.interval_1) & (num[1] in self.interval_2) else False

    def __ror__(self, num):
        '''
        Funkcja sprawdzająca czy punkt jest na granicy pudełek\n
        :param num: tablica zawierająca 2 wartości punktu sprawdzanego - x, y\n
        :rtype: bool
        '''
        x, y = num[0], num[1]
        is_on_border = x in set([self.interval_1.lower, self.interval_1.upper]) or y in set([self.interval_2.lower, self.interval_2.upper])
        is_inside_box = self.__contains__(num)
        return True if is_on_border & is_inside_box else False

    def __str__(self):
        return self.interval_1 + 'x' + self.interval_2

