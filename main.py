import os
from time import sleep
import cv2
import numpy as np
from PIL import Image
from ppadb.client import Client as AdbClient
from Tester import ocr as oc
from Solution import SudokuSolution
import copy

client = AdbClient(host="127.0.0.1", port=5037)
devices = client.devices()

if len(devices) == 0:
    print("No Devices")
    quit()

myDevice = devices[0]


def readNumber(ar):
    box = (40, 25, 110, 125)
    img = Image.fromarray(ar).convert('RGB')
    img = img.crop(box)
    i = np.array(img)
    im = toCV2(i)
    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 100, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY)[1]
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    return oc(im, thresh, contours)


def toCV2(im):
    im = im[:, :, ::-1].copy()
    return im


def pre_process_image(img):
    proc = cv2.GaussianBlur(img.copy(), (9, 9), 0)
    proc = cv2.adaptiveThreshold(proc, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    return proc


def finalGrid():
    finalgrid = []
    for i in range(0, len(tempgrid) - 8, 9):
        finalgrid.append(tempgrid[i:i + 9])  # Converting all the cell images to np.array
    for i in range(9):
        for j in range(9):
            finalgrid[i][j] = np.array(finalgrid[i][j])
    try:
        for i in range(9):
            for j in range(9):
                os.remove("BoardCells/cell" + str(i) + str(j) + ".jpg")
    except:
        pass
    for i in range(9):
        for j in range(9):
            cv2.imwrite(str("BoardCells/cell" + str(i) + str(j) + ".jpg"), finalgrid[i][j])
            return finalgrid


def crop_centre(img, cropX, cropY):
    y, x, z = img.shape
    startX = x // 2 - (cropX // 2)
    startY = y // 2 - (cropY // 2)
    return img[startY:startY + cropY, startX:startX + cropX]


def board():
    puzzle = np.zeros([9, 9])
    final = finalGrid()
    box = (50, 40, 108, 120)
    for x in range(9):
        for y in range(9):
            val = readNumber(final[x][y])
            if val is not None:
                puzzle[x][y] = val
    return puzzle


def insertNumber(number):
    print(number)
    x = number * 150
    y = 2700
    myDevice.shell("input tap " + str(x) + " " + str(y))


def getCell(x, y):
    print(x,y)
    x = (x + 1) * 150 - 50
    y = (y + 1) * 150 + 380
    myDevice.shell("input tap " + str(x) + " " + str(y))


def solver(puzzle, solution):
    for x in range(9):
        for y in range(9):
            if puzzle[x][y] == 0:
                val = solution[x][y]
                getCell(y,x)

                insertNumber(val)


myDevice.shell("monkey -p com.easybrain.sudoku.android -c android.intent.category.LAUNCHER 1")
print("App Open")
sleep(2)
myDevice.shell("input tap 670 2387")
print("New Game")
sleep(1)
myDevice.shell("input tap 366 2600")
print("Difficulty")
sleep(1)

image1 = myDevice.screencap()
with open("screen.png", "wb") as fp:
    fp.write(image1)

window_name = 'image'

# Crop image and save it
pic = cv2.imread('screen.png')
crop_img = pic[439:1839, 20:1420].copy()
cv2.imwrite("screen.png", crop_img)

# Reread image
pic = cv2.imread('screen.png', 0)
cropped = pre_process_image(pic)

edge_h = np.shape(cropped)[0]
edge_w = np.shape(cropped)[1]
celledge_h = (edge_h // 9)
celledge_w = (np.shape(cropped)[1] // 9)

tempgrid = []
for i in range(celledge_h, edge_h + 1, celledge_h):
    for j in range(celledge_w, edge_w + 1, celledge_w):
        rows = cropped[i - celledge_h:i]
        tempgrid.append([rows[k][j - celledge_w:j] for k in range(len(rows))])

puzzle = board()
# print(puzzle)
solution = copy.copy(puzzle)

sudoku = SudokuSolution(solution)

solution = sudoku.board
# print(solution)

solver(puzzle, solution)

cv2.imwrite('screen.png', cropped)
