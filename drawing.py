import pygame

pygame.font.init()
my_font = pygame.font.SysFont('calibri', 30)
second_font = pygame.font.SysFont('calibri', 40)


def draw_conductor(screen, x1, y1, x2, y2):
    """
    Отрисовка перемычки
    :param x1: х-координата первого узла элемента
    :param y1: y-координата первого узла элемента
    :param x2: х-координата второго узла элемента
    :param y2: y-координата второго узла элемента

    """
    # пересчет координат основных узлов в координаты на экране
    X = 600 + x1 * 90
    Y = 120 + y1 * 90
    XX = 600 + x2 * 90
    YY = 120 + y2 * 90
    # отрисовка линии - перемычки
    pygame.draw.line(screen, (255, 255, 255), (X, Y), (XX, YY), 5)

def draw_resist(screen, x1, y1, x2, y2):
    """
     Отрисовка резистора
     :param x1: х-координата первого узла элемента
     :param y1: y-координата первого узла элемента
     :param x2: х-координата второго узла элемента
     :param y2: y-координата второго узла элемента

     """
    # пересчет координат основных узлов в координаты на экране
    X = 600 + x1 * 90
    Y = 120 + y1 * 90
    XX = 600 + x2 * 90
    YY = 120 + y2 * 90
    # соответственно Х и У координаты точек А и В
    # где А и В - точки крепления "проводов резистора" к его "корпусу"
    XA = (XX + 2 * X) / 3
    YA = (YY + 2 * Y) / 3
    XB = (2 * XX + X) / 3
    YB = (2 * YY + Y) / 3
    # далее идет расчет координат вершин прямоугольника по которым будет отрисовываться резистор
    # W1, W2 - две вершины, которые ближе всего к первому основному узлу (и к точке А)
    # Z1, Z2 - две вершины, которые ближе всего ко второму основному узлу (и к точке В)
    if Y == YY:
        # горизонтальное положение резистора
        WY1 = YA - abs(XX - X) / 9
        WX1 = XA
        WY2 = YA + abs(XX - X) / 9
        WX2 = XA
        ZY1 = YB - abs(XX - X) / 9
        ZX1 = XB
        ZY2 = YB + abs(XX - X) / 9
        ZX2 = XB
    else:
        # вертикальное положение резистора
        WY1 = YA
        WX1 = XA - abs(YY - Y) / 9
        WY2 = YA
        WX2 = XA + abs(YY - Y) / 9
        ZY1 = YB
        ZX1 = XB - abs(YY - Y) / 9
        ZY2 = YB
        ZX2 = XB + abs(YY - Y) / 9
    # отрисовка линий, соединяющих вершины прямоугольника и "ножки" резистора
    pygame.draw.line(screen, (0, 255, 255), (X, Y), (XA, YA), 5)
    pygame.draw.line(screen, (0, 255, 255), (XB, YB), (XX, YY), 5)
    pygame.draw.line(screen, (0, 255, 255), (WX1, WY1), (WX2, WY2), 5)
    pygame.draw.line(screen, (0, 255, 255), (WX1, WY1), (ZX1, ZY1), 5)
    pygame.draw.line(screen, (0, 255, 255), (ZX1, ZY1), (ZX2, ZY2), 5)
    pygame.draw.line(screen, (0, 255, 255), (WX2, WY2), (ZX2, ZY2), 5)


def draw_blackbox(screen, x1, y1, x2, y2):
    """
     Отрисовка черного ящика
     :param x1: х-координата первого узла элемента
     :param y1: y-координата первого узла элемента
     :param x2: х-координата второго узла элемента
     :param y2: y-координата второго узла элемента

     """
    # пересчет координат основных узлов в координаты на экране
    X = 600 + x1 * 90
    Y = 120 + y1 * 90
    XX = 600 + x2 * 90
    YY = 120 + y2 * 90
    # соответственно Х и У координаты точек А и В
    # где А и В - точки крепления "проводов ЧЯ" к его "корпусу"
    XA = (XX + 2 * X) / 3
    YA = (YY + 2 * Y) / 3
    XB = (2 * XX + X) / 3
    YB = (2 * YY + Y) / 3
    # далее идет расчет координат вершин прямоугольника по которым будет отрисовываться ЧЯ
    # W1, W2 - две вершины, которые ближе всего к первому основному узлу (и к точке А)
    # Z1, Z2 - две вершины, которые ближе всего ко второму основному узлу (и к точке В)
    if Y == YY:
        # горизонтальное положение ЧЯ
        WY1 = YA - abs(XX - X) / 6
        WX1 = XA
        WY2 = YA + abs(XX - X) / 6
        WX2 = XA
        ZY1 = YB - abs(XX - X) / 6
        ZX1 = XB
        ZY2 = YB + abs(XX - X) / 6
        ZX2 = XB
    else:
        # вертикальное положение ЧЯ
        WY1 = YA
        WX1 = XA - abs(YY - Y) / 6
        WY2 = YA
        WX2 = XA + abs(YY - Y) / 6
        ZY1 = YB
        ZX1 = XB - abs(YY - Y) / 6
        ZY2 = YB
        ZX2 = XB + abs(YY - Y) / 6
    # отрисовка линий, соединяющих вершины прямоугольника (коропуса ЧЯ) и "ножки" ЧЯ
    pygame.draw.line(screen, (148, 0, 211), (X, Y), (XA, YA), 5)
    pygame.draw.line(screen, (148, 0, 211), (XB, YB), (XX, YY), 5)
    pygame.draw.line(screen, (148, 0, 211), (WX1, WY1), (WX2, WY2), 5)
    pygame.draw.line(screen, (148, 0, 211), (WX1, WY1), (ZX1, ZY1), 5)
    pygame.draw.line(screen, (148, 0, 211), (ZX1, ZY1), (ZX2, ZY2), 5)
    pygame.draw.line(screen, (148, 0, 211), (WX2, WY2), (ZX2, ZY2), 5)


