# по какой-то причине в фаерфоксе через раз работают ютабовские горячие клаваиши
# в хроме такой проблемы нет
import math
import cv2
import time
from pynput.keyboard import Key, Controller
from cvzone.HandTrackingModule import HandDetector

previousTime = 0
Delay_counter = 0
Delay_reset = 10

# Параметры вывода видеоряда
##############################
CamWidth = 1280
CamHeight = 720

capture = cv2.VideoCapture(0)
capture.set(3, CamWidth)
capture.set(4, CamHeight)
##############################

# Параметры определения и отрисовки
##############################
detector = HandDetector(detectionCon=0.9, maxHands=1)
keyboard = Controller()


##############################

def fingerbutton(fin1, fin2, func, delay_counter, delay_reset):
    sensitivity = 0.3
    # cv2.circle(img, lmList[fin1], 3, (0, 255, 100), 5)
    # cv2.circle(img, lmList[fin2], 3, (0, 255, 100), 5)
    length = math.hypot(lmList[fin2][0] - lmList[fin1][0], lmList[fin2][1] - lmList[fin1][1])

    if length / distanceFromCamera < sensitivity:
        cv2.circle(img, lmList[fin1], 3, (0, 0, 0), 5)
        cv2.circle(img, lmList[fin2], 3, (0, 0, 0), 5)
        if delay_counter == 0:
            func()
            delay_counter = delay_reset

    return delay_counter


##############################
def pressA():
    keyboard.press('a')
    keyboard.release('a')


def pressB():
    keyboard.press('b')
    keyboard.release('b')


def pressO():
    keyboard.press('o')
    keyboard.release('o')


# Горячие клавиши в видосах на ютубе
##############################
def FullScreen():
    keyboard.press('f')
    keyboard.release('f')


def PlayPause():
    keyboard.press(Key.space)
    keyboard.release(Key.space)


def Backward():
    keyboard.press('j')
    keyboard.release('j')


def Forward():
    keyboard.press('l')
    keyboard.release('l')


def VolUp():
    keyboard.press(Key.up)
    keyboard.release(Key.up)


def VolDown():
    keyboard.press(Key.down)
    keyboard.release(Key.down)


def EmptyFunc():
    print("")
    # todo можно определить область срабатывания чтобы исключить случайные нажатия
    # типа квадрата по центру

    # todo придумать как регулировать громкость
    # вроде сделал, но точность традает


while True:
    success, img = capture.read()
    hands, img = detector.findHands(img)

    if hands:
        lmList = hands[0]["lmList"]
        # расчет дистанции для камеры, возьму точки 17(под мизинцем) и 0(основание кисти), ибо их чаще всего видно
        #######################################################
        pnt1 = 0
        pnt2 = 17
        x1, y1 = lmList[pnt1]
        x2, y2 = lmList[pnt2]
        cv2.circle(img, lmList[pnt1], 3, (255, 255, 100), 5)
        cv2.circle(img, lmList[pnt2], 3, (255, 100, 255), 5)
        cv2.putText(img, str(x1), (10, 100), 0, 1, (255, 255, 100), 3)
        cv2.putText(img, str(x2), (10, 150), 0, 1, (255, 100, 255), 3)
        distanceFromCamera = int(math.sqrt((y2 - y1) ** 2 + (x2 - x1) ** 2))
        #######################################################

        # Delay_counter = fingerbutton(4, 8, pressA, Delay_counter, Delay_reset)
        # Delay_counter = fingerbutton(4, 12, pressB, Delay_counter, Delay_reset)
        # Delay_counter = fingerbutton(4, 16, pressO, Delay_counter, Delay_reset)

        Delay_counter = fingerbutton(4, 8, PlayPause, Delay_counter, Delay_reset)
        Delay_counter = fingerbutton(4, 12, Forward, Delay_counter, Delay_reset)
        Delay_counter = fingerbutton(4, 16, Backward, Delay_counter, Delay_reset)
        Delay_counter = fingerbutton(4, 20, FullScreen, Delay_counter, Delay_reset)
        Delay_counter = fingerbutton(1, 12, VolUp, Delay_counter, Delay_reset)
        Delay_counter = fingerbutton(1, 16, VolDown, Delay_counter, Delay_reset)

        if Delay_counter > 0:
            Delay_counter -= 1

    # Подсчет фепесов, если поставить макс кол-во рук =  2, то фпс режутся в половину+, т.е 15 фпс в среднем
    # сторонняя камера просто не может в 30 жаль
    currentTime = time.time()
    fps = 1 / (currentTime - previousTime)
    previousTime = currentTime
    cv2.putText(img, str(int(fps)), (10, 70), 0, 3, (255, 255, 255), 3)

    cv2.imshow("Kiss Cam", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break