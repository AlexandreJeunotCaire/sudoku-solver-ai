import os
from cv2 import cv2

src = os.path.normpath('D:/work/sharptech/classifier/data/original/test')
dst = os.path.normpath('D:/work/sharptech/classifier/data/resized/test')
dim = (500, 500)
for c in os.listdir(src):
    sub_dir = os.path.join(src, c)
    dst_dir = os.path.join(dst, c)
    os.mkdir(dst_dir)
    for file in os.listdir(sub_dir):
        f_img = os.path.join(sub_dir, file)
        img = cv2.imread(f_img, cv2.IMREAD_UNCHANGED)
        resized = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
        gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)

        dst_img = os.path.join(dst_dir, file)
        cv2.imwrite(dst_img, gray) 