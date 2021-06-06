from cv2 import cv2
import numpy as np
import os
import sys
from inference import *
from sudoku import *
from time import time

def distance(pt1, pt2):
    return np.sqrt((pt1[0][0] - pt2[0][0])**2 + (pt1[0][1] - pt2[0][1])**2)

def preprocessing(im):
    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (11, 11), 0)
    thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    inv = cv2.bitwise_not(thresh)
    return inv

def biggest_grid(canny):
    (contours, _) = cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    final_contours = []
    for c in contours:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.015 * peri, True)
        if len(approx) == 4:
            final_contours.append(c)
    final_contours.sort(key=lambda e: cv2.contourArea(e), reverse=True)
    return final_contours

def prepare_warp(final_contours):
    sorted_add = sorted(((pt, pt[0][0] + pt[0][1]) for pt in final_contours[0]), key=lambda e: e[1])
    sorted_diff = sorted(((pt, pt[0][0] - pt[0][1]) for pt in final_contours[0]), key=lambda e: e[1])

    top_left = sorted_add[0][0]
    top_right = sorted_diff[-1][0]
    bottom_right = sorted_add[-1][0]
    bottom_left = sorted_diff[0][0]

    warp_width = int(max(distance(top_left, top_right), distance(bottom_left, bottom_right)))
    warp_height = int(max(distance(top_left, bottom_left), distance(top_right, bottom_right)))

    warp_uni = max(warp_height, warp_width)

    warp_uni = int(warp_uni + 9/2)
    warp_uni -= warp_uni % 9

    warp_dim = np.array([[0, 0], [warp_uni - 1, 0], [warp_uni - 1, warp_uni - 1], [0, warp_uni - 1]], dtype="float32")
    return np.array([top_left, top_right, bottom_right, bottom_left], dtype="float32"), warp_uni, warp_dim

##################################################################

#im = cv2.imread("sudoku-2.jpeg")
im0 = cv2.imread("tmp/sudoku.png")
im1 = cv2.imread("tmp/carre.jpg")
#im = cv2.imread("sudoku-test1.jpg")
#im = cv2.imread("sudoku-test2.jpg")
#im = cv2.imread("sudoku-test3.jpg")
#im = cv2.imread("sudoku-3.jpg")
#im = cv2.imread("sudoku-original.jpg")
im2 = cv2.imread("my_dataset/raw/IMG_20210530_000116.jpg")

def splitcells(img):
    rows = np.vsplit(img, 9)
    res = []
    for l in rows:
        cols = np.hsplit(l, 9)
        for b in cols:
            res.append(b)
    return res

def image_resize(image, width = None, height = None, inter = cv2.INTER_AREA):
    dim = None
    (h, w) = image.shape[:2]

    if width is None and height is None:
        return image
    if width is None:
        r = height / float(h)
        dim = (int(w * r), height)
    else:
        r = width / float(w)
        dim = (width, int(h * r))
    resized = cv2.resize(image, dim, interpolation = inter)

    return resized


model = load()
def treat(im):
    inv = preprocessing(im)

    canny = cv2.Canny(inv.copy(), 20, 40)

    final_contours = biggest_grid(canny)

    ordered_pts, warp_size, warp_dim = prepare_warp(final_contours)

    grid = cv2.getPerspectiveTransform(ordered_pts, warp_dim)
    perspective = cv2.warpPerspective(inv, grid, (warp_size, warp_size))

    cells = splitcells(perspective)

    raw_grid = [[0 for j in range(9)] for i in range(9)]
    i = 0
    j = 0
    for c in cells:
        reduced = image_resize(c, 28, 28)
        middle = reduced[10:18, 10:18]
        avg = np.mean(middle)
        if avg > 25:
            res = int(find_digit(model, reduced))
            raw_grid[i][j] = res
        j += 1
        if j == 9:
            j = 0
            i += 1

    sol = solve_sudoku([[c for c in line] for line in raw_grid])
    step = warp_size // 9
    coords = [step // 2, step // 2]
    blank_image = np.zeros((perspective.shape[0],perspective.shape[1],3), np.uint8)
    for e in sol:
        for i, l in enumerate(e):
            for j, c in enumerate(l):
                if raw_grid[i][j] == 0:
                    cv2.putText(blank_image, str(c), (coords[0], coords[1]), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 2)
                coords[0] += step
            coords[0] = step // 2
            coords[1] += step
    h = cv2.getPerspectiveTransform(warp_dim, ordered_pts)
    src_warped = cv2.warpPerspective(blank_image, h, (im.shape[1],im.shape[0]))
    im = cv2.add(im, src_warped)
    cv2.imshow("Image", im)
    cv2.waitKey()
    cv2.destroyAllWindows()


treat(im2)