import math
import cv2
import time
from pynput.keyboard import Key, Controller
from cvzone.HandTrackingModule import HandDetector

previousTime = 0

Delay_counter = 0  # Counter to track the delay
Delay_reset = 8
# Параметры вывода видеоряда
##############################
CamWidth = 640
CamHeight = 480

capture = cv2.VideoCapture(1)
capture.set(3, CamWidth)
capture.set(4, CamHeight)
##############################

# Параметры определения и отрисовки
##############################
detector = HandDetector(detectionCon=0.9, maxHands=1)
keyboard = Controller()


##############################

def fingerbutton(fin1, fin2, func, delay_counter, delay_reset):
    cv2.circle(img, lmList[fin1], 3, (0, 255, 100), 5)
    cv2.circle(img, lmList[fin2], 3, (0, 255, 100), 5)
    length = math.hypot(lmList[fin2][0] - lmList[fin1][0], lmList[fin2][1] - lmList[fin1][1])

    if length / distanceFromCamera < 0.35:
        cv2.circle(img, lmList[fin1], 3, (0, 0, 0), 5)
        cv2.circle(img, lmList[fin2], 3, (0, 0, 0), 5)
        if delay_counter == 0:
            func()
            delay_counter = delay_reset

    return delay_counter


def pressA():
    keyboard.press('a')
    keyboard.release('a')


def pressB():
    keyboard.press('b')
    keyboard.release('b')


while True:
    success, img = capture.read()
    hands, img = detector.findHands(img)

    if hands:
        lmList = hands[0]["lmList"]
        # расчет дистанции для камеры, возьму точки 17 и 0, ибо их чаще всего видно
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

        Delay_counter = fingerbutton(4, 8, pressA, Delay_counter, Delay_reset)
        Delay_counter = fingerbutton(4, 12, pressB, Delay_counter, Delay_reset)

        if Delay_counter > 0:
            Delay_counter -= 1

    # Подсчет фепесов, если поставить макс кол-во 2, то фепесы режутся в половину+, т.е 15 фпс в среднем
    currentTime = time.time()
    fps = 1 / (currentTime - previousTime)
    previousTime = currentTime
    cv2.putText(img, str(int(fps)), (10, 70), 0, 3, (255, 255, 255), 3)

    cv2.imshow("Kiss Cam", img)
    cv2.waitKey(1)