def draw_battery(screen, x1, y1, x2, y2):
    """
    Отрисовка источника ЭДС
    :param x1: х-координата первого узла элемента
    :param y1: y-координата первого узла элемента
    :param x2: х-координата второго узла элемента
    :param y2: y-координата второго узла элемента

    """
    # пересчет координат основных узлов в координаты на экране
    X = 600 + x1 * 90
    Y = 120 + y1 * 90
    XX = 600 + x2 * 90
    YY = 120 + y2 * 90
    # соответственно Х и У координаты точек А и В
    # где А и В - точки крепления "проводов источника" к его "пластинам"
    XA = (4 * XX + 5 * X) / 9
    YA = (4 * YY + 5 * Y) / 9
    XB = (5 * XX + 4 * X) / 9
    YB = (5 * YY + 4 * Y) / 9
    # далее идет расчет координат вершин "пластин" по которым будет отрисовываться источник
    # W1, W2 - две вершины, которые ближе всего к первому основному узлу (и к точке А)
    # Z1, Z2 - две вершины, которые ближе всего ко второму основному узлу (и к точке В)
    if Y == YY:
        # горизонтальное положение источника
        WY1 = YA - abs(XX - X) / 9
        WX1 = XA
        WY2 = YA + abs(XX - X) / 9
        WX2 = XA
        ZY1 = YB - abs(XX - X) / 4
        ZX1 = XB
        ZY2 = YB + abs(XX - X) / 4
        ZX2 = XB
    else:
        # вертикальное положение источника
        WY1 = YA
        WX1 = XA - abs(YY - Y) / 9
        WY2 = YA
        WX2 = XA + abs(YY - Y) / 9
        ZY1 = YB
        ZX1 = XB - abs(YY - Y) / 4
        ZY2 = YB
        ZX2 = XB + abs(YY - Y) / 4
    # отрисовка линий - "пластин" осточника и его проводов
    pygame.draw.line(screen, (255, 242, 0), (X, Y), (XA, YA), 5)
    pygame.draw.line(screen, (255, 242, 0), (XB, YB), (XX, YY), 5)
    pygame.draw.line(screen, (255, 242, 0), (WX1, WY1), (WX2, WY2), 5)
    pygame.draw.line(screen, (255, 242, 0), (ZX1, ZY1), (ZX2, ZY2), 5)


def draw_description(screen):
    # вывод памятки на экран
    surf = my_font.render("Описание:", True, (255, 111, 255))
    screen.blit(surf, (50, 270))
    surf = my_font.render("Кнопка 1 / перемычки / ", True, (255, 255, 255))
    screen.blit(surf, (50, 300))
    surf = my_font.render("Кнопка 2 / резисторы / 2 Ом", True, (0, 255, 255))
    screen.blit(surf, (50, 330))
    surf = my_font.render("Кнопка 3 / источники / ", True, (255, 242, 0))
    screen.blit(surf, (50, 360))
    surf = my_font.render("Кнопка 4 / черный ящик / ???", True, (148, 0, 211))
    screen.blit(surf, (50, 390))
    surf = my_font.render("Кнопка 0 / сброс схемы / =(", True, (124, 255, 0))
    screen.blit(surf, (50, 420))
    surf = my_font.render("Пробел   / обсчет схемы / =)", True, (255, 111, 255))
    screen.blit(surf, (50, 450))


def draw_voltmeter(screen, volts=0):
    # отрисовка экрана вольтметра, с отображением значения переменной, отвечающей за напряжение между выделенными узлами
    pygame.draw.rect(screen, (0, 0, 0), (200, 130, 200, 110), 0)
    pygame.draw.rect(screen, (255, 0, 0), (200, 130, 200, 110), 5)
    surf = my_font.render("Voltage A-B", True, (255, 0, 0))
    screen.blit(surf, (230, 200))
    surf = second_font.render(str(volts) + " [V]", True, (255, 0, 0))
    screen.blit(surf, (250, 160))


def update_nodes(screen):
    """
    сбрасывание предыдущей схемы и отрисовка узлов новой схемы размером также 5х5

    """

    pygame.draw.rect(screen, (0, 0, 0), (560, 0, 500, 600), 0)
    surf = second_font.render("Нормально делай - нормально будет. (с) Карл Гаусс", True, (255, 255, 255))
    screen.blit(surf, (65, 20))
    for i in range(5):
        for j in range(5):
            pygame.draw.circle(screen, (255, 255, 255), (600 + i * 90, 90 * j + 120), 5, 0)
