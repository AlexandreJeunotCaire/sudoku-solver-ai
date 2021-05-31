from cv2 import cv2
import numpy as np
import os
import sys

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
    four_corners = None
    for c in contours:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.015 * peri, True)
        if len(approx) == 4:
            final_contours.append(c)
            four_corners = approx
    final_contours.sort(key=lambda e: cv2.contourArea(e), reverse=True)
    return final_contours, four_corners

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
    return np.array([top_left, top_right, bottom_right, bottom_left], dtype="float32"), warp_uni, warp_uni, warp_dim

##################################################################

#im = cv2.imread("sudoku-2.jpeg")
#im = cv2.imread("sudoku.png")
#im = cv2.imread("sudoku-test1.jpg")
#im = cv2.imread("sudoku-test2.jpg")
#im = cv2.imread("sudoku-test3.jpg")
#im = cv2.imread("sudoku-3.jpg")
#im = cv2.imread("sudoku-original.jpg")
im = sys.argv[1]

def splitcells(img):
    rows = np.vsplit(img, 9)
    res = []
    for l in rows:
        cols = np.hsplit(l, 9)
        for b in cols:
            res.append(b)

    """
    for cell in res:
        for i, line in enumerate(cell):
            j = 0
            if line[i] != 0:
                while j < len(line) // 4 or j < len(line) and line[j] > 50:
                    cell[i][j] = 0
                    j += 1

            k = len(line) - 1
            if line[k] != 0:
                while k > (3 * len(line) / 4) or k > 0 and line[k] > 50:
                    cell[i][k] = 0
                    k -= 1

            l = 0

            while l < len(line):
                if line[l] < 200:
                    cell[i][l] = 0
                l += 1
    """
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

def treat(img):
    im = cv2.imread(img)

    inv = preprocessing(im)
    canny = cv2.Canny(inv, 20, 40)

    final_contours, four_corners = biggest_grid(canny)


    cv2.drawContours(im, final_contours[0], -1, (0, 255, 0), 3)
    ordered_pts, warp_width, warp_height, warp_dim = prepare_warp(final_contours)

    grid = cv2.getPerspectiveTransform(ordered_pts, warp_dim)
    perspective = cv2.warpPerspective(inv, grid, (warp_width, warp_height))
    perspective_canny = cv2.Canny(perspective, 20, 40)


    cells = splitcells(perspective)

    #cv2.imshow("Image", im)
    #cv2.imshow("Grid", perspective_canny)

    for i, c in enumerate(cells):
        #cnt, _ = cv2.findContours(c, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        #cnt.sort(key=lambda e: cv2.contourArea(e), reverse=True)
        #print(len(cnt))
        #cp = im.copy()
        #cv2.drawContours(cp, cnt, -1, (0, 0, 255), 1)
        tmp = image_resize(c, 28, 28)
        #cv2.imshow(f"Image {i}", tmp)
        #cv2.waitKey(0)
        #cv2.destroyAllWindows()
        #print("./my_dataset/cells/" + img[17:-4] + "_" + str(i) + ".jpg")
        cv2.imwrite("./my_dataset/cells/" + img[17:-4] + "_" + str(i) + ".jpg", tmp)

    #cv2.waitKey()
    #cv2.destroyAllWindows()


#print(im)
treat(im)